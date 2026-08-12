import asyncio


# 这是一个协程函数（定义菜谱），调用它并不会开始做菜
async def cook_dish(dish_name):
    print(f"开始炖 {dish_name}")
    # 模拟炖菜等待的过程（等20分钟）
    await asyncio.sleep(2)
    print(f"{dish_name} 炖好了！")
    return f"一碗{dish_name}"

async def main():
    # 同时点三个火（创建任务），但此时还没真正开始等
    # task1 = asyncio.create_task(cook_dish("红烧肉1号"))
    # task2 = asyncio.create_task(cook_dish("红烧肉2号"))
    # task3 = asyncio.create_task(cook_dish("红烧肉3号"))

    #另一种写法,创建tasks列表,直接传入
    tasks=[asyncio.create_task(cook_dish(f"红烧肉{i}号")) for i in range(3)]
    results=await asyncio.gather(*tasks)

    # 现在站在厨房中间等所有锅响（并发等待）:result返回结果列表
    # results = await asyncio.gather(task1, task2, task3)
    # print(f"全部完成：{results}")

# 程序的唯一入口
if __name__ == "__main__":
    asyncio.run(main())