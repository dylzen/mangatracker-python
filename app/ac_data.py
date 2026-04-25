import config as config
import file_ops
import requests
import re
from bs4 import BeautifulSoup

AC_COOKIES = {"ac_campaign": "show"}

def get_data(user_input):
    print("Fetching data...")
    home_url = config.ac_home_url
    titles_ita = []
    stories = []
    drawings = []
    categories = []
    years = []
    volumes = []
    italy_stati = []
    next_releases = []
    next_releases_long = []
    next_releases_dates = []
    latest_releases = []
    latest_releases_dates = []

    mangalist = file_ops.get_titles(user_input)
    for manga in mangalist:
        print("Fetching "+manga)
        response = requests.get(manga, cookies=AC_COOKIES)
        soup = BeautifulSoup(response.text, 'html.parser')
        titolo_italiano = soup.find('h1').getText()
        print(titolo_italiano)
        storia = soup.find(text="Storia")
        disegni = soup.find(text="Disegni")
        categoria = soup.find(text="Categoria")
        anno = soup.find(text="Anno")
        volumi = soup.find(text=re.compile("Volumi"))
        stato_ita = soup.find(text="Stato in Italia")
        
        storia_td = storia.parent
        disegni_td = disegni.parent
        categoria_td = categoria.parent
        anno_td = anno.parent
        volumi_td = volumi.parent
        stato_ita_td = stato_ita.parent

        target_sto = storia_td.find_next_sibling('dd').text
        target_dis = disegni_td.find_next_sibling('dd').text
        target_cat = categoria_td.find_next_sibling('dd').text
        target_anno = anno_td.find_next_sibling('dd').text
        target_volumi = volumi_td.find_next_sibling('dd').text
        target_statoIt = stato_ita_td.find_next_sibling('dd').text

        titles_ita.append(titolo_italiano.strip())
        stories.append(target_sto.strip())
        drawings.append(target_dis.strip())
        target_cat = re.sub("\s+", " ", target_cat.strip())
        categories.append(target_cat.strip())
        target_anno = re.sub("\s+", "", target_anno.strip())
        years.append(target_anno.strip())
        volumes.append(target_volumi.strip())
        italy_stati.append(target_statoIt.strip())

        if ((target_statoIt.strip() == "in corso") or (target_statoIt.strip() == "annunciato") or (target_statoIt.strip() == "Riedizione in corso")) and soup.find(text="Prossima uscita") is not None:
            prossima_uscita = soup.find('h3').getText()
            next_releases_long.append(prossima_uscita.strip())
            next_release_link = soup.select_one("a[href*=edizione\/]")
            next_releases_dates.append(home_url+next_release_link.get('href'))
            latest_releases.append("")
            latest_releases_dates.append("N.D.")
        elif target_statoIt.strip() == "completato" and soup.find(text="Prossima uscita") is not None:
            prossima_uscita = soup.find('h3').getText()
            next_releases_long.append(prossima_uscita.strip())
            next_release_link = soup.select_one("a[href*=edizione\/]")
            next_releases_dates.append(home_url+next_release_link.get('href'))
            latest_releases.append("")
            latest_releases_dates.append("N.D.")
        elif soup.find(text="Ultima uscita") is not None:
            ultima_uscita = soup.find('h3').getText()
            latest_releases.append("Ultima uscita: "+ultima_uscita.strip())
            next_release_link = soup.select_one("a[href*=edizione\/]")
            latest_releases_dates.append(home_url+next_release_link.get('href'))
            next_releases.append("")
            next_releases_long.append("")
            next_releases_dates.append("N.D.")
        else:
            next_releases.append("")
            next_releases_long.append("")
            next_releases_dates.append("N.D.")
            latest_releases.append("")
            latest_releases_dates.append("N.D.")
            continue           

    print("Creating dates list...")
    next_volume_dates = []
    latest_volume_dates = []
    for item in next_releases_dates:
        if item != "N.D.":
            print("Found new release date for manga: " +item)
            response_next = requests.get(item, cookies=AC_COOKIES)
            soup_next = BeautifulSoup(response_next.text, 'html.parser')
            next_date_parent = soup_next.find('strong', text="Data pubblicazione:")
            next_volume_dates.append(next_date_parent.next_sibling.text)
        else:
            next_volume_dates.append("")

    for item in latest_releases_dates:
        if item != "N.D.":
            response_latest = requests.get(item, cookies=AC_COOKIES)
            soup_latest = BeautifulSoup(response_latest.text, 'html.parser')
            latest_date_parent = soup_latest.find('strong', text="Data pubblicazione:")
            latest_volume_dates.append(latest_date_parent.next_sibling.text)
        else:
            latest_volume_dates.append("")

    dates_new = []
    for date in next_volume_dates:
        dates_new.append(date.replace('/01/', 'gen').replace('/11/', 'nov').replace('/12/', 'dic'))
    
    return user_input, titles_ita, stories, drawings, categories, years, volumes, latest_releases, latest_volume_dates, next_releases_long, next_volume_dates, italy_stati

def ac_write_to_xlsx(user_input):
    user_input, titles_ita, stories, drawings, categories, years, volumes, latest_releases, latest_volume_dates, next_releases_long, next_volume_dates, italy_stati = get_data(user_input)

    print("Writing data to excel file...")
    path_collection, book = file_ops.load_book()
    sheet = book['auto']

    column = 1
    sheet.cell(row=1, column=column, value="Titolo italiano")
    for i, value in enumerate(titles_ita, start=1):
        sheet.cell(row=i+1, column=column, value=value)
    column = 2
    sheet.cell(row=1, column=column, value="Storia")
    for i, value in enumerate(stories, start=1):
        sheet.cell(row=i+1, column=column, value=value)
    column = 3
    sheet.cell(row=1, column=column, value="Disegni")
    for i, value in enumerate(drawings, start=1):
        sheet.cell(row=i+1, column=column, value=value)
    column = 4
    sheet.cell(row=1, column=column, value="Categoria")
    for i, value in enumerate(categories, start=1):
        sheet.cell(row=i+1, column=column, value=value)
    column = 5
    sheet.cell(row=1, column=column, value="Anno")
    for i, value in enumerate(years, start=1):
        sheet.cell(row=i+1, column=column, value=value)
    column = 6
    sheet.cell(row=1, column=column, value="Volumi pubblicati")
    for i, value in enumerate(volumes, start=1):
        sheet.cell(row=i+1, column=column, value=value)
    column = 7
    sheet.cell(row=1, column=column, value="Ultimo volume")
    for i, value in enumerate(latest_releases, start=1):
        sheet.cell(row=i+1, column=column, value=value)
    column = 8
    sheet.cell(row=1, column=column, value="Ultima data di uscita")
    for i, value in enumerate(latest_volume_dates, start=1):
        sheet.cell(row=i+1, column=column, value=value)
    column = 9
    sheet.cell(row=1, column=column, value="Prossimo volume")
    for i, value in enumerate(next_releases_long, start=1):
        sheet.cell(row=i+1, column=column, value=value)
    column = 10
    sheet.cell(row=1, column=column, value="Prossima data di uscita")
    for i, value in enumerate(next_volume_dates, start=1):
        sheet.cell(row=i+1, column=column, value=value)
    column = 14
    sheet.cell(row=1, column=column, value="Stato in Italia")
    for i, value in enumerate(italy_stati, start=1):
        sheet.cell(row=i+1, column=column, value=value)

    book.save(path_collection)
    print("Collection file updated successfully.")
    
    file_ops.copy_to_cloud(path_collection, config.path_cloud)
    print("Collection file copied for cloud sync.")

