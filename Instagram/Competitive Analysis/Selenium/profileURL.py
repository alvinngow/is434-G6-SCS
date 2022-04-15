# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.options import Options
# from instascrape import Profile, scrape_posts

# # Creating our webdriver
# webdriver = Chrome(executable_path='./chromedriver_win32/chromedriver')
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')

# # Scraping SCS's profile
# SESSIONID = '52429546524%3AySspiL5CQgYPLO%3A1'
# # https://www.whatismybrowser.com/detect/what-is-my-user-agent/
# headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36", "cookie": f"sessionid={SESSIONID};"}
# scs = Profile("sgchildrensoc")
# scs.scrape(headers=headers)

# # Scraping the posts
# posts = scs.get_posts(webdriver=webdriver, login_first=True)
# scraped, unscraped = scrape_posts(posts, silent=False, headers=headers, pause=10)


# https://dev.to/chrisgreening/scraping-every-post-on-an-instagram-profile-with-less-than-10-lines-of-python-1n8b

# --------------  testing script to see chromedriver works --------------
# import time

# from selenium import webdriver

# from selenium.webdriver.chrome.service import Service

# service = Service('./chromedriver_win32/chromedriver')

# service.start()

# driver = webdriver.Remote(service.service_url)

# driver.get('http://www.google.com/');

# time.sleep(5) # Let the user actually see something!

# driver.quit()


# https://stackoverflow.com/questions/69875125/find-element-by-commands-are-deprecated-in-selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, urllib.request
import requests

PATH = r"./chromedriver_win32/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("https://www.instagram.com/")

#login
time.sleep(5)
# username = driver.find_element_by_css_selector("input[name='username']")
# password = driver.find_element_by_css_selector("input[name='password']")

username = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
password = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
username.clear()
password.clear()
username.send_keys("smusa2022.demo@gmail.com")
password.send_keys("password2022")
# login = driver.find_element_by_css_selector("button[type='submit']").click()
login = driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()

#save your login info?
time.sleep(10)
notnow = driver.find_element(By.XPATH,"//button[contains(text(), 'Not Now')]").click()
# notnow = driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
#turn on notif
time.sleep(10)
notnow2 = driver.find_element(By.XPATH,"//button[contains(text(), 'Not Now')]").click()
# notnow2 = driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()

#searchbox
time.sleep(5)
# searchbox = driver.find_element_by_css_selector("input[placeholder='Search']")
searchbox = driver.find_element(By.CSS_SELECTOR,"input[placeholder='Search']")
searchbox.clear()
searchbox.send_keys("sgchildrensoc")
time.sleep(5)
searchbox.send_keys(Keys.ENTER)
time.sleep(5)
searchbox.send_keys(Keys.ENTER)


posts = []
#scroll
scrolldown = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
match=False
while(match==False):
    last_count = scrolldown
    time.sleep(3)

    # links = driver.find_elements_by_tag_name('a')
    links = driver.find_elements(By.TAG_NAME, 'a')
    for link in links:
        post = link.get_attribute('href')
        if '/p/' in post and post not in posts:
            posts.append(post)

    scrolldown = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    if last_count==scrolldown:
        match=True

time.sleep(3)
#posts
with open("output.txt", "w") as txt_file:
    for line in posts:
        txt_file.write(line + "\n")
# print(posts)
print("Number of posts:", len(posts))


# #get videos and images
# download_url = ''
# for post in posts:	
# 	driver.get(post)
# 	shortcode = driver.current_url.split("/")[-2]
# 	time.sleep(7)
# 	if driver.find_element_by_css_selector("img[style='object-fit: cover;']") is not None:
# 		download_url = driver.find_element_by_css_selector("img[style='object-fit: cover;']").get_attribute('src')
# 		urllib.request.urlretrieve( download_url, '{}.jpg'.format(shortcode))
# 	else:
# 		download_url = driver.find_element_by_css_selector("video[type='video/mp4']").get_attribute('src')
# 		urllib.request.urlretrieve( download_url, '{}.mp4'.format(shortcode))
# 	time.sleep(5)