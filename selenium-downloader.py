import pickle
from selenium import webdriver
import time

with open("one-on-one-urls.pkl", "rb") as infile:
    urls, outfiles = pickle.load(infile)
infile.close()

browser = webdriver.Chrome()
browser.get("https://www.google.com")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)

for u, o in zip(urls, outfiles):
    browser.get(u)
    #innerHTML = browser.execute_script("return document.body.innerHTML")
    trucking = browser.find_element_by_xpath("//body").get_attribute('outerHTML')
    browser.get(u)
    trucking = browser.execute_script("return document.body.innerHTML")
    with open(o, "wb") as txt_out:
        txt_out.write(trucking.encode('utf-8'))
    txt_out.close()

