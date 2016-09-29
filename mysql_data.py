# coding:utf-8
import MySQLdb
from datetime import date
database = {}
database['host'] = '127.0.0.1'
database['db_name'] = 'your_database_name'
database['user'] = 'root'
database['pwd']='****'

conn = MySQLdb.Connection(db=database['db_name'],host=database['host'],user=database['user'],passwd=database['pwd'], charset='UTF8')
cursor = conn.cursor()
length_of_table = cursor.execute("show tables")
print("There is %d tables in total"%int(length_of_table))

print("共计%s张表"%str(length_of_table)) 
# 取得所有表名称
table_list = [item[0] for item in cursor.fetchall()]

# 循环获得所有表名中的列信息
all_table_info = []
sql="select COLUMN_NAME,COLUMN_TYPE,COLUMN_DEFAULT,IS_NULLABLE,EXTRA,COLUMN_COMMENT from INFORMATION_SCHEMA.COLUMNS where table_name='%s' and table_schema='%s'"
for table_name in table_list:
	#  查询字段名,数据类型,默认值,允许非空,是否自动递增,备注
	cursor.execute(sql % (table_name, database['db_name']))
	table_info = cursor.fetchall();
	table_info = [{'name':col[0], 'type':col[1], 'default':col[2], 'is_nullable':col[3], 'extra':col[4],'comment':col[5]} for col in table_info]
	all_table_info.append({'table_name':table_name,'data':table_info})
cursor.close()
conn.close()

data_file = file(database['db_name']+str(date.today())+".txt", "w+")
data_file.write("自动生成数据字典\n")
data_file.write("生成日期:%s"%str(date.today()))
for table in all_table_info:
	data_file.write("表名: "+str(table['table_name'])+"\n")
	data_file.write("字段名                 数据类型                默认值                  允许非空                 是否自动递增             备注\n")
	for col in table['data']:
		col_data = [col['name'], col['type'], str(col['default']), col['is_nullable'], u"是" if col['extra']=='auto_increment' else u"否", col['comment'] or u""]
		
		col_data = [item+" "*(20-len(item)) for item in col_data]
		insert_str= u' | '.join(col_data) + "\n"
		data_file.write(insert_str.encode('utf-8'))
		data_file.write("\n")
data_file.close();
print("生成完毕")
