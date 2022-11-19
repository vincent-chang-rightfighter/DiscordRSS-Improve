import feedparser
import requests
import sqlite3
import time
from discord import Webhook, RequestsWebhookAdapter, Embed, Colour
from datetime import datetime, timezone, timedelta

webHookUrl = ['https://discord.com/api/webhooks/...AccountidA',
              'https://discord.com/api/webhooks/...AccountidB']

PTTRssUrl = ['https://www.ptt.cc/atom/PC_Shopping.xml',
             'https://www.ptt.cc/atom/HardwareSale.xml']


def req_webhook(webHookUrl: str, DATA: dict, URL: str):
    try:
        time.sleep(5)
        SendToDC = requests.post(
            webHookUrl, json=DATA)
        if 200 <= SendToDC.status_code < 300:
            print(
                f"Send Webhook {str(URL)}\nStatus:{SendToDC.status_code}")
        else:
            print(
                f"Send Webhook {str(URL)}\nStatus:{SendToDC.status_code}, response:\n{SendToDC.json()}")
    except Exception as e:
        print(e)


def main(Webhookurl: str, RssUrl: str):
    con = sqlite3.connect('rss.db')
    cur = con.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Stuff(url TEXT PRIMARY KEY NOT NULL)''')
    data = feedparser.parse(RssUrl)
    Provider = data.feed.title
    for i in data.entries:
        Title = i.title
        hyperLink = i.link
        description = i.summary
        Author = i.author

        exist = con.execute(
            "SELECT * FROM Stuff WHERE url = ?", ([hyperLink])).fetchone()
        if exist is None:
            # print(shorTcode)
            cur.execute(
                "INSERT INTO Stuff VALUES(?)", [hyperLink])
            con.commit()
            time_now = datetime.now(timezone(timedelta(hours=+8))).isoformat()
            embed = {
                "description":  description[5:len(description)-7].replace("*", "\*"),
                "title": Title,
                "timestamp": time_now,
                "color": 0x546e7a,
                "author": {
                    "name": Provider+" ( "+Author+" )",
                },
                "footer": {
                    "text": "Powered by vincent-chang-rightfighter/DiscordRSS-Improve",
                    "icon_url": "https://raw.githubusercontent.com/vincent-chang-rightfighter/DiscordWebhook-InstagramUrl/main/icon.png"
                },
            }
            data = {"content": f"{Title}\n{hyperLink}",
                    "embeds": [embed], }
            req_webhook(Webhookurl, data, hyperLink)

        else:
            print("Yep exists")
    con.close()


if __name__ == "__main__":
    # main()
    for i in range(len(PTTRssUrl)):
        main(webHookUrl[i], PTTRssUrl[i])
