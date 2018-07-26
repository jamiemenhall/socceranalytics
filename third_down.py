import _pickle as pickle
import numpy as np

third_downs = {}

with open("pbp.pkl", "rb") as infile:
    pbp = pickle.load(infile)
infile.close()

with open("games.pkl", "rb") as infile:
    games = pickle.load(infile)
infile.close()

for index, row in pbp.iterrows():
    gid = str(row["gid"])
    off = str(row["off"])
    season, week, visit, home = games[gid]
    if row["dwn"] == 3 and not (type(row["trg"]) == type("hi")):
        key = (off, season, week)
        old_dict = third_downs.get(key,{})
        
        target = row["trg"]
        old_dict[target] = old_dict.get(target, 0) + 1
        third_downs[key] = old_dict

with open("thirddowns.pkl", "wb") as outfile:
    games = pickle.dump(third_downs, outfile, protocol=2)
outfile.close()
