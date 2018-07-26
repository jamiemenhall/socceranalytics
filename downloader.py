import os, time, random

cf = "mycookies.txt"

def create_wget_cmd(savefile, cookiefile, url):
    return "wget -O " + savefile + " --load-cookies " + cookiefile + " " + url

def save_data(urls, outfiles, prefix=None):
    if prefix is not None:
        outfiles = [prefix+"/"+o for o in outfiles]
    for url, save in zip(urls, outfiles):
        cmd = create_wget_cmd(save, cf, url)
        os.system(cmd)
        time.sleep(random.randint(6, 30))

#urls = []
#outfiles = []

## By Position ##
#for season in [str(i) for i in range(2013, 2018)]:
#    for pos in ["WR", "CB"]:
#        pos_season_75 = "https://www.profootballfocus.com/data/by_position.php?tab=by_position&season="+season+"&pos="+pos+"&runpass=pass&teamid=-1&numsnaps=75&numgames=1&conf=-1&yr=-1&wk=1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17"
#        urls.append(pos_season_75)
#        outfiles.append("season_"+season+"_pos_"+pos+"_numsnaps_75.html") #75 % numsnaps for season

#save_data(urls, outfiles, "season_by_pos")

urls = []
outfiles = []

for season in [str(i) for i in range(2013, 2018)]:
    for pos in ["WR", "CB"]:
        for week in [str(i) for i in range(1,18)]:
            runpass = "pass" if pos == "WR" else ""
            pos_week_25 = "https://www.profootballfocus.com/data/by_position.php?tab=by_position&season="+season+"&pos="+pos+"&runpass="+runpass+"&teamid=-1&numsnaps=25&numgames=1&conf=-1&yr=-1&wk="+week
            urls.append(pos_week_25)
            outfiles.append("week_"+week+"_season_"+season+"_pos_"+pos+"_numsnaps_25.html")

save_data(urls, outfiles, None)

urls = []
outfiles = []
for season in [str(i) for i in range(2013, 2018)]:
    for pos in ["wrs", "cbs"]:
        for week in [str(i) for i in range(1,18)]:
            slot_performance_weekly = "https://www.profootballfocus.com/data/signature.php?tab=signature&season="+season+"&pos="+pos+"&teamid=-1&filter=50&conf=-1&yr=-1&wk="+week
            urls.append(slot_performance_weekly)
            outfiles.append("slot_perf_week_"+week+"_season_"+season+"_pos_"+pos+"_numsnaps_50.html")

save_data(urls, outfiles, None)
