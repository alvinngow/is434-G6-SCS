from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, urllib.request
import requests
import pandas as pd
import copy
import json


# Get posts
PATH_CSV = "./Instagram_Posts_Extractor/result.csv"
df = pd.read_csv(PATH_CSV)
posts = df[df["type"] == "Photo"]["postUrl"].unique().tolist()
# print(posts[:5])

PATH = r"../chromedriver_win32/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("https://www.instagram.com/")

#login
time.sleep(5)
username = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
password = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
username.clear()
password.clear()
# username.send_keys("smusa2022.demo@gmail.com")
username.send_keys("ulkeuyposttbtiomfn@bvhrk.com")
password.send_keys("ulkeuyposttbtiomfn@")
login = driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()

#save your login info?
time.sleep(10)
notnow = driver.find_element(By.XPATH,"//button[contains(text(), 'Not Now')]").click()
#turn on notif
time.sleep(10)
notnow2 = driver.find_element(By.XPATH,"//button[contains(text(), 'Not Now')]").click()

#searchbox
time.sleep(5)

# If there is error, load again
# likeArray = []
FILE_URL = "likes_MSF.json"
with open(FILE_URL) as f:
    likeArray = json.load(f)
post_array = list(map(lambda x: x["post"], likeArray))


for post in posts:
    if post in post_array:
        continue

    driver.get(post)
    time.sleep(5)

    # Click like button
    likes_button = driver.find_element(By.CSS_SELECTOR,"div._7UhW9.xLCgt.qyrsm.KV-D4.fDxYl.T0kll").click()
    time.sleep(2)

    users = []
    elements = driver.find_elements(By.CSS_SELECTOR,"div.qF0y9.Igw0E.rBNOH.eGOV_.ybXk5._4EzTm.XfCBB.HVWg4")

    while True:
        time.sleep(2)

        spans = driver.find_elements(By.CSS_SELECTOR,"span._7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll")
        array_length = len(users)
        for span in spans:
            if span.text not in users:
                users.append(span.text)

        if array_length == len(users):
            break

        for element in elements:
            driver.execute_script("arguments[0].scrollIntoView(true);", element);
        time.sleep(2)

        prev_elements = elements
        elements = driver.find_elements(By.CSS_SELECTOR,"div.qF0y9.Igw0E.rBNOH.eGOV_.ybXk5._4EzTm.XfCBB.HVWg4")
        elements = list(filter(lambda x: x not in prev_elements, elements))

    likeArray.append({
        "post": post,
        "users" : users
    })

    with open(FILE_URL, 'w') as fp:
        json.dump(likeArray, fp, indent=4)