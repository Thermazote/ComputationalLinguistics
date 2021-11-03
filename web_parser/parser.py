from bs4 import BeautifulSoup as BS
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import logging
import config


def loadNewPage(driver, pageNumber):
    driver.find_element(By.CLASS_NAME, "button-more").click()
    driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", driver.find_element(By.CLASS_NAME, "button-more"), "data-next-page", pageNumber)

siteURL = config.URL
dbPath = config.DB_PATH
pagesCount = config.PG_COUNT            # count of times to press "show more articles"
minutesPeriod = config.MINUTES_PERIOD   # frequency of parsing site - period in minutes

logging.basicConfig(filename="parser.log", level=logging.INFO, format='%(asctime)s %(message)s')  # configure logger

while(True):
    # connect database
    db = sqlite3.connect(dbPath)
    cursor = db.cursor()

    # get html page using web driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")      # use background mode
    driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
    driver.get(siteURL)
    logging.info("Start scanning.")
    
    # increase html page as many times as needed 
    for it in range(0, pagesCount):
        loadNewPage(driver, it + 3)     # it + 3 because default next page is 2 so we should specify next number
    logging.info("Uploaded " + str(pagesCount) + " pages additionally.")
    
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
        articlePage = driver.page_source
        aHtml = BS(articlePage, "html.parser")
        contentSection = aHtml.find("div", class_="n-text")
        aText = contentSection.text
        playerSection = contentSection.find("div", class_="video-player")
        aVideoLink = ""
        if (playerSection is not None):
            aVideoLink = playerSection.find("iframe").get("src")
        aReplyCount = aHtml.find("span", class_="attr-comment").text

        # create dataset and check set for current article
        aDataSet = (aName, aDate, aLink, aText, aVideoLink, aReplyCount)
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
    driver.quit()   # stop the driver
    db.close()      # disconnect database
    logging.info("End of scanning. Next scan is in " + str(minutesPeriod) + " minutes.")
    time.sleep(minutesPeriod * 60)     # waiting for next period