import requests
from bs4 import BeautifulSoup as BS
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time    
    
siteURL = "https://v102.ru"
dbName = "db.sqlite"

# connect database
db = sqlite3.connect(dbName)
cursor = db.cursor()

# get html page using webdriver
chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
driver.get(siteURL)
#time.sleep(0.1)
page = driver.page_source
html = BS(page, "html.parser")

# get articles data
articles = []
rawArticles = html.find_all("div", class_="new-article")
for article in rawArticles:
    # get article topic
    aName = article.find("h3").text
    aDate = article.find("span", class_="date-new").text
    aLink = siteURL + article.find("a", class_ ="detail-link").get("href")

    # get article content
    driver.get(aLink)
    #time.sleep(0.1)
    articlePage = driver.page_source
    aHtml = BS(articlePage, "html.parser")
    contentSection = aHtml.find("div", class_="n-text")
    aText = contentSection.text
    playerSection = contentSection.find("div", class_="video-player")
    aVideoLink = ""
    if (playerSection is not None):
        aVideoLink = playerSection.find("iframe").get("src")
    aReplyCount = aHtml.find("span", class_="attr-comment").text
    
    # create dataset for current article
    aDataSet = (aName, aDate, aLink, aText, aVideoLink, aReplyCount)
    articles.append(aDataSet)

# send articles to database    
for article in articles:
    cursor.execute("INSERT INTO articles(name, date, link, text, video_link, replies_count) VALUES(?,?,?,?,?,?)", article)
db.commit()