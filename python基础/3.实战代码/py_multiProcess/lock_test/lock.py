import threading
import time

class Account:
    def __init__(self,balance):
        self.balance=balance

def draw(account:Account,amount):
    #加锁,保证资源独享
    lock=threading.Lock()
    with lock:
        if account.balance>=amount:
            print(f"{threading.current_thread().name}取钱成功")
            # time.sleep(0.1)
            account.balance-=amount
            print(f"余额:{account.balance}")
        else:
            print(f"{threading.current_thread().name}取钱失败.余额不足")

if __name__=="__main__":
    a1=Account(1000)
    ta=threading.Thread(name="贺晨浩",target=draw,args=(a1,800))
    tb=threading.Thread(name="申江源",target=draw,args=(a1,800))

    #不加锁时,有时会取钱失败.余额不足;有时会取钱为-600,且打印顺序错乱; 就是线程切换导致的
    #加上堵塞时,必定取钱余额剩-600
    #加上锁后,必定余额200,且打印顺序正确
    ta.start()
    tb.start()