'''
Author:ChenHao
'''
import requests

urls=[
    f"https://www.cnblogs.com/#p{page}"
    for page in range(1,50+1)
]

def craw(url):
    # 使用 requests.get() 发送 GET 请求，获取服务器响应对象
    r = requests.get(url)

    # 打印当前请求的 URL，以及响应文本（r.text）的字符长度
    # r.text 是服务器返回的 HTML 或其它文本内容
    print(url, len(r.text))

