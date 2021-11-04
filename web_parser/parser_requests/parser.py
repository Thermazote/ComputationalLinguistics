from bs4 import BeautifulSoup as BS
import sqlite3
import requests
import time
import logging
import config

logging.basicConfig(filename="parser.log", level=logging.INFO, format='%(asctime)s %(message)s')  # configure logger

while(True):
    logging.info("Start scanning.")
    
    # connect database
    db = sqlite3.connect(config.DB_PATH)
    cursor = db.cursor()
    
    # get freshArtLink
    mainRequest = requests.get(config.URL)
    mainHtml = BS(mainRequest.content, "html.parser")
    freshArticle = mainHtml.find("div", class_="new-article")
    freshArticleId = int(freshArticle.find("a", class_="detail-link").get("href")[6:-5])

    # get as many articles as specified
    articleId = freshArticleId
    existingArticleCount = 0
    while (existingArticleCount < config.ARTICLES_COUNT):
        # get article page
        aLink = config.URL + "news/" + str(articleId) + ".html"
        aRq = requests.get(aLink)
        
        # decrement article id for next iteration
        articleId -= 1
        
        # check if article with this id exists (if article doesn't exist it'l be redirected to main page of site)
        aHtml = BS(aRq.content, "html.parser")
        if (aRq.url != (config.URL)):
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
        if (playerSection is not None):
            aVideoLink = playerSection.find("iframe").get("src")
        aRepliesCount = aHtml.find("span", class_="attr-comment").text
            
        # create dataset and check set for current article
        aDataSet = (aName, aDate, aLink, aText, aVideoLink, aRepliesCount)
        checkSet = (aName, aDate, aLink)
        
        # check if current article is on the database
        cursor.execute("SELECT * FROM articles WHERE name = ? AND date = ? AND link = ?", checkSet)
        records = cursor.fetchall()
        if (records):
            # update replies count of EXISTING article
            updatedRepliesCount = records[0][6]
            articleID = records[0][0]
            updateSet = (updatedRepliesCount, articleID)
            cursor.execute("UPDATE articles SET replies_count = ? WHERE id = ?", updateSet)
            logging.info("Article with ID = " + str(articleID) + " was updated in database.")
        else:
            # add to database NEW article
            cursor.execute("INSERT INTO articles(name, date, link, text, video_link, replies_count) VALUES(?,?,?,?,?,?)", aDataSet)
            logging.info("New article was added to database.")
        db.commit()
        

        
    db.close()      # disconnect database
    logging.info("End of scanning. Next scan is in " + str(config.MINUTES_PERIOD) + " minutes.")
    time.sleep(config.MINUTES_PERIOD * 60)     # waiting for next period