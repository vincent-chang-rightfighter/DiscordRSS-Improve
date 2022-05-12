import feedparser
import sqlite3
from discord import Webhook, RequestsWebhookAdapter, Embed, Colour
from datetime import datetime, timezone, timedelta


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}

webHookUrl = ['https://discord.com/api/webhooks/...AccountidA',
              'https://discord.com/api/webhooks/...AccountidB']

PTTRssUrl = ['https://www.ptt.cc/atom/PC_Shopping.xml',
             'https://www.ptt.cc/atom/HardwareSale.xml']


def build_webhook(Webhookurl):
    webhook = Webhook.from_url(Webhookurl, adapter=RequestsWebhookAdapter())
    return webhook


def main(Webhookurl: str, RssUrl: str):
    con = sqlite3.connect('rss.db')
    cur = con.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Stuff(url TEXT PRIMARY KEY NOT NULL)''')
    webhook = build_webhook(Webhookurl)
    data = feedparser.parse(RssUrl)

    Title = data.entries[0].title
    hyperLink = data.entries[0].link
    description = data.entries[0].summary
    Author = data.entries[0].author
    Provider = data.feed.title

    exist = con.execute(
        "SELECT * FROM Stuff WHERE url = ?", ([hyperLink])).fetchone()
    if exist is None:
        # print(shorTcode)
        cur.execute(
            "INSERT INTO Stuff VALUES(?)", [hyperLink])
        con.commit()
        print("Not exist. Send webhook\n"+str(hyperLink))
        embed = Embed()
        embed.title = Title
        embed.colour = Colour.dark_gray()
        embed.description = description[5:len(description)-7]
        embed.timestamp = datetime.now(timezone(timedelta(hours=+8)))
        embed.set_author(name=Provider+" ( "+Author+" )")
        embed.set_footer(text='Powered by vincent-chang-rightfighter/DiscordRSS-Improve',
                         icon_url='https://raw.githubusercontent.com/vincent-chang-rightfighter/DiscordWebhook-InstagramUrl/main/icon.png')
        webhook.send(
            content=f"{Title}\n{hyperLink}", embed=embed)
    else:
        print("Yep exists")
    con.close()


if __name__ == "__main__":
    # main()
    for i in range(len(PTTRssUrl)):
        main(webHookUrl[i], PTTRssUrl[i])
