# mangatracker

> **Disclaimer**: This is a personal project created for educational and portfolio purposes only. It is not intended for production use or redistribution. The author does not encourage or endorse scraping third-party websites. Users are responsible for complying with the terms of service of any website they interact with.

A personal Python script that tracks manga titles by scraping metadata from popular websites and storing it in a local SQLite database.

## Features

- **Source A**: Fetches Italian metadata (title, author, artist, category, year, volumes, status, release dates) from an Italian manga database
- **Source B**: Fetches ratings, member count, ranking and popularity from a popular anime/manga catalog

## Setup

1. Create a conda environment:
   ```
   conda create -n mangatracker python=3.12 requests beautifulsoup4 openpyxl
   conda activate mangatracker
   pip install python-dotenv
   ```

2. Copy `app/.env.example` to `app/.env` and fill in your configuration:
   ```
   cp app/.env.example app/.env
   ```

3. Run the migration to import manga URLs from the Excel file into SQLite:
   ```
   cd app
   python migrate_from_excel.py
   ```

## Usage

```
cd app
python main.py
```

You will be presented with a menu:
```
Choose an option:
- 'a' : Source A - get basic metadata and next volumes dates
- 'm' : Source B - get ratings, popularity and rank
- 'b' : Fetches from both services, then quits
- 'q' : QUIT
```

## Project structure

```
app/
  main.py              # Entry point with menu
  source_a.py          # Source A scraper
  source_b.py          # Source B scraper
  .env.example         # Environment variables template
  db.py                # SQLite database operations
  config.py            # Loads settings from .env (not tracked)
  migrate_from_excel.py # One-time migration from Excel to SQLite
```

## Author

Dylan Tangredi\
[linkedin](https://www.linkedin.com/in/dylantangredi/)
