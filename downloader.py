import os, time, random

cf = "mycookies.txt"

def create_wget_cmd(savefile, cookiefile, url):
    return "wget -O " + savefile + " --load-cookies " + cookiefile + " " + url

urls = []
outfiles = []

for year in years:
    for week in weeks:
        for stat in stats:


for url, save in zip(urls, outfiles):
    cmd = create_wget_cmd(save, cf, url)
    os.command(cmd)
    time.sleep(random.randint(60, 300))


