import datetime
import os

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
list_data = []
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
        print("next")
        sc = ""
        score = list(item.contents[4].contents[0].contents[0].findAll('b'))
        if score.__len__() == 1:
            sc = score[0].contents[0]
        else:
            sc = score[0].contents[0] + score[1].contents[0]
        if sc != "- : -":
            data_match.append(str(item.contents[1].contents[1].contents[0]).split("\n")[1].replace(".", "-")) #+ ' ' + item.contents[1].contents[1].contents[2])
            list_hosts.append(item.contents[3].contents[0].contents[2].contents[0])
            list_guests.append(item.contents[5].contents[0].contents[2].contents[0])

            list_score.append(sc)


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
        else:
            break
    except:
        print(item.contents[3].contents[0].contents[2].contents[0] + "VS" +
              item.contents[5].contents[0].contents[2].contents[0])


# i = 0
# while i != data_match.__len__():
#     print(data_match[i] + '|||' + list_hosts[i] + '  время' + list_hosts_time[i] + '  ' + list_score[i] + '  ' +
#           list_guests[i] + '  время' + list_guests_time[i])
#     i += 1


list_hat = "Дата матча", "Хозяева", "Время забитых шайб(Х)", "Гости", "Время забитых шайб(Г)"

raw_data = {
        'DataTime': data_match,
        'Хозяева': list_hosts,
        'Время Х': list_hosts_time,
        'Гости': list_guests,
        'Время Г': list_guests_time}
df = pd.DataFrame(raw_data, columns=['DataTime', 'Хозяева', 'Время Х', 'Гости', 'Время Г'])
time = datetime.datetime.now()
# frame = pd.DataFrame(list_hosts, list_hosts_time, list_score, list_guests, list_guests_time) # собираем фрейм
df_path = os.path.join("datasets","hockey", 'collect_data_hockey_{}_{}_{}.csv'.format(time.year, time.month, time.day))
df.to_csv(df_path, sep=',', decimal=';', index=False) #экспортируем в файл


hockey = pd.read_csv(df_path)
def count1P(list_time: list):
    count = 0
    if str(list_time) != 'nan':
        for i in list_time:
            if int(i) < 20 and int(i) != -1:
                count += 1
    return count
def count2P(list_time: list):
    count = 0
    if str(list_time) != 'nan':
        for i in list_time:
            if int(i) > 19 and int(i) < 40 and int(i) != -1:
                count += 1
    return count
def count3P(list_time: list):
    count = 0
    if str(list_time) != 'nan':
        for i in list_time:
            if int(i) > 39 and int(i) < 60 and int(i) != -1:
                count += 1
    return count
def countOT(list_time: list):
    count = 0
    if str(list_time) != 'nan':
        for i in list_time:
            if int(i) > 59 and int(i) != -1:
                count += 1
    return count
def countSS(list_time: list):
    count = 0
    if str(list_time) != 'nan':
        for i in list_time:
            if int(i) == -1:
                count += 1
    return count
hockey['1PHosts'] = hockey['Время Х'].str.split(" ").apply(count1P)
hockey['2PHosts'] = hockey['Время Х'].str.split(" ").apply(count2P)
hockey['3PHosts'] = hockey['Время Х'].str.split(" ").apply(count3P)
hockey['OTHosts'] = hockey['Время Х'].str.split(" ").apply(countOT)
hockey['SSHosts'] = hockey['Время Х'].str.split(" ").apply(countSS)
hockey['CountHosts'] = hockey['SSHosts'] + hockey['OTHosts'] + hockey['3PHosts'] + hockey['2PHosts'] + hockey['1PHosts']


hockey['1PGuests'] = hockey['Время Г'].str.split(" ").apply(count1P)
hockey['2PGuests'] = hockey['Время Г'].str.split(" ").apply(count2P)
hockey['3PGuests'] = hockey['Время Г'].str.split(" ").apply(count3P)
hockey['OTGuests'] = hockey['Время Г'].str.split(" ").apply(countOT)
hockey['SSGuests'] = hockey['Время Г'].str.split(" ").apply(countSS)
hockey['CountGuests'] = hockey['SSGuests'] + hockey['OTGuests'] + hockey['3PGuests'] + hockey['2PGuests'] + hockey['1PGuests']

new_hockey = hockey[["DataTime","Хозяева","Гости","1PHosts","2PHosts","3PHosts","OTHosts","SSHosts","CountHosts","1PGuests" ,"2PGuests","3PGuests","OTGuests","SSGuests","CountGuests"]]

new_hockey = new_hockey.rename(columns={'Хозяева': 'Hosts', 'Гости': 'Guests'})
new_new_hockey = new_hockey.copy()
df_path = os.path.join("datasets","hockey", 'collect_and_prepare_data_hockey_{}_{}_{}.csv'.format(time.year, time.month, time.day))
new_new_hockey.to_csv(df_path, sep=',', encoding='utf-8', index=False)
# for item in artist_name_list:
#     print(item.contents.__len__())
