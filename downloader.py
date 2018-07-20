import os, time, random

cf = "mycookies.txt"

def create_wget_cmd(savefile, cookiefile, url):
    return "wget -O " + savefile + " --load-cookies " + cookiefile + " " + url

urls = []
outfiles = []

## By Position ##
for season in [str(i) for i in range(2013, 2018)]:
    for pos in ["WR", "CB"]:
        pos_season_75 = "https://www.profootballfocus.com/data/by_position.php?tab=by_position&season="+season+"&pos="+pos+"&runpass=pass&teamid=-1&numsnaps=75&numgames=1&conf=-1&yr=-1&wk=1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17"
        urls.append(pos_season_75)
        outfiles.append("season_"+season+"_pos_"+pos+"_numsnaps_75.html") #75 % numsnaps for season

#for year in years:
#    for week in weeks:
#        for stat in stats:


outfiles = ["pff_data/"+o for o in outfiles]

for url, save in zip(urls, outfiles):
    cmd = create_wget_cmd(save, cf, url)
    os.system(cmd)
    time.sleep(random.randint(60, 300))


