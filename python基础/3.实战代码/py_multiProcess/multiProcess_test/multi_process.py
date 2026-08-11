import math
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
P5MES = [112272535095293]* 100

def is_prime(n):
    """
    判断一个整数 n 是否为素数（质数）。
    参数:
        n (int): 待判断的正整数
    返回:
        bool: 如果是素数返回 True，否则返回 False
    """
    # 小于 2 的数不是素数
    if n < 2:
        return False
    # 2 是素数
    if n == 2:
        return True
    # 偶数（除 2 外）都不是素数
    if n % 2 == 0:
        return False

    # 只需检查到 sqrt(n) 即可，且只检查奇数因子
    sqrt_n = int(math.floor(math.sqrt(n)))  # 取整
    for i in range(3, sqrt_n + 1, 2):  # 从 3 开始，步长 2（跳过偶数）
        if n % i == 0:
            return False
    return True  # 没有找到因子，则为素数

def single_thread():
    for i in P5MES:
        is_prime(i)

def multi_thread():
    with ThreadPoolExecutor() as pool:
        pool.map(is_prime,P5MES)

def multi_process():
    with ProcessPoolExecutor() as pool:
        pool.map(is_prime,P5MES)


if __name__ == "__main__":
    start = time.time()
    single_thread()
    end = time.time()
    print("single_thread, cost:", end - start, "seconds")

    start = time.time()
    multi_thread()
    end = time.time()
    print("multi_thread, cost:", end - start, "seconds")

    start = time.time()
    multi_process()
    end = time.time()
    print("multi_process, cost:", end - start, "seconds")