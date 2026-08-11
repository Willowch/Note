import concurrent.futures
import blog_spider

#craw
with concurrent.futures.ThreadPoolExecutor() as pool:
    #全部一次操作map,返回的类型为迭代器,.result返回结果本身,与参数一一对应
    htmls=pool.map(blog_spider.craw,blog_spider.urls)
    # print(type(htmls))
    htmls=list(zip(blog_spider.urls,htmls))
    for url,html in htmls:
        print(url,len(html))

print("craw 结束")

#parse
with concurrent.futures.ThreadPoolExecutor() as pool:
    futures={}
    #单个操作
    for url,html in htmls:
        #submit返回的是封装起来的future对象,要.result返回结果本身:parse返回(连接,标题)的列表
        future=pool.submit(blog_spider.parse,html)
        futures[future]=url
    # #一起遍历
    # for future,url in futures.items():
    #     print(url,future.result())#.result返回结果本身
    #先出结果先打印:可在结果中观察到 parse的页码不再按顺序
    for future in concurrent.futures.as_completed(futures):
        url=futures[future]
        print(url,future.result())