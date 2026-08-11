import queue          # 导入队列模块，用于线程间安全地传递数据
import threading      # 导入线程模块，用于创建和管理多线程
import time           # 导入时间模块，用于模拟延时
import random         # 导入随机模块，用于生成随机延时
import blog_spider    # 导入自定义模块，包含 urls 列表、craw() 和 parse() 函数

def do_craw(url_queue: queue.Queue, html_queue: queue.Queue):
    while True:
        # 从 URL 队列中取出一个 URL（若队列为空则阻塞等待）
        url = url_queue.get()
        # 调用爬虫函数获取网页 HTML 源码
        html = blog_spider.craw(url)
        # 将 HTML 放入另一个队列，供解析线程使用
        html_queue.put(html)
        # 打印当前线程名称、爬取的 URL 以及 URL 队列剩余大小
        print(f"当前线程:{threading.currentThread().name},爬取网页:{url},url_queue大小:{url_queue.qsize()}")
        # 随机休眠 1~2 秒，模拟网络延迟，避免请求过快
        time.sleep(random.randint(1, 2))

def do_parse(html_queue: queue.Queue, fout):
    while True:
        # 从 HTML 队列中取出一个 HTML 源码
        html = html_queue.get()
        # 调用解析函数，得到 (链接, 标题) 元组列表
        results = blog_spider.parse(html)
        # 遍历结果，逐行写入输出文件
        for result in results:
            fout.write(f"{result}\n")
        # 打印当前线程名称和 HTML 队列剩余大小
        print(f"当前线程:{threading.currentThread().name},html_queue大小:{html_queue.qsize()}")
        # 随机休眠 1~2 秒，模拟解析耗时
        time.sleep(random.randint(1, 2))

if __name__ == "__main__":
    # 创建两个队列：url_queue 存放待爬取 URL，html_queue 存放爬取到的 HTML
    url_queue = queue.Queue()
    html_queue = queue.Queue()

    # 将所有待爬取的 URL 放入 url_queue
    for url in blog_spider.urls:
        url_queue.put(url)

    # 启动 3 个爬虫线程（生产者），它们从 url_queue 取 URL 并爬取
    for i in range(3):
        t = threading.Thread(target=do_craw, args=(url_queue, html_queue), name=f"craw{i}")
        t.start()

    # 打开输出文件
    fout = open("output.txt", "w", encoding="utf-8")
        # 启动 2 个解析线程（消费者），它们从 html_queue 取 HTML 并解析写入文件
    for i in range(2):
        t = threading.Thread(target=do_parse, args=(html_queue, fout), name=f"parse{i}")
        t.start()
