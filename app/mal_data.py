from datetime import datetime

import config
import file_ops
import requests
from bs4 import BeautifulSoup

COLUMNS = [
    (20, "ratings_mal", "rating"),
    (21, "members_MAL", "members"),
    (22, "ranking_MAL", "ranking"),
    (23, "popularity_MAL", "popularity"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}


def get_data(user_input):
    print("Fetching data...")
    results = []

    for item_link in file_ops.get_titles(user_input):
        print("Fetching: " + item_link)
        response = requests.get(item_link, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        rating = soup.select_one('div[class*="score-label"]')
        member = soup.select_one('span[class="numbers members"] strong')
        ranking = soup.select_one('span[class="numbers ranked"] strong')
        popularity = soup.select_one('span[class="numbers popularity"] strong')

        results.append({
            "rating": rating.text.strip() if rating else "",
            "members": member.text.strip() if member else "",
            "ranking": ranking.text.strip() if ranking else "",
            "popularity": popularity.text.strip() if popularity else "",
        })

    return results


def mal_write_to_xlsx(user_input):
    results = get_data(user_input)

    print("Writing data to excel file...")
    path_collection, book = file_ops.load_book()
    sheet = book["Lista"]
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    for col_num, header, key in COLUMNS:
        sheet.cell(row=1, column=col_num, value=header)
        for row_num, entry in enumerate(results, start=2):
            sheet.cell(row=row_num, column=col_num, value=entry[key])

    sheet.cell(row=1, column=25, value=timestamp)

    book.save(path_collection)
    print("Collection file updated successfully.")

    file_ops.copy_to_cloud(path_collection, config.path_cloud)
