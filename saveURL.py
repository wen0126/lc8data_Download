import mysql.connector
import time
import os

CLOUD_MAX = 50  # 云量
PATH = 23  # 行号
ROW = 31  # 列号
START_TIME = '2013-01-01'
END_TIME = '2016-01-01'
SPACECRAFT = 'LANDSAT_8'  #
INFO = 'SCENE_ID, PRODUCT_ID,CLOUD_COVER,TOTAL_SIZE,BASE_URL'  # 保存的信息：产品ID，云量，大小，链接

BASE_URL = 'http://storage.googleapis.com/'

mydb = mysql.connector.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="960816",  # 数据库密码
    database='landsat_index',  # 连接数据库
)
mycursor = mydb.cursor()  # 创建指针

# 生成新文件夹
file_path = '{}{:0>3d}'.format(PATH, ROW)
base_path = os.getcwd()
entity_dir = os.path.join(base_path, file_path)
os.makedirs(entity_dir, exist_ok=True)
os.chdir(entity_dir)

print('Retriving {}{:0>3d}'.format(PATH, ROW))
time_start = time.time()
sql = "SELECT {} FROM gc_index WHERE PRODUCT_ID !='' AND SPACECRAFT_ID = '{}' AND WRS_PATH={} AND WRS_ROW = {} AND CLOUD_COVER<={} AND DATE_ACQUIRED >={} AND DATE_ACQUIRED <= {}".format(
    INFO, SPACECRAFT, PATH, ROW, CLOUD_MAX,START_TIME,END_TIME)
mycursor.execute(sql)
myresult = mycursor.fetchall()
time_end = time.time()
print('Time cost: ', time_end - time_start)
myresult.sort()
print("Data Num: ", len(myresult))
# for result in myresult:
# print(result)


# 保存检索到的影像信息
file_result = 'gs{}{:0>3d}_result.csv'.format(PATH, ROW)
with open(file_result, 'w') as f:
    f.write(INFO + '\n')
    for result in myresult:
        f.write(','.join(str(i) for i in result) + '\n')
# 保存下载链接
file_url = 'gs{}{:0>3d}_url.txt'.format(PATH, ROW)
down_url = {}
for result in myresult:
    url_list = []
    EntityID = result[1]
    url_middle = result[4].split('//')[-1]
    url0 = '{}{}/{}_ANG.txt'.format(BASE_URL, url_middle, EntityID)
    url1 = '{}{}/{}_B1.TIF'.format(BASE_URL, url_middle, EntityID)
    url2 = '{}{}/{}_B2.TIF'.format(BASE_URL, url_middle, EntityID)
    url3 = '{}{}/{}_B3.TIF'.format(BASE_URL, url_middle, EntityID)
    url4 = '{}{}/{}_B4.TIF'.format(BASE_URL, url_middle, EntityID)
    url5 = '{}{}/{}_B5.TIF'.format(BASE_URL, url_middle, EntityID)
    url6 = '{}{}/{}_B6.TIF'.format(BASE_URL, url_middle, EntityID)
    url7 = '{}{}/{}_B7.TIF'.format(BASE_URL, url_middle, EntityID)
    url8 = '{}{}/{}_B8.TIF'.format(BASE_URL, url_middle, EntityID)
    url9 = '{}{}/{}_B9.TIF'.format(BASE_URL, url_middle, EntityID)
    url10 = '{}{}/{}_B10.TIF'.format(BASE_URL, url_middle, EntityID)
    url11 = '{}{}/{}_B11.TIF'.format(BASE_URL, url_middle, EntityID)
    url12 = '{}{}/{}_BQA.TIF'.format(BASE_URL, url_middle, EntityID)
    url13 = '{}{}/{}_MTL.txt'.format(BASE_URL, url_middle, EntityID)
    url_list = [url0, url1, url2, url3, url4, url5, url6, url7, url8, url9, url10, url11, url12, url13]
    down_url[EntityID] = url_list
with open(file_url, 'w') as f:
    f.write(str(down_url))
