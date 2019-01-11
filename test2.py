import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm
import pandas as pd

tqdm.monitor_interval = 0


def clear_score(list_scores: list) -> str:
    st =""
    for item in list_scores:
        if item.contents.__len__() > 0:
            if item.contents[0] == "Серия буллитов:":
                st += str(-1) + " "
            else:
                st += item.contents[0] + " "
    if st.__len__() > 1:
        st = st[:-1]
    return st


list_match = list()
data_match = []
list_hosts = []
list_guests = []
list_score = []
list_hosts_time = []
list_guests_time = []

number_month = [10, 11, 12, 1, 2, 3, 4]
#number_month = [10]
list_page = None
for i in number_month:
    text = requests.get('https://www.sports.ru/nhl/calendar/?s=6882&m={}'.format(str(i)))
    soup = BeautifulSoup(text.text, 'html.parser')
    list_match += soup.findAll('tr')

# artist_name_list = set(artist_name_list)
for item in list_match:
    if item.contents.__len__() != 9:
        list_match.remove(item)

for item in list_match:
    if item.contents.__len__() != 9:
        list_match.remove(item)

print(list_match.__len__())
i = 0
for item in list_match:
    try:
        data_match.append(item.contents[1].contents[1].contents[0] + ' ' + item.contents[1].contents[1].contents[2])
        list_hosts.append(item.contents[3].contents[0].contents[2].contents[0])
        list_guests.append(item.contents[5].contents[0].contents[2].contents[0])

        score = list(item.contents[4].contents[0].contents[0].findAll('b'))
        if score.__len__() == 1:
            list_score.append(score[0].contents[0])
        else:
            list_score.append(score[0].contents[0] + score[1].contents[0])

        if list_score[-1] != "- : -":
            url = item.contents[4].contents[0].get('href')
            text = requests.get(url)
            soup = BeautifulSoup(text.text, 'html.parser')

            list_L = soup.findAll("div", class_="command floatL")[0].findAll("div", class_="js-first-team")[0].findAll('b')
            #print(list_L)
            st = clear_score(list_L)
            print(st)
            list_hosts_time.append(st)

            list_R = soup.findAll("div", class_="command floatR")[0].findAll("div", class_="js-second-team")[0].findAll('b')
            #print(list_R)
            strok = clear_score(list_R)
            print(strok)
            list_guests_time.append(strok)
            print('матч__{}_________________________________________________'.format(i))
            i += 1
    except:
        print(item.contents[3].contents[0].contents[2].contents[0] + "VS" +
              item.contents[5].contents[0].contents[2].contents[0])






i = 0
while i != data_match.__len__():
    print(data_match[i] + '|||' + list_hosts[i] + '  время' + list_hosts_time[i] + '  ' + list_score[i] + '  ' +
          list_guests[i] + '  время' + list_guests_time[i])
    i += 1


list_hat = "Дата матча", "Хозяева", "Время забитых шайб(Х)", "Счет в матче", "Гости", "Время забитых шайб(Г)"


frame = pd.DataFrame([data_match, list_hosts, list_hosts_time, list_score, list_guests, list_guests_time]) # собираем фрейм
frame.to_csv('my_csv_export.csv',sep=',', decimal=';',index=False) #экспортируем в файл


# for item in artist_name_list:
#     print(item.contents.__len__())
