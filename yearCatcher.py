import time
import requests as rq

from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

def get_agent() -> dict:
    ua = UserAgent()
    user_agent = ua.random
    return {'user-agent': user_agent}

def get_article_year(subURL: str) -> str:
    headers = get_agent()
    res = rq.get(subURL, headers=headers)
    soup = BS(res.text, 'html.parser')
    header = soup.select('span.article-meta-value')
    year = header[3].text[-4:]
    return year

def find_page_index(page_index: int) -> list:
    flag = False
    year = None
    while flag != True:
        headers = get_agent()
        URL = f'https://www.ptt.cc/bbs/Stock/index{page_index}.html'

        RES = rq.get(URL, headers=headers)

        # 將 HTML 網頁程式碼丟入 bs4 分析模組
        soup = BS(RES.text, 'html.parser')

        # 呈上。取出'下一頁'元素
        paging = soup.select('div.btn-group-paging a')

        # 將'下一頁'元素存到 next_URL 中
        next_URL = 'https://www.ptt.cc' + paging[2]['href']

        dateElements = soup.select('div.date')
        articles = soup.select('div.title a')

        # for 迴圈帶入到下一頁的 URL 資訊
        URL = next_URL

        pervious = None
        current = None

        for i in range(2, len(dateElements)):
            pervious = [dateElements[i-2], articles[i-2]]
            current = [dateElements[i-1], articles[i-1]]
            if pervious[0].text.strip()[0:3] == '12/' and current[0].text.strip()[0:2] == '1/':
                print(f'pervious: {pervious[0].text} {pervious[1].text}')
                print(f'current: {current[0].text} {current[1].text}')
                print(f'page_index: {page_index}')
                flag = True
                subURL = f"https://www.ptt.cc{current[1]['href']}"
                year = get_article_year(subURL)
                break
        if year == None:
            return []
        return [year, page_index]

page_index = 6700
target_index = 7307
result = []
while page_index <= target_index:
    item = find_page_index(page_index)
    if item != []:
        result.append(item)
        print(f'{result}')
    page_index += 1