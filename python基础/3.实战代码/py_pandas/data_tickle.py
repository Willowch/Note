'''
Author:ChenHao
'''
import pandas as pd
'''
csv清洗脚本,将csv文件中的数据进行清洗,并保存为新的csv文件,供数据统计画图使用
'''
data=pd.read_csv('data/movies.csv')


data['电影名']=data['电影名'].str.replace('。','')
data.to_csv('data/movies_clean.csv',index=False)

