import flask          # 导入 Flask 框架，用于构建 Web 应用
import json           # 导入 json 模块（此处未直接使用，但通常用于 JSON 处理）
import time           # 导入时间模块，用于模拟耗时操作
from concurrent.futures import ThreadPoolExecutor  # 导入线程池执行器，用于并发执行任务

# 创建 Flask 应用实例
app = flask.Flask(__name__)

# 创建全局线程池（默认使用 CPU 核心数 * 5 个线程）
# 注意：生产环境中应考虑线程池大小限制，避免资源耗尽
pool = ThreadPoolExecutor()

def read_file():
    """模拟读取文件操作（I/O 密集型），耗时 0.1 秒"""
    time.sleep(0.1)
    return "file"

def read_db():
    """模拟读取数据库操作（I/O 密集型），耗时 0.2 秒"""
    time.sleep(0.2)
    return "db"

def read_api():
    """模拟调用外部 API 操作（I/O 密集型），耗时 0.3 秒"""
    time.sleep(0.3)
    return "api"

@app.route("/")
def index():
    """
    根路由处理函数。
    并行执行三个 I/O 任务（读文件、读数据库、读 API），
    将结果合并为 JSON 响应返回。
    """
    # 向线程池提交三个任务，分别返回 Future 对象（代表异步执行的任务句柄）
    result_file = pool.submit(read_file)
    result_db   = pool.submit(read_db)
    result_api  = pool.submit(read_api)

    # 调用 .result() 会阻塞当前线程，直到对应任务完成并返回结果
    # 三个任务并发执行，总耗时约为最慢任务的时间（0.3 秒），而非累加（0.6 秒）
    return flask.jsonify({
        "file": result_file.result(),
        "db":   result_db.result(),
        "api":  result_api.result()
    })

if __name__ == "__main__":
    # 启动 Flask 开发服务器（默认监听 127.0.0.1:5000）
    app.run()