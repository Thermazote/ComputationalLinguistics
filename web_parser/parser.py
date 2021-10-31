import requests
from bs4 import BeautifulSoup as BS
import webbrowser as wb # for debuging
import sqlite3

    
siteURL = "https://v102.ru"
dbName = "db.sqlite"

# connect database
db = sqlite3.connect(dbName)
cursor = db.cursor()

# get html page
rq = requests.get(siteURL)
html = BS(rq.content, "html.parser")

# get article data
article = html.find("div", class_="new-article")
aName = article.find("h3").text
aDate = article.find("span", class_="date-new").text
aLink = siteURL + article.find("a", class_ ="detail-link").get("href")

#get article content
rqArticle = requests.get(aLink)
aHtml = BS(rqArticle.content, "html.parser")
aReplyCount = int(aHtml.find("span", class_="attr-comment").text)
contentSection = aHtml.find("div", class_="n-text")
aText = contentSection.text
playerSection = contentSection.find("div", class_="video-player")
aVideoLink = ""
if (playerSection is not None):
    aVideoLink = playerSection.get("href")

article_set = (aName, aDate, aLink, aText, aVideoLink, aReplyCount)
cursor.execute("INSERT INTO articles(name, date, link, text, video_link, replies_count) VALUES(?,?,?,?,?,?)", article_set)
db.commit()