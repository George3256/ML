import os
import pandas as pd
import matplotlib.pyplot as plt

filename = os.path.join("datasets", "hockey", "new_hockey_2019_01_18.csv")
def load_hockey_data(filename):
    return pd.read_csv(filename, sep=',', encoding='utf-8')

hockey = load_hockey_data(filename)
data = None
def plot_statistic_hosts(comand, column):
    global data
    filepath = os.path.join("plotting", "Комманда_{}   Период_{}.png". format(comand, column))
    data = hockey[["DataTime", column]].where(hockey["Hosts"] == comand).dropna()
    plt.figure(figsize=(30, 5))
    plt.plot(data["DataTime"], data[column])
    plt.savefig(filepath)
    plt.close()
    # plt.show()

def plot_statistic_guests(comand, column):
    global data
    filepath = os.path.join("plotting", "Комманда_{}   Период_{}.png". format(comand, column))
    data = hockey[["DataTime", column]].where(hockey["Guests"] == comand).dropna()
    plt.figure(figsize=(30,5))
    plt.plot(data["DataTime"], data[column])
    plt.savefig(filepath)
    plt.close()
    # plt.show()

def plot_statistic(comand):
    list_column_hosts = ["1PHosts","2PHosts","3PHosts","OTHosts","SSHosts","CountHosts"]
    for column in list_column_hosts:
        plot_statistic_hosts(comand, column)
    list_column_guests = ["1PGuests","2PGuests","3PGuests","OTGuests","SSGuests","CountGuests"]
    for column in list_column_guests:
        plot_statistic_hosts(comand, column)

list_name = hockey["Hosts"].unique()
for name in list_name:
    plot_statistic(name)
    print(name)
