import csv

FILENAME = "users.csv"
with open(FILENAME, "a") as file:
    writer = csv.writer(file)
    i = 0
    list_hat = "Дата матча", "Хозяева", "Время забитых шайб(Х)", "Счет в матче", "Гости", "Время забитых шайб(Г)"
    writer.writerow(lisr)