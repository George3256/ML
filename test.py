import requests
from bs4 import BeautifulSoup
import csv

page10 = requests.get('https://www.sports.ru/nhl/calendar/?s=6882&m=10')
page11 = requests.get('https://www.sports.ru/nhl/calendar/?s=6882&m=11')
page12 = requests.get('https://www.sports.ru/nhl/calendar/?s=6882&m=12')

soup = BeautifulSoup(page10.text, 'html.parser')
artist_name_list = soup.findAll(class_='player')
soup = BeautifulSoup(page11.text, 'html.parser')
artist_name_list += soup.findAll(class_='player')
soup = BeautifulSoup(page12.text, 'html.parser')
artist_name_list += soup.findAll(class_='player')

artist_name_list = set(artist_name_list)
for item in artist_name_list:
    print(item.contents[0])
    #+ item.get('href')
print(artist_name_list.__len__())