import os
from bs4 import BeautifulSoup as BS
import pymongo
import requests
import time
import logging
import config

logging.basicConfig(filename="parser.log", level=logging.INFO, format='%(asctime)s %(message)s')  # configure logger

while True:
    logging.info("Start scanning.")
    
    # connect database
    mongo_username = os.getenv('MONGO_USERNAME')
    mongo_password = os.getenv('MONGO_PASSWORD')
    conn_str = "mongodb+srv://" + mongo_username + ":" + mongo_password + "@cluster0.8ngl3.mongodb.net"
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    db = client['articles_analysis']
    articles_coll = db['articles']
    
    # get freshArtLink
    mainRequest = requests.get(config.URL)
    mainHtml = BS(mainRequest.content, "html.parser")
    freshArticle = mainHtml.find("div", class_="new-article")
    freshArticleId = int(freshArticle.find("a", class_="detail-link").get("href")[6:-5])

    # get as many articles as specified
    articleId = freshArticleId
    existingArticleCount = 0
    while existingArticleCount < config.ARTICLES_COUNT:
        # get article page
        aLink = config.URL + "news/" + str(articleId) + ".html"
        aRq = requests.get(aLink)
        
        # decrement article id for next iteration
        articleId -= 1
        
        # check if article with this id exists (if article doesn't exist it'l be redirected to main page of site)
        aHtml = BS(aRq.content, "html.parser")
        if aRq.url != config.URL:
            existingArticleCount += 1
            logging.info("Article exists.")
        else:
            logging.info("Redirected. Article does not exist.")
            continue
        
        # get articles data
        aName = aHtml.find("h1", itemprop = "headline").text
        aDateRaw = aHtml.find("span", class_="date-new").text.split()
        aDate = aDateRaw[0] + " " + aDateRaw[1]
        contentSection = aHtml.find("div", class_="n-text")
        aText = contentSection.text
        playerSection = contentSection.find("div", class_="video-player")
        aVideoLink = ""
        if playerSection is not None:
            aVideoLink = playerSection.find("iframe").get("src")
        aRepliesCount = aHtml.find("span", class_="attr-comment").text
        
        # check if current article is on the database
        document = articles_coll.find_one({"name": aName, "date": aDate, "link": aLink})
        if document:
            # update replies count of EXISTING article
            articles_coll.update_one({"_id": document["_id"]}, {"$set": {"replies_count": document["replies_count"]}})
            logging.info("Article with ID = " + str(document["_id"]) + " was updated in database.")
        else:
            # add to database NEW article
            articles_coll.insert_one(
                {
                    "name": aName,
                    "date": aDate,
                    "link": aLink,
                    "text": aText,
                    "video_link": aVideoLink,
                    "replies_count": aRepliesCount
                }
            )
            logging.info("New article was added to database.")

    logging.info("End of scanning. Next scan is in " + str(config.MINUTES_PERIOD) + " minutes.")
    time.sleep(config.MINUTES_PERIOD * 60)     # waiting for next period
