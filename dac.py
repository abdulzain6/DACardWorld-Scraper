from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium import webdriver
from tempfile import mkdtemp
from selenium_stealth import stealth
import random, json, os
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import pygsheets
import pandas as pd

def get_data(page_no: int) -> dict:
    """Gets the data from the site"""
    
    script = """
    async function get_data(page_no) {
        data = await fetch('https://typesense.dacardworld.com/buy-list/0/multi_search?x-typesense-api-key=', {
            method: 'POST',
            headers: {
                'authority': 'typesense.dacardworld.com',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'text/plain',
                'dnt': '1',
                'origin': 'https://www.dacardworld.com',
                'referer': 'https://www.dacardworld.com/',
                'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
            },
        body: '{"searches":[{"query_by":"title,barcode","sort_by":"featured:desc,_text_match:desc,year_sort:desc","highlight_full_fields":"title,barcode","collection":"items_buying","q":"*","facet_by":"package,year,series,categories.lvl0","filter_by":"package:=[`Tin`,`Box`,`Set`,`Pack`,`Deck`,`Case`]","max_facet_values":100,"page":'+page_no+',"per_page":250},{"query_by":"title,barcode","sort_by":"featured:desc,_text_match:desc,year_sort:desc","highlight_full_fields":"title,barcode","collection":"items_buying","q":"*","facet_by":"package","max_facet_values":100,"page":1}]}'
        })
        data = await data.text()
        return data
    }
    return get_data(""" + str(page_no) + """);"""
    documents = []
    hits = json.loads(driver.execute_script(script))["results"][0]["hits"]
    for hit in hits:
        documents.append(hit["document"])
    return documents

def store_data(df):
    gc = pygsheets.authorize(service_file='creds.json')
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/12gUBxQZf5p1H4MA8oTuNW0IbdLXO6TDx1YjrlutUOcQ/edit#gid=0")
    content_sheet = sh.worksheet_by_title("Sheet1")
    content_sheet.set_dataframe(df, (1,1), fit=True)

def get_total_items(page_source: str) -> int:
    """Get the total number of items"""

    total = 0
    item_type = ["box", "set", "case", "pack", "deck", "tin"]
    soup = BeautifulSoup(page_source, "html.parser")
    filters = soup.find_all("label", class_="ais-RefinementList-label")
    for filter in filters:
        title = filter.find("span", class_="ais-RefinementList-labelText").text
        if title.lower() not in item_type:
            continue
        total_items_by_type = filter.find("span", class_="ais-RefinementList-count label radius secondary right").text.replace(",", "")
        total += int(total_items_by_type)
    return total



if __name__ == "__main__":
    options = uc.ChromeOptions()
    options.add_argument(f'--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36')
    options.add_argument(f"--window-size={random.randrange(1000,1100)},{random.randrange(1000,1100)}")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu-sandbox')
    options.add_argument('--headless')
    options.add_argument("--single-process")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--incognito")
    seleniumwire_options = {}
    directory = mkdtemp()
    capabilities = webdriver.DesiredCapabilities.CHROME
    driver = uc.Chrome(options=options,  user_data_dir=directory,desired_capabilities=capabilities, version_main=110)
    renderers = [
        ("ANGLE (AMD, AMD Radeon Vega 3 Graphics (raven2 LLVM 14.0.6), OpenGL 4.6", "Google Inc. (AMD)"),
    ]
    renderer = random.choice(renderers)
    stealth(driver,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        platform="Linux x86_64",
    )
    driver.get("https://www.dacardworld.com/buying/buy-list/")
    total = get_total_items(driver.page_source)
    print(f"Total Number of items found: {total}")
    data = []
    for i in range(1, (total//250) + 1):
        data.extend(get_data(i))
    with open("Data.json", "w") as fp:
        json.dump(data, fp)
