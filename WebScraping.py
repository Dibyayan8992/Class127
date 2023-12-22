from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
browser = webdriver.Chrome("")
browser.get(START_URL)
time.sleep(3)

headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
planet_data = []
new_planet_data = []
final_data = []

def scrape():
    for i in range(0, 1):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink = "https://exoplanets.nasa.gov"+li_tags[0].find_all("a", href = True)[0]["href"]
            temp_list.append(hyperlink)
            planet_data.append(temp_list)
        browser.find_element("xpath", '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

def scrape_more_data(hyperlink):
    page  = requests.get(hyperlink)
    soup = BeautifulSoup(page.content, "html.parser")
    temp_list = []
    tr_tags = soup.find_all("tr", attrs = {"class": "fact_row"})
    
    for tr_tag in tr_tags:
        td_tags = tr_tag.find_all("td")
        
        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div", attrs = {"class": "value"})[0].contents[0])
            except:
                temp_list.append("")
        
    new_planet_data.append(temp_list)

scrape()

for data in planet_data:
    scrape_more_data(data[5])

for index, data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element]
    final_data.append(data + new_planet_data_element)

with open("final.csv", "w", newline="") as f:
         csvwriter = csv.writer(f)
         csvwriter.writerow(headers)
         csvwriter.writerows(final_data)