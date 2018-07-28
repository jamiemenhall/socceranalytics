import os, time, random
from parser import html_to_pd
import requests

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


#TEAM NAMES, ALPHABETICAL BY CITY:
team_names = '''Cardinals
Falcons
Ravens
Bills
Panthers
Bears
Bengals
Browns
Cowboys
Broncos
Lions
Packers
Texans
Colts
Jaguars
Chiefs
Chargers
Rams
Dolphins
Vikings
Patriots
Saints
Giants
Jets
Raiders
Eagles
Steelers
49ers
Seahawks
Buccaneers
Titans
Redskins'''.split()

team_ids = dict([(n,i+1) for i, n in enumerate(team_names)])

seasons = [str(i) for i in range(2015,2018)]
weeks = [str(i) for i in range(1,18)]

matchups = {}

# import schedules
for year in seasons:
    url = "https://www.pro-football-reference.com/years/"+year+"/games.htm"
    content = requests.get(url).content
    schedule = html_to_pd(content.decode("utf-8"),0)
    print(schedule)
    print(schedule)
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
stat="v"
start_gids = {"2015":3406, "2016":4094, "2017":7922}
for year in seasons:
    start_gid = start_gids[year]
    for week in weeks:
        for matchup in matchups[(year, week)]:
            winner_id, loser_id = matchup
            for gid in range(start_gid, start_gid + len(matchups[(year, week)])):
                url1="https://www.profootballfocus.com/data/gstats.php?tab=by_week&season="+year+"&gameid="+str(gid)+"&teamid="+str(winner_id)+"&stats="+stat
                url2="https://www.profootballfocus.com/data/gstats.php?tab=by_week&season="+year+"&gameid="+str(gid)+"&teamid="+str(loser_id)+"&stats="+stat
                urls.append(url1)
                urls.append(url2)
                outfiles.append("week-by-week-stat-"+stat+"-gid-"+str(gid)+"-winnerteamid-"+str(winner_id)+".html")
                outfiles.append("week-by-week-stat-"+stat+"-gid-"+str(gid)+"-loserteamid-"+str(loser_id)+".html")
        start_gid = start_gid + len(matchups[(year, week)])+1


save_data(urls, outfiles, None)
