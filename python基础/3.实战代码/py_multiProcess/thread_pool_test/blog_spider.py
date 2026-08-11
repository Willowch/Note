import requests
from bs4 import BeautifulSoup

urls=[
    f"https://www.cnblogs.com/#p{page}"
    for page in range(1,50+1)
]

def craw(url):
    r=requests.get(url)
    return r.text

#返回一个页面的(连接,标题)列表
def parse(html):
    # 使用 BeautifulSoup 解析 HTML，指定解析器为 "html.parser"（Python 内置）
    soup = BeautifulSoup(html, "html.parser")

    # 查找所有 <a> 标签，且 class 属性为 "post-item-title"（文章标题链接）
    links = soup.find_all("a", class_="post-item-title")

    # 使用列表推导式，遍历每个 <a> 标签，提取 href 属性（链接）和标签内的文本（标题）
    return [(link["href"], link.get_text()) for link in links]

if __name__=="__main__":
    for result in parse(craw(urls[2])):
        print(result)