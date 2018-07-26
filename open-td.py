import _pickle as pickle

with open("thirddowns.pkl", "rb") as infile:
    td = pickle.load(infile)
infile.close()

print(td)

for k, v in td.items():
    print(k, v)
    print([type(k) for k in v.keys()])
