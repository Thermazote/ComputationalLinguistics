from bs4 import BeautifulSoup as BS
import os
import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import logging
import config


def load_page(driver, page_number):
    driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);",
                          driver.find_element(By.CLASS_NAME, "button-more"), "data-next-page", page_number)
    driver.find_element(By.CLASS_NAME, "button-more").click()


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

    # configure web driver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")      # use background mode
    driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)

    # iterate pages as many time as specified
    for pgNumber in range(1 + config.PAGE_OFFSET, config.PAGE_COUNT + config.PAGE_OFFSET):
        # get current page
        driver.get(config.URL)
        load_page(driver, pgNumber)
        logging.info("New page number " + str(pgNumber) + " was loaded")
        time.sleep(5)
        
        # get html code of page
        page = driver.page_source
        html = BS(page, "html.parser")
        
        # get articles data
        rawArticles = html.find_all("div", class_="new-article")
        articles = rawArticles[15:]     # get articles from loaded part of page
        for article in articles:
            # get article topic
            aName = article.find("h3").text
            aDate = article.find("span", class_="date-new").text
            aLink = config.URL + article.find("a", class_="detail-link").get("href")

            # get article content
            driver.get(aLink)
            articlePage = driver.page_source
            aHtml = BS(articlePage, "html.parser")
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
                articles_coll.update_one({"_id": document["_id"]},
                                         {"$set": {"replies_count": document["replies_count"]}})
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
            
    driver.quit()   # stop the driver
    logging.info("End of scanning. Next scan is in " + str(config.MINUTES_PERIOD) + " minutes.")
    time.sleep(config.MINUTES_PERIOD * 60)     # waiting for next period
