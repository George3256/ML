import numpy

import pandas as pd
import os
HOCKEY_PATH = os.path.join("datasets", "hockey")

def load_hockey_data(hockey_path=HOCKEY_PATH):
    csv_path = os.path.join(hockey_path, "hockey.csv")
    return pd.read_csv("hockey.csv")
hockey = load_hockey_data()
#print(hockey.head())

def count1P(list_time: list):
    count = 0
    if str(list_time) != 'nan':
        for i in list_time:
            if int(i) <= 20 and int(i) != -1:
                count += 1
    return count

def count2P(list_time: list):
    count = 0
    if str(list_time) != 'nan':
        for i in list_time:
            if int(i) <= 20 and int(i) != -1:
                count += 1
    return count

hockey['1PHosts'] = hockey['Время Х'].str.split(" ").apply(count1P)
print(hockey['Время Х'])
print(hockey['1PHosts'])
