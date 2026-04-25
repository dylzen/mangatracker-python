"""One-time migration script to import AC and MAL URLs from the Excel file into SQLite."""

import os
from openpyxl import load_workbook
import db

EXCEL_PATH = os.path.join(os.path.dirname(__file__), "..", "Manga_Collection.xlsx")

AC_URL_COL = 26
MAL_URL_COL = 25


def migrate():
    db.init_db()

    book = load_workbook(EXCEL_PATH, read_only=True)
    sheet = book["auto"]

    ac_urls = []
    mal_urls = []

    for row in sheet.iter_rows(min_row=2, min_col=AC_URL_COL, max_col=AC_URL_COL):
        value = row[0].value
        if value:
            ac_urls.append(value)

    for row in sheet.iter_rows(min_row=2, min_col=MAL_URL_COL, max_col=MAL_URL_COL):
        value = row[0].value
        if value:
            mal_urls.append(value)

    book.close()

    for i, ac_url in enumerate(ac_urls):
        mal_url = mal_urls[i] if i < len(mal_urls) else None
        db.insert_manga(ac_url=ac_url, mal_url=mal_url)
        print(f"Imported: {ac_url}")

    # Import any remaining MAL URLs that didn't have a matching AC row
    for i in range(len(ac_urls), len(mal_urls)):
        db.insert_manga(mal_url=mal_urls[i])
        print(f"Imported (MAL only): {mal_urls[i]}")

    print(f"\nMigration complete. Imported {max(len(ac_urls), len(mal_urls))} manga entries.")


if __name__ == "__main__":
    migrate()
