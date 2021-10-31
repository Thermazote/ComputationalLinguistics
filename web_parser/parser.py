from bs4 import BeautifulSoup as BS
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def loadNewPage(driver, pageNumber):
    driver.find_element(By.CLASS_NAME, "button-more").click()
    driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", driver.find_element(By.CLASS_NAME, "button-more"), "data-next-page", pageNumber)

siteURL = "https://v102.ru"
dbName = "db.sqlite"

# connect database
db = sqlite3.connect(dbName)
cursor = db.cursor()

# get html page using web driver
chrome_options = Options()
#chrome_options.add_argument("--headless")      # use background mode
driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
driver.get(siteURL)

# increase html page as many times as needed
COUNT = 5   # count of times to press "show more articles"
for it in range(0, COUNT):
    loadNewPage(driver, it + 3)     # it + 3 because default next page is 2 so we should specify next number
    #time.sleep(0.2)     # time to load articles, it'l be enough for 3 seconds 

# get source code of page
page = driver.page_source
html = BS(page, "html.parser")

# get articles data
articles = []
rawArticles = html.find_all("div", class_="new-article")
for article in rawArticles:
    # get article topic
    aName = article.find("h3").text
    aDate = article.find("span", class_="date-new").text
    aLink = siteURL + article.find("a", class_="detail-link").get("href")

    # get article content
    driver.get(aLink)
    # time.sleep(0.1)
    articlePage = driver.page_source
    aHtml = BS(articlePage, "html.parser")
    contentSection = aHtml.find("div", class_="n-text")
    aText = contentSection.text
    playerSection = contentSection.find("div", class_="video-player")
    aVideoLink = ""
    if (playerSection is not None):
        aVideoLink = playerSection.find("iframe").get("src")
    aReplyCount = aHtml.find("span", class_="attr-comment").text

    # create dataset for current article and send it to database
    aDataSet = (aName, aDate, aLink, aText, aVideoLink, aReplyCount)
    cursor.execute("INSERT INTO articles(name, date, link, text, video_link, replies_count) VALUES(?,?,?,?,?,?)", aDataSet)
    db.commit()

driver.quit()