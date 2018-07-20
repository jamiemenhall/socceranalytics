import csv
import cPickle as pickle

columns = {}
players = {}
header_skip = 0 
with open('data/PBP.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        if header_skip > 2:
            name = row[3]
            players[name] = row
        elif header_skip == 0:
            columns = dict([(c,i) for i,c in enumerate(row)])
            header_skip += 1
        elif header_skip == 1:
            print (row)
            header_skip += 1
f.close()

print(columns)
print (len(players))

with open("players_dict.pkl", "wb") as outfile:
    pickle.dump(players, outfile)
outfile.close()
