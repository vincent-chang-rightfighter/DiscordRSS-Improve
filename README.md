# Discord RSS - Improve
Send new RSS feed entries to discord via a webhook. 
For PTT RSS 



## Usage
1. Install dependencies - `python3 -m pip install -r requirements.txt`

>安裝依賴 - `python3 -m pip install -r requirements.txt`

2. Modify main.py file 

>修改 main.py 檔案

3. Run the script - `sh run.sh` 

>執行腳本 `sh run.sh` 

this script run main.py 5 seconds again
>此腳本每5秒鐘執行1次



## Configuration

### Modify main.py 

#### line 10 & line 13

Replace to your discord server webhook link
>替換成你的伺服器 webhook 連結

```py
webHookUrl = ['https://discord.com/api/webhooks/...AccountidA',
              'https://discord.com/api/webhooks/...AccountidB']

```

```py
PTTRssUrl = ['https://www.ptt.cc/atom/PC_Shopping.xml',
             'https://www.ptt.cc/atom/HardwareSale.xml']
```

### PTT RSS 訂閱

```https://www.ptt.cc/atom/  + 板名 + .xml```

#### 例如

PTT joke 板 網頁網址

```https://www.ptt.cc/bbs/joke/index.html```

RSS 訂閱網址就是這樣

```https://www.ptt.cc/atom/joke.xml```



A webhook to receive an RSS 

Increase or decrease according to the number of RSS 

The following relation table is for reference.


|PTTRssUrl| Webhook|
|---|---|
|`https://www.ptt.cc/atom/PC_Shopping.xml`|`https://discord.com/api/webhooks/...AccountidA`|
|`https://www.ptt.cc/atom/HardwareSale.xml`|`https://discord.com/api/webhooks/...Accountidb`|

#### line 53
Change webhook post content to your style
>修改 webhook 傳送內容成你的風格

```py
webhook.send(content=f"{Title}\n{hyperLink}", embed=embed)
```