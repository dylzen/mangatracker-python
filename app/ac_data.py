import re

import config
import db
import requests
from bs4 import BeautifulSoup

AC_COOKIES = {"ac_campaign": "show"}


def _fetch_page(url):
    response = requests.get(url, cookies=AC_COOKIES)
    return BeautifulSoup(response.text, "html.parser")


def _get_field(soup, label):
    tag = soup.find(text=re.compile(rf"^\s*{label}\s*$"))
    if tag is None:
        return ""
    return re.sub(r"\s+", " ", tag.parent.find_next_sibling("dd").text.strip())


def _get_release_date(url):
    soup = _fetch_page(url)
    date_tag = soup.find("strong", text="Data pubblicazione:")
    if date_tag and date_tag.next_sibling:
        return date_tag.next_sibling.text.strip()
    return ""


def _parse_release_info(soup, home_url):
    has_next = soup.find(text="Prossima uscita") is not None
    has_latest = soup.find(text="Ultima uscita") is not None

    prossimo_volume = ""
    prossima_data = ""
    ultimo_volume = ""
    ultima_data = ""

    if has_next:
        h3 = soup.find("h3")
        prossimo_volume = h3.getText().strip() if h3 else ""
        link = soup.select_one("a[href*=edizione\\/]")
        if link:
            prossima_data = _get_release_date(home_url + link.get("href"))
    elif has_latest:
        h3 = soup.find("h3")
        ultimo_volume = "Ultima uscita: " + h3.getText().strip() if h3 else ""
        link = soup.select_one("a[href*=edizione\\/]")
        if link:
            ultima_data = _get_release_date(home_url + link.get("href"))

    return prossimo_volume, prossima_data, ultimo_volume, ultima_data


def fetch_and_store():
    print("Fetching AC data...")
    home_url = config.ac_home_url

    for ac_url in db.get_ac_urls():
        print("Fetching " + ac_url)
        soup = _fetch_page(ac_url)

        titolo = soup.find("h1").getText().strip()
        print(titolo)

        stato = _get_field(soup, "Stato in Italia")
        prossimo_volume, prossima_data, ultimo_volume, ultima_data = (
            _parse_release_info(soup, home_url)
        )

        data = {
            "titolo_italiano": titolo,
            "storia": _get_field(soup, "Storia"),
            "disegni": _get_field(soup, "Disegni"),
            "categoria": _get_field(soup, "Categoria"),
            "anno": re.sub(r"\s+", "", _get_field(soup, "Anno")),
            "volumi": _get_field(soup, "Volumi"),
            "stato_italia": stato,
            "prossimo_volume": prossimo_volume,
            "prossima_data": prossima_data,
            "ultimo_volume": ultimo_volume,
            "ultima_data": ultima_data,
        }

        db.update_ac_data(ac_url, data)

    print("AC data updated successfully.")
