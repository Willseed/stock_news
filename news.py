# HTTP Method: GET(), POST()
import random
import requests as rq
import time
import calendar
import os

# 導入 BeautifulSoup module: 解析 HTML 語法工具
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

def index_mapping(year: int) -> list:
    index_list = {
        2011: [40, 5],
        2012: [44, 9],
        2013: [52, 14],
        2014: [65, 16],
        2015: [80, 39],
        2016: [118, 29],
        2017: [146, 27],
        2018: [172, 44],
        2019: [215, 741],
        2020: [955, 1459],
        2021: [2413, 2113],
        2022: [4525, 1292],
        2023: [5817, 991],
        2024: [6808, 7308]
    }
    return index_list[year]

# 時間戳轉換成日期
def timestamp2date(timestamp: str):
    tmp_list = timestamp.split()
    month = mapping_month(tmp_list[1])
    return f'{tmp_list[4]}{month:02d}{int(tmp_list[2]):02d}'

# 英文月份縮寫對應數字
def mapping_month(month_abbr: str):
    month_abbr_list = {month: index for index, month in enumerate(calendar.month_abbr) if month}
    return month_abbr_list[month_abbr]

def find_last_index(content):
    last_index = 0
    for index, item in enumerate(content):
        if item == '--':
            last_index = index
    return last_index

def extract_content(subURL: str, article: str, target_year: int):
    ua = UserAgent()
    user_agent = ua.random
    headers = {'user-agent': user_agent}
    print(subURL)
    print(article)
    res = rq.get(subURL, headers=headers)
    soup = BS(res.text, 'html.parser')
    header = soup.select('span.article-meta-value')
    author = header[0].text
    timestamp = header[3].text
    date = timestamp2date(timestamp)
    print(date)
    if int(date[0:4]) != target_year:
        return
    serial_number = subURL.split('/')[-1]
    if os.path.isdir(f'file/{target_year}') == False:
        os.makedirs(f'file/{target_year}')
    with open(f'./file/{target_year}/{date}_{serial_number}.txt', 'w', encoding='utf-8') as f:
        f.write(subURL + '\n')
        f.write(article + '\n')
        f.write(author + '\n')
        f.write(timestamp + '\n')
        main_container = soup.find(id='main-container')
        all_text = main_container.text
        content = all_text.split('\n')
        last_index = find_last_index(content)
        final_content = content[0:last_index]
        f.write("\n".join(final_content))
        comment_tag = soup.select('div.push span.push-tag')
        comment_user = soup.select('div.push span.push-userid')
        comment_content = soup.select('div.push span.push-content')
        for i in range(len(comment_tag)):
            f.write(f'{comment_tag[i].text.strip()} {comment_user[i].text.strip()}{comment_content[i].text.strip()}\n')

year = 2023
year_index, page_index = index_mapping(year)

# 將 PTT Stock 存到 URL 變數中
URL = f'https://www.ptt.cc/bbs/Stock/index{year_index}.html'

# 使用 for 迴圈將逐筆將標籤(tags)裡的 List 印出, 這裡取3頁
for round in range(page_index):
    
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
    for item in articles:
        article = item.text
        if '[公告]' in article:
            continue
        subURL = 'https://www.ptt.cc' + item['href']
        try:
            extract_content(subURL, article, year)
        except Exception as e:
            print(f'發生異常，異常原因：{e}')
        time.sleep(random.uniform(0.5, 2.5))