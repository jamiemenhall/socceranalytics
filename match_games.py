#python 2
import csv
import cPickle as pickle

games = {}

header_skip = 0 
with open('amc_data/GAME.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        if header_skip == 1:
            gid = row[0]
            seas = row[1]
            wk = row[2]
            visit = row[4]
            home = row[5]
            games[gid] = [seas, wk, visit, home]
        elif header_skip == 0:
            print([(c,i) for i,c in enumerate(row)])
            header_skip += 1
f.close()

with open("games.pkl", "wb") as outfile:
    pickle.dump(games, outfile)
outfile.close()
