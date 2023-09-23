# HTTP Method: GET(), POST()
import random
import requests as rq
import time

# 導入 BeautifulSoup module: 解析 HTML 語法工具
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

def find_last_index(content):
    last_index = 0
    for index, item in enumerate(content):
        if item == '--':
            last_index = index
    return last_index

def extract_content(subURL):
    ua = UserAgent()
    user_agent = ua.random
    headers = {'user-agent': user_agent}
    print(subURL)
    res = rq.get(subURL, headers=headers)
    soup = BS(res.text, 'html.parser')
    header = soup.select('span.article-meta-value')
    author = header[0].text
    timestamp = header[3].text
    print(author)
    print(timestamp)
    main_container = soup.find(id='main-container')
    all_text = main_container.text
    content = all_text.split('\n')
    last_index = find_last_index(content)
    final_content = content[0:last_index]
    print("\n".join(final_content))
    comment_tag = soup.select('div.push span.push-tag')
    comment_user = soup.select('div.push span.push-userid')
    comment_content = soup.select('div.push span.push-content')
    for i in range(len(comment_tag)):
        print(f'{comment_tag[i].text.strip()} {comment_user[i].text.strip()}{comment_content[i].text.strip()}')


# 將 PTT Stock 存到 URL 變數中
URL = 'https://www.ptt.cc/bbs/Stock/index43.html' 


# 使用 for 迴圈將逐筆將標籤(tags)裡的 List 印出, 這裡取3頁
for round in range(5775):
    
    # Send get request to PTT Stock
    RES = rq.get(URL)
    
    # 將 HTML 網頁程式碼丟入 bs4 分析模組
    soup = BS(RES.text, 'html.parser') 
    
    # 查找標題文章的 html 元素。過濾出標籤名稱為'div'且 class 屬性為 title, 子標籤名稱為'a'
    articles = soup.select('div.title a') 
    
    # 呈上。取出'下一頁'元素
    paging = soup.select('div.btn-group-paging a') 
    
    # 將'下一頁'元素存到 next_URL 中
    next_URL = 'https://www.ptt.cc' + paging[2]['href'] 
    
    # for 迴圈帶入到下一頁的 URL 資訊
    URL = next_URL 
    
    # 萃取文字出來: title, URL
    for x in articles: 
        article = x.text
        if '[公告]' in article:
            continue
        subURL = 'https://www.ptt.cc' + x['href']
        print(article)
        try:
            extract_content(subURL)
        except Exception as e:
            print(f'發生異常，異常原因：{e}')
        time.sleep(random.uniform(0.5, 2.5))