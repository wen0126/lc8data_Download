import mysql.connector

# 连接数据库
mydb = mysql.connector.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="960816",  # 数据库密码
)
mycursor = mydb.cursor()
mycursor.execute("DROP DATABASE landsat_index")  # 删除已有的数据库
mycursor.execute("CREATE DATABASE landsat_index")  # 创建数据库
mycursor.execute("USE landsat_index")

# 生成表
mycursor.execute("CREATE TABLE gc_index( sid INT UNSIGNED AUTO_INCREMENT, \
	SCENE_ID VARCHAR(30),\
	PRODUCT_ID VARCHAR(50),\
	SPACECRAFT_ID VARCHAR(10),\
	SENSOR_ID VARCHAR(10),\
	DATE_ACQUIRED VARCHAR(10),\
	COLLECTION_NUMBER VARCHAR(10),\
	COLLECTION_CATEGORY VARCHAR(10),\
	SENSING_TIME VARCHAR(30),\
	DATA_TYPE VARCHAR(10),\
	WRS_PATH INT,\
	WRS_ROW INT,\
	CLOUD_COVER FLOAT,\
	NORTH_LAT FLOAT,\
	SOUTH_LAT FLOAT,\
	WEST_LON FLOAT,\
	EAST_LON FLOAT,\
	TOTAL_SIZE INT,\
	BASE_URL VARCHAR(150),\
	PRIMARY KEY ( sid ))DEFAULT CHARSET=utf8")

# 查看表
mycursor.execute("SHOW TABLES")
for x in mycursor:
    print(x)

# 查看描述
mycursor.execute("desc gc_index")
for x in mycursor:
    print(x)

# 插入数据
sql = "INSERT INTO gc_index (SCENE_ID,PRODUCT_ID,SPACECRAFT_ID,SENSOR_ID,DATE_ACQUIRED,COLLECTION_NUMBER,COLLECTION_CATEGORY,SENSING_TIME,DATA_TYPE,WRS_PATH,WRS_ROW,CLOUD_COVER,NORTH_LAT,SOUTH_LAT,WEST_LON,EAST_LON,TOTAL_SIZE,BASE_URL)\
                           VALUES (%s,         %s,           %s,       %s,           %s,                %s,                %s,          %s,       %s,      %s,    %s,          %s,       %s,       %s,      %s,      %s,        %s,       %s)"

# 得从第二行开始
f = open('./index.csv', 'r')
lines = f.readlines()
i = 0
for line in lines:
    i += 1
    line = line.split(',')
    if i >= 2:
        mycursor.execute(sql,line)
mydb.commit()
