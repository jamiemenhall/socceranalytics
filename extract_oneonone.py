from parser import html_to_pd
import pandas as pd
import numpy as np
from os import listdir, walk
from os.path import isfile, join

print([x for x in walk("~/football/pff_data")])

#print(open(join("/home/maxdunitz/football", "blah.txt")).read().decode("utf-8"))


base_directory = "/home/maxdunitz/football/pff_data/test"

html_files = [f for f in listdir(base_directory) if isfile(join(base_directory, f))]

print (html_files)

for f in html_files:
    max_size = 0
    max_idx = 0
    try:
        for i in range(10):
            pd = html_to_pd(open(join(base_directory,f), "rb").read().decode("utf-8"), i)
            if pd.shape[0]*pd.shape[1] > max_size:
                max_size = pd.shape[0]*pd.shape[1]
                max_idx = i
    except:
        pass
    print(html_to_pd(open(join(base_directory,f), "rb").read().decode("utf-8"),max_idx))


