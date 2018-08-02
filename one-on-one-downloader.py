import os, time, random
from parser import html_to_pd
import requests
import pickle

cf = "~/football/mycookies.txt"

def create_wget_cmd(savefile, cookiefile, url):
    #cmd =  'phantomjs --cookies-file='+cookiefile+' get.js "' + url + '" > ' + savefile
    #print(cmd)
    #return cmd
    return "wget -O " + savefile + " --load-cookies " + cookiefile + " " + url

def save_data(urls, outfiles, prefix=None):
    if prefix is not None:
        outfiles = [prefix+"/"+o for o in outfiles]
    for url, save in zip(urls, outfiles):
        cmd = create_wget_cmd(save, cf, url)
        os.system(cmd)
        time.sleep(random.randint(6, 30))


#TEAM NAMES, ALPHABETICAL BY CITY:
team_ids = {
        "Cardinals": 1,
        "Falcons": 2,
        "Ravens": 3,
        "Bills": 4,
        "Panthers": 5,
        "Bears": 6,
        "Bengals": 7,
        "Browns": 8,
        "Cowboys": 9,
        "Broncos": 10,
        "Lions": 11,
        "Packers": 12,
        "Texans": 13,
        "Colts": 14,
        "Jaguars": 15,
        "Chiefs": 16,
        "Chargers": 27,
        "Rams": 26,
        "Dolphins": 17,
        "Vikings": 18,
        "Patriots": 19,
        "Saints": 20,
        "Giants": 21,
        "Jets": 22,
        "Raiders": 23,
        "Eagles": 24,
        "Steelers": 25,
        "49ers": 28,
        "Seahawks": 29,
        "Buccaneers": 30,
        "Titans": 31,
        "Redskins": 32}

#team_ids = dict([(n,i+1) for i, n in enumerate(team_names)])

seasons = [str(i) for i in range(2012,2018)]
weeks = [str(i) for i in range(1,18)]

matchups = {}

# import schedules
for year in seasons:
    url = "https://www.pro-football-reference.com/years/"+year+"/games.htm"
    content = requests.get(url).content
    schedule = html_to_pd(content.decode("utf-8"),0)
    for index, row in schedule.iterrows():
        week = row[0]
        if week in weeks:
            team1 = row[4]
            team2 = row[6]
            team1_id = team_ids[team1.split()[-1]]
            team2_id = team_ids[team2.split()[-1]]
            matchups[(year, week)] = matchups.get((year, week), []) + [(team1_id, team2_id)]
            print(team1, team2)

urls = []
outfiles = []
stat="o"
start_gids = {"2012": 2390, "2013": 2742, "2014":3074, "2015":3406, "2016":4094, "2017":7922}
for year in seasons:
    start_gid = start_gids[year]
    for week in weeks:
        for matchup in matchups[(year, week)]:
            winner_id, loser_id = matchup
            for gid in range(start_gid, start_gid + len(matchups[(year, week)])):
                for stat in ["d", "o", "c", "v"]:
                    url1="https://www.profootballfocus.com/data/gstats.php?tab=by_week&season="+year+"&gameid="+str(gid)+"&teamid="+str(winner_id)+"&stats="+stat+"&player_id="
                    url2="https://www.profootballfocus.com/data/gstats.php?tab=by_week&season="+year+"&gameid="+str(gid)+"&teamid="+str(loser_id)+"&stats="+stat+"&player_id="
                    urls.append(url1)
                    urls.append(url2)
                    outfiles.append("one-on-one-season-"+year+"-week-"+week+"-stat-"+stat+"-gid-"+str(gid)+"-winnerteamid-"+str(winner_id)+".html")
                    outfiles.append("one-on-one-season-"+year+"-week-"+week+"-stat-"+stat+"-gid-"+str(gid)+"-loserteamid-"+str(loser_id)+".html")
        start_gid = start_gid + len(matchups[(year, week)])+1

#urls = ["https://www.profootballfocus.com/data/gstats.php?tab=by_team&season=2015&gameid=3406&teamid=25&stats=v&playerid="]
#urls = ["https://www.profootballfocus.com/data/by_week.php?tab=by_week&season=2015&wk=1"]
#outfiles = ["test.html"]
#save_data(urls, outfiles, None)

with open("one-on-one-urls.pkl", "wb") as outfile:
    pickle.dump((urls, outfiles), outfile)
outfile.close()

