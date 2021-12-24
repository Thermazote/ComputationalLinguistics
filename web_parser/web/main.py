from flask import Flask
from flask import request
import pymongo
import os
import datetime


app = Flask(__name__)

row_count = 10

# connect database
mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')
conn_str = "mongodb+srv://" + mongo_username + ":" + mongo_password + "@cluster0.8ngl3.mongodb.net"
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
db = client['articles_analysis']
articles_coll = db['articles']


@app.route('/')
def index():
    if request.method == 'GET':
        documents = articles_coll.find().sort("date", pymongo.DESCENDING)
        table = '''
            <table border="2" style="width: 100%">
                <tr>
                    <th>Title</th>
                    <th>Date</th>
                    <th>Link</th>
                    <th>Video</th>
                    <th>Replies count</th>
                    <th>Facts</th>
                    <th>Sentiment</th>
                </tr>'''
                
        for i in range(row_count):
            name = '<td>' + documents[i]['name'] + '</td>'
            date = '<td>' + str(documents[i]['date']) + '</td>'
            link = '<td>' + documents[i]['link'] + '</td>'
            video_link = '<td>' + documents[i]['video_link'] + '</td>'
            replies_count = '<td>' + str(documents[i]['replies_count']) + '</td>'
            facts = ''
            sentiment = ''
            try:
                facts += '<td>' + documents[i]['facts'] + '</td>'
                sentiment += '<td>' + documents[i]['sentiment'] + '</td>'
            except KeyError:
                facts += '<td></td>'
                sentiment += '<td></td>'
            table += '<tr>' + name + date + link  + video_link + replies_count + facts + sentiment + '</tr>'
        table += '</table>'
        html = '''
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="utf-8">
                    <title>Article analysis</title>
                </head>
                <body>
                    <h1 align="center"><a href="https://v102.ru">v102.ru</a> ARTICLES ANALYSIS</h1>
                    %s
                </body>
            </html>''' % table
        return html

if __name__ == "__main__":
    app.run()