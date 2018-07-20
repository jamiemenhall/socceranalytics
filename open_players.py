import cPickle as pickle

with open("players_dict.pkl", "rb") as infile:
    players = pickle.load(infile)
print len(players)
