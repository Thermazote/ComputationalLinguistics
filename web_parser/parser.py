import requests
from bs4 import BeautifulSoup as BS
import webbrowser as wb # for debuging


siteURL = "https://v102.ru"

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
aText = aHtml.find("div", class_="n-text").text
aReplyCount = int(aHtml.find("span", class_="attr-comment").text)
aVideoLink = ""
try:
    aVideoLink = aHtml.find("div", class_="n-text").find("div", class_="video-player").get("href")
except:
    aVideoLink = "None"

print("Name: " + aName)
print("Date: " + aDate)
print("Link: " + aLink)
print("Text: " + aText)
print("Reply count: " + str(aReplyCount))
print("Video link: " + aVideoLink)