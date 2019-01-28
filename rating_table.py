import re
import string
import datetime
from datetime import datetime
import pickle
import os
import pandas as pd
import swifter
from multiprocessing import Pool
import pandas as pd

HOCKEY_PATH = os.path.join("datasets", "hockey")


def score(row: pd.Series) -> str:
    count_guests = row["CountGuests"]
    count_hosts = row["CountHosts"]
    over_hosts = row["OverHosts"]
    over_guests = row["OverGuests"]
    row['ScoreHosts'] = 0
    row['ScoreGuests'] = 0
    if count_hosts > count_guests:
        row['ScoreHosts'] = 2
        row['ScoreGuests'] = 0
    else:
        row['ScoreHosts'] = 0
        row['ScoreGuests'] = 2
    if over_hosts == 1:
        row['ScoreGuests'] = 1
    elif over_guests == 1:
        row['ScoreHosts'] = 1
    return row



def load_hockey_data(hockey_path=HOCKEY_PATH):
    csv_path = os.path.join(hockey_path, "hockey_2019_01_21.csv")
    return pd.read_csv(csv_path)

hockey = load_hockey_data()

hockey = hockey.apply(score, axis=1)
print(hockey.head(6))

hockey.to_csv(os.path.join("datasets", "hockey", "hockey_add_score_2019_01_28.csv"), sep=',', encoding='utf-8', index=False)