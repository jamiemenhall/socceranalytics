from parser import html_to_pd
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

html_files = [f for f in listdir("pff_data") if isfile(join("pff_data", f))]

for f in html_files:
    print(html_to_pd(open("pff_data/"+f, "rb").read().decode("utf-8"), 4))

