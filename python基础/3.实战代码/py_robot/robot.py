import requests
from lxml import html
import csv
import re

# 1.爬取电影数据主逻辑:
#     1>向榜单页面爬取所有电影的url
#     2>遍历所有电影url,获取每部电影信息,组成字典返回
#     3>将字典写入csv文件
# 2.由于该网站无page属性,故无法获取page属性,故无法获取分页数据;
# 注意:写入csv文件后,要观察一下,然后对特殊数据找问题,解决问题
# 3.用正则来对数据进行清洗逻辑:
#     1>从网页中爬取的数据,先通过正则匹配提取
#     2>再写入csv文件



FILE_SAVE_PATH= "../py_pandas/data/movies.csv"  #保存文件路径
TMDB_BASE_URL = "https://www.themoviedb.org"#基础url
TMDB_TOP_URL="https://www.themoviedb.org/movie/top-rated" #榜单页面url
MORE_MOVIE_URL="https://www.themoviedb.org/discover/movie/items"

#获取url电影详细信息
def get_movie_year(movie_years):
    #py中字符串有值时,返回True,否则返回False
    movie_years=movie_years[0].strip() if movie_years else ""
    return movie_years.replace("(", "").replace(")", "")

#清洗电影年份
def get_movie_date(movie_dates):
    movie_dates=movie_dates[0].strip() if movie_dates else "" #先提取,去空格
    return re.search(r"\d{4}-\d{2}-\d{2}",movie_dates).group() #返回匹配到的值;

#清洗电影时长
def get_movie_cost_time(movie_cost_times):
    movie_cost_times=movie_cost_times[0].strip() if movie_cost_times else ""#先提取,去空格
    hours=re.search(r"(\d+)h",movie_cost_times)#匹配小时的match对象
    minutes=re.search(r"(\d+)m",movie_cost_times)
    h=int(hours.group((1))) if hours else 0 #正则用()分组后,可用.group(N)返回第N组,否则返回全部匹配的值
    m=int(minutes.group((1))) if minutes else 0
    return str(h*60+m)+"分钟"

#获得单个电影信息
def get_movie_detail(movie_all_url):
    #1.发送请求,获取电影详情
    movie_response=requests.get(movie_all_url,timeout=60)

    # 2.解析,获取文本文档
    doc=html.fromstring(movie_response.text)
    #.xpath返回的是 匹配值的列表(一般只有一个值)
    movie_name=doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()") #电影名称
    movie_years = doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/span/text()") #电影上映年份
    movie_dates = doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[2]/text()") #电影上映时间
    movie_tags = doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[3]/a/text()")#电影标签
    movie_cost_times=doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[4]/text()")#电影时长
    movie_scores = doc.xpath("//*[@id='consensus_pill']/div/div[1]/div/div/@data-percent")#评分
    movie_languages = doc.xpath("//*[@id='media_v4']/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()")#语言
    movie_directors = doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()")# 导演
    movie_authors = doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[2]/p[1]/a/text()")# 作者
    movie_slogans = doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/h3[1]/text()")# 标语
    movie_descriptions = doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/div/p/text()")# 描述
    #此部电影信息 组成字典
    movie_infos={
        "电影名":movie_name[0].strip() if movie_name else "",#strip去除收尾多余空格
        "上映年份":get_movie_year(movie_years),
        "上映时间":get_movie_date(movie_dates),
        "标签":",".join(movie_tags) if movie_tags else "",
        "时长":get_movie_cost_time(movie_cost_times),
        "评分":movie_scores[0].strip() if movie_scores else "",
        "语言":movie_languages[0].strip() if movie_languages else "",
        "导演":",".join(movie_directors) if movie_directors else "",
        "作者":",".join(movie_authors) if movie_authors else "",
        "标语":movie_slogans[0].strip() if movie_slogans else "",
        "描述":movie_descriptions[0].strip() if movie_descriptions else ""
    }
    return movie_infos

#将电影信息保存到csv文件中
def save_all_movies(all_movies):
    with open(FILE_SAVE_PATH,"w",encoding="utf-8",newline="")as f:
        writers=csv.DictWriter(f,fieldnames=["电影名","上映年份","上映时间","标签","时长","评分","语言","导演","作者","标语","描述"])
        writers.writeheader()#写入表头
        writers.writerows(all_movies)#写入数据


def main():
    all_movies = []  # 存储所有电影信息,以便保存到csv当中
    # 1.发送请求,获取高分电影榜 电影
    response = requests.get(TMDB_TOP_URL, timeout=60)  # 设置超时时间

    # 2.将榜单数据转为html文本文档
    docu = html.fromstring(response.text)
    #从浏览器获取xpath地址
    movie_list = docu.xpath(
        "/html/body/div[2]/main/section/div/div/div/div[2]/div[2]/div/section/div/div/div[1]/div/div")

    # 3.遍历电影列表,获取电影详细信息
    for movie in movie_list:
        movie_url = movie.xpath("./div/div/a/@href")
        if movie_url:
            # 电影详情完整url
            movie_all_url = TMDB_BASE_URL + movie_url[0] + "?language=zh-CN"  # 加上参数,返回中文
            print(movie_all_url)
            movie_detail = get_movie_detail(movie_all_url)
            all_movies.append(movie_detail)


    print("所有电影已读出,正在写入csv文件...")
    save_all_movies(all_movies)


if __name__=="__main__":
    main()