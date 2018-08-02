from selenium import webdriver
import time
import pickle

browser = webdriver.Chrome()
url = "https://www.profootballfocus.com/amember/login?amember_redirect_url=%2Fauth%2Ftokenize%3Freturn_url%3Dhttps%3A%2F%2Fwww.profootballfocus.com%2Fauth_callback"
#innerHTML = browser.execute_script("return document.body.innerHTML")
#print(innerHTML)a
browser.get(url)
time.sleep(150)
pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
