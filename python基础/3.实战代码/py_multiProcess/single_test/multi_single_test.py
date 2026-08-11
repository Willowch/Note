from py_multiProcess.single_test import blog_spider
import threading
import time

def single_thread():
    print("单线程开始")
    for url in blog_spider.urls:
        blog_spider.craw(url)
    print("单线程结束")


def multi_thread():
    print("多线程开始")
    # 创建一个空列表，用于存放所有线程对象
    threads = []

    for url in blog_spider.urls:
        # 为每个 URL 创建一个线程，目标函数是 blog_spider.craw，并传入 url 作为参数
        # 注意：args=(url,) 中的逗号必须保留，以确保传递的是元组
        threads.append(
            threading.Thread(target=blog_spider.craw, args=(url,))
        )

    # 启动所有线程，每个线程开始执行 craw 函数
    for thread in threads:
        thread.start()

    # 等待所有线程执行完毕，主线程阻塞直到所有子线程结束
    for thread in threads:
        thread.join()
    print("多线程结束")

if __name__=="__main__":
    #分为两个操作:爬取,输出
    #线程1爬取,线程1输出和线程2爬取同时;持续并发
    start_time = time.time()
    single_thread()
    print(f"single_thread: {time.time() - start_time} seconds")#28秒

    start_time = time.time()
    multi_thread()
    print(f"multi_thread: {time.time() - start_time} seconds")#6秒