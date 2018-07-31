import pickle
from selenium import webdriver
import time
browser = webdriver.Chrome()
browser.get("https://www.google.com")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)
browser.get("https://www.profootballfocus.com/data/gstats.php?tab=by_week&season=2015&gameid=3406&teamid=19&stats=v&playerid=")
time.sleep(10)
#innerHTML = browser.execute_script("return document.body.innerHTML")
trucking = browser.find_element_by_xpath("//body").get_attribute('outerHTML')
browser.get("https://www.profootballfocus.com/data/gstats.php?tab=by_week&season=2015&gameid=3406&teamid=19&stats=v&playerid=")
trucking = browser.page_source
#print(partyid)
#print(innerHTML)
with open("selenium_html.html", "w") as txt_out:
    txt_out.write(trucking.encode('utf-8'))
txt_out.close()

