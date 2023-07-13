import requests
import time
import numpy
import pandas as pd
import locale
from datetime import datetime
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL, 'fr_FR')

base_url = "https://www.kijiji.ca"
page_1_url = base_url + "/b-appartement-condo/ville-de-montreal/1+1+2+ou+2+1+2/page-1/c37l1700281a27949001?radius=10.0&price=__1300&address=1400+Maisonneuve+Blvd+W%2C+Montreal%2C+QC+H3G+1M8%2C+Canada&ll=45.496845,-73.577866"
page_2_url = base_url + "/b-appartement-condo/ville-de-montreal/1+1+2+ou+2+1+2/page-2/c37l1700281a27949001?radius=10.0&price=__1300&address=1400+Maisonneuve+Blvd+W%2C+Montreal%2C+QC+H3G+1M8%2C+Canada&ll=45.496845,-73.577866"
page_3_url = base_url + "/b-appartement-condo/ville-de-montreal/1+1+2+ou+2+1+2/page-3/c37l1700281a27949001?radius=10.0&price=__1300&address=1400+Maisonneuve+Blvd+W%2C+Montreal%2C+QC+H3G+1M8%2C+Canada&ll=45.496845,-73.577866"
page_4_url = base_url + "/b-appartement-condo/ville-de-montreal/1+1+2+ou+2+1+2/page-4/c37l1700281a27949001?radius=10.0&price=__1300&address=1400+Maisonneuve+Blvd+W%2C+Montreal%2C+QC+H3G+1M8%2C+Canada&ll=45.496845,-73.577866"
page_5_url = base_url + "/b-appartement-condo/ville-de-montreal/1+1+2+ou+2+1+2/page-5/c37l1700281a27949001?radius=10.0&price=__1300&address=1400+Maisonneuve+Blvd+W%2C+Montreal%2C+QC+H3G+1M8%2C+Canada&ll=45.496845,-73.577866"

pages = [page_1_url, page_2_url, page_3_url, page_4_url, page_5_url]
df = pd.DataFrame(columns=["title", "price", "description", "date_posted",
                           "address", "url", "parking", "date d'emménagement", "animals", "area"])

for page in pages:

    response = requests.get(page)
    soup = BeautifulSoup(response.text, "lxml")
    ads = soup.find_all("div", class_=['search-item', 'regular-ad'])

    # Now I will create a list to store all the links of every ad
    ad_links = []
    for ad in ads:
        link = ad.find_all("a", class_='title')
        for l in link:
            ad_links.append(base_url + l['href'])
    print(len(ad_links))

    # From here I will explore every link individually in my list ad_links, and take the necessary directly from the given link
    for i in ad_links:
        response = requests.get(i)
        soup = BeautifulSoup(response.text, "lxml")

        # get ad title

        try:
            title = soup.find("h1").text
        except AttributeError:
            title = ""

        # get ad price
        try:
            if len(soup.find('div', class_='titleRow-4059548442').find_next('span').get_text().split()[:-1]) >= 2:
                list_ = soup.find('div', class_='titleRow-4059548442').find_next('span').get_text().split()[:-1]
                price = float(list_[0] + list_[1])
            else:
                price = float(soup.find('div', class_='titleRow-4059548442').find_next('span').get_text().split()[0])
        except AttributeError:
            price = ""

        # get date posted
        try:
            date_posted = datetime.strptime(soup.find("div", class_="datePosted-383942873").find_next('time')['title'],
                                            '%d %B %Y %H:%M')
        except (AttributeError, TypeError):
            date_posted = ""

        # get ad description
        try:
            description = soup.find("div", class_="descriptionContainer-3460900372").find_next('p').get_text()
        except AttributeError:
            description = ""

        # get the ad city
        try:
            address = soup.find("span", itemprop="address").get_text().strip()
        except AttributeError:
            address = ""

        # get the parking

        try:
            parking = soup.find('dd', class_='twoLinesValue-2815147826').get_text().strip()
        except AttributeError:
            parking = ""

        # get the date of moving in
        try:
            move_in_date = datetime.strptime(soup.find('h3', string="Aperçu").find_previous('div').find_next('dt', string="Date d'emménagement").find_previous('dl').find_next('dd').get_text(), '%d %B %Y')
        except AttributeError:
            move_in_date = ""

        # get animals
        try:
            animals = soup.find('h3', string="Aperçu").find_previous('div').find_next('dt',
                                                                                      string="Animaux acceptés").find_previous(
                'dl').find_next('dd').get_text()
        except AttributeError:
            animals = ""

        # get the area
        try:
            area = soup.find('h3', string="L'unité d'habitation").find_previous('div').find_next('dd').get_text()
        except AttributeError:
            area = ""

        df = df.append({
            "title": title,
            "price": price,
            "date_posted": date_posted,
            "address": address,
            "url": i,
            "parking": parking,
            "date d'emménagement": move_in_date,
            "animals": animals,
            "area": area,
            "description": description
        },
            ignore_index=True
        )
    df.to_csv("Renting_properties_data.csv")
print(df)
