#!/usr/bin/python

from argparse import ArgumentParser
import mysql.connector
from mysql.connector import Error
import re
import socket
from random import randint

def input_database():
	dec_msg='Input Proxy Listener by SOHA Database'
	usage_msg='Input Parameter 1.SOHA_IP_Address 2.SOHA_Mysql_Port 3.SOHA_SVC'

	type = ArgumentParser(description=dec_msg, usage=usage_msg)
	type.add_argument('ip_addr', type=str)
	type.add_argument('port', type=int)
	type.add_argument('soha_svc', type=str)

	param = type.parse_args()

	global master_ip
	global master_port
	global master_svc
	master_ip = param.ip_addr
	master_port = param.port
	master_svc = param.soha_svc

def connection_database(ip_addr,port,soha_svc):
	try:
		soha_conn = mysql.connector.connect(host=ip_addr,port=port,database='(auth = (user_name = dgadmin))',user='(service = (svc = %s) (auth_type = 1))'%(soha_svc),password='petra@one1')
		
	except Error as e:
		print('SOHA Mysql_Connection Error',e)

	return soha_conn

def select_data(sql):
	global master_ip,master_port,master_svc
	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()
	cursor.execute(sql)
	data = cursor.fetchall()
	
	return data

def search_data(reg,data):
	regex = re.compile(reg)
	tmp_data = regex.search(str(data))
	if tmp_data != None:
		match_data = tmp_data.group()
	return match_data

def insert_pt_database():
	global master_ip,master_port,master_svc
	global db_type
	global db_name
	db_type = ['11','12','13','15','16','20','23','29','31']
	db_name = ['ORACLE_trace','SQLSERVER_trace','UDB_trace','SybaseASE_trace','MYSQL_trace','Tibero_trace','Cubrid_trace','Altibase6310_trace','HANADB_trace']
	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()

	for index in range(0,len(db_type)):
		select_sql = 'select nextval(\'PT_A_KEY_SEQ\') from dual'
		data = select_data(select_sql)
		db_id.append(search_data('\d+',data[0]))
		insert_sql = "insert into pt_database(DB_ID,DB_TYPE,DB_NAME,DB_GLOBAL_NAME,SYSTEM_ID) values(%s,%s,\'%s\',0,0)"%(db_id[index],db_type[index],db_name[index])
		cursor.execute(insert_sql)

def insert_pt_db_instance():
	global master_ip,master_port,master_svc
	global db_type
	global db_name

	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()

	for index in range(0,len(db_id)):
		select_sql = 'select nextval(\'PT_A_KEY_SEQ\') from dual'
		data = select_data(select_sql)
		instance_id.append(search_data('\d+',data[0]))
		insert_sql = "insert into pt_db_instance(INSTANCE_ID,SYSTEM_ID,INSTANCE_NAME,DB_TYPE,LINK_NAME) values(%s,0,\'%s\',%s,\'INST_LINK_%s\')"%(instance_id[index],db_name[index],db_type[index],instance_id[index])
		cursor.execute(insert_sql)

def insert_pt_db_service():
	global master_ip,master_port,master_svc

	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()

	for i in range(0,len(db_id)):
		select_sql = 'select nextval(\'PT_A_KEY_SEQ\') from dual'
		data = select_data(select_sql)
		service_id.append(search_data('\d+',data[0]))
		insert_sql = 'insert into pt_db_service(SERVICE_ID,DB_ID,INSTANCE_ID) values(%s,%s,%s)'%(service_id[i],db_id[i],instance_id[i])
		cursor.execute(insert_sql)

def use_port_check(port):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	result = sock.connect_ex(('127.0.0.1',port))
	if result == 0:
		check_result = False
	else:
		check_result = True
	return check_result

def create_random_port(count):
	port_list=[]
	for i in range(0,int(count)):
		tmp_port = randint(10000,65535)
		if len(port_list) == 0:
			if use_port_check(tmp_port):
				port_list.insert(i,tmp_port)
			else:
				tmp_port = randint(10000,65535)
		else:
			j = i-1
			if port_list[j] == tmp_port:
				tmp_port = randint(10000,65535)
			else:
				if use_port_check(tmp_port):
					port_list.insert(j,tmp_port)
				else:
					tmp_port = randint(10000,65535)
	return port_list	

