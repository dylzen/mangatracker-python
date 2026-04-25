from datetime import datetime

import db
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}


def fetch_and_store():
    print("Fetching Source B data...")
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    for url in db.get_source_b_urls():
        print("Fetching: " + url)
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        rating = soup.select_one('div[class*="score-label"]')
        member = soup.select_one('span[class="numbers members"] strong')
        ranking = soup.select_one('span[class="numbers ranked"] strong')
        popularity = soup.select_one('span[class="numbers popularity"] strong')

        data = {
            "rating": rating.text.strip() if rating else "",
            "members": member.text.strip() if member else "",
            "ranking": ranking.text.strip() if ranking else "",
            "popularity": popularity.text.strip() if popularity else "",
        }

        db.update_source_b_data(url, data, timestamp)

    print("Source B data updated successfully.")
