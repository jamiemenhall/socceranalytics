#python 2
import csv
import cPickle as pickle

players = {}

header_skip = 0 
with open('amc_data/PLAYER.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        if header_skip == 1:
            pid = row[0]
            fname = row[1]
            lname = row[2]
            players[pid] = [fname, lname]
        elif header_skip == 0:
            print([(c,i) for i,c in enumerate(row)])
            header_skip += 1
f.close()

with open("players.pkl", "wb") as outfile:
    pickle.dump(games, outfile)
outfile.close()