def insert_pt_listen_addr():
	global master_ip,master_port,master_svc
	global listen_port
	global listen_addr_id
	global db_type
	listen_port = create_random_port(len(db_id))

	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()
	
	for i in range(0,len(db_id)):
		select_sql = 'select nextval(\'PT_A_KEY_SEQ\') from dual'
		data = select_data(select_sql)
		listen_addr_id.append(search_data('\d+',data[0]))
		insert_sql = 'insert into pt_listen_addr(listen_addr_id,system_id,target_svc_type,listen_ip,listen_port) values(%s,0,%s,\'%s\',%s)'%(listen_addr_id[i],db_type[i],master_ip,listen_port[i])
		cursor.execute(insert_sql)

def insert_pt_listen_service():
	global master_ip,master_port,master_svc
	global listen_svc_id
	global listen_addr_id
	global instance_id

	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()
	
	for i in range(0,len(db_id)):
		select_sql = 'select nextval(\'PT_A_KEY_SEQ\') from dual'
		data = select_data(select_sql)
		listen_svc_id.append(search_data('\d+',data[0]))
		insert_sql = 'insert into pt_listen_service(listen_svc_id,listen_addr_id,instance_id) values(%s,%s,%s)'%(listen_svc_id[i],listen_addr_id[i],instance_id[i])
		cursor.execute(insert_sql)

def insert_pt_prod_service():
	global master_ip,master_port,master_svc
	global service_id
	global prod_id

	product_id = input('Please enter the product_id of the product to create the prod_service : ')

	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()
	
	select_linkname_sql = 'select product_id from ppmt_product where product_id=%s'%(product_id)
	tmp_id = select_data(select_linkname_sql)
	if len(tmp_id) != 0:
		prod_id = search_data('\d+',tmp_id[0])
		#print(prod_id)
	else:
		print('Product id not found')
		exit()

	select_sql = 'select nextval(\'PT_A_KEY_SEQ\') from dual'
	data = select_data(select_sql)
	service_id = search_data('\d+',data[0])

	prod_service_sql = 'insert into pt_prod_service(service_id,service_name,product_id,pd_svc_type) values(%s,\\\'petraAutoTest Listener\\\',%s,2)'%(service_id,prod_id)
	insert_sql = 'select * from ppmp_prod_exec_sql(0,\'%s\',0)'%(prod_service_sql)
	cursor.execute(insert_sql)

def diff_port(listen_port,listener_port):
	for i in range(0,len(listen_port)):
		if listen_port[i] == listener_port[i]:
			return True
	return False

def insert_pact_inline_listener():
	global master_ip,master_port,master_svc
	global listener_id
	global listen_addr_id
	global service_id
	global prod_id
	global listen_port
	listener_port=[]
	listener_id=[]

	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()

	linkname_select_sql = 'select soha_link from ppmt_product where product_id=%s'%(prod_id)
	cursor.execute(linkname_select_sql)
	linkname = cursor.fetchall()
	linkname = search_data('\w+_\d+',linkname[0])
	
	ip_select_sql = 'select host from pt_database_link_info where link_name=\'%s\''%(linkname)
	cursor.execute(ip_select_sql)
	listener_ip = cursor.fetchall()
	listener_ip = search_data('(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',listener_ip)

	listener_port = create_random_port(len(listen_port))
	
	while True:
		if diff_port(listen_port,listener_port):
			listener_port = create_random_port(len(listen_port))
		else:
			break

	for i in range(0,len(listen_addr_id)):
		select_sql = 'select nextval(\'PT_A_KEY_SEQ\') from dual'
		data = select_data(select_sql)
		listener_id.append(search_data('\d+',data[0]))
	
		insert_sql = 'insert into pact_inline_listener(active_flag,listener_id,service_id,test_mode,bridge_flag,listen_addr_id,listen_ip,listen_port)'
		insert_sql += ' values(0,%s,%s,0,0,%s,\'%s\',%s)'%(listener_id[i],service_id,listen_addr_id[i],listener_ip,listener_port[i])
		cursor.execute(insert_sql)

def update_param():
	global master_ip,master_port,master_svc
	global prod_id

	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()

	sql = 'select * from ppmp_prod_exec_sql(%s,\'UPDATE DG_SYS_PARAM SET(VAL_NUMBER, LAST_UPDATE) = (10, sysdate()) WHERE PARAM_NAME = \\\'START_RELAY_SERVERS\\\'\',0)'%(prod_id)
	cursor.execute(sql)

def main():
	global db_id
	global instance_id
	global service_id
	global listen_addr_id
	global listen_svc_id
	db_id = []
	instance_id = []
	service_id = []
	listen_addr_id = []
	listen_svc_id = []
	input_database()
	insert_pt_database()
	insert_pt_db_instance()
	insert_pt_db_service()
	insert_pt_listen_addr()
	insert_pt_listen_service()
	insert_pt_prod_service()
	insert_pact_inline_listener()
	update_param()
	
main()
