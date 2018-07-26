import pandas as pd
import numpy as np
import _pickle as pickle

gid = 0
offt = 3
dwn = 15
ytg = 16
ydg = 19
psr = 30
trg = 34



player_df = pd.read_csv("amc_data/PBP.csv")

relevant_cols = player_df[['gid', 'off', 'dwn', 'ytg', 'yfog', 'yds', 'psr', 'trg']]

print(relevant_cols.shape)

with open("pbp.pkl", "wb") as outfile:
    pickle.dump(relevant_cols, outfile, protocol=2)
outfile.close()

