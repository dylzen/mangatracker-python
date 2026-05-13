from datetime import datetime

import db
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}


def _parse_float(text):
    try:
        return float(text)
    except (ValueError, TypeError):
        return None


def _parse_int(text):
    try:
        return int(text.replace(",", "").replace("#", ""))
    except (ValueError, TypeError, AttributeError):
        return None


def fetch_and_store():
    print("Fetching Source B data...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for url in db.get_source_b_urls():
        print("Fetching: " + url)
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        rating = soup.select_one('div[class*="score-label"]')
        member = soup.select_one('span[class="numbers members"] strong')
        ranking = soup.select_one('span[class="numbers ranked"] strong')
        popularity = soup.select_one('span[class="numbers popularity"] strong')

        data = {
            "rating": _parse_float(rating.text.strip()) if rating else None,
            "members": _parse_int(member.text) if member else None,
            "ranking": _parse_int(ranking.text) if ranking else None,
            "popularity": _parse_int(popularity.text) if popularity else None,
        }

        db.update_source_b_data(url, data, timestamp)

    print("Source B data updated successfully.")
