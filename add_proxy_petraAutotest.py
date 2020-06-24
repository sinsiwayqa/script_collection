#!/usr/bin/python

from argparse import ArgumentParser
import mysql.connector
from mysql.connector import Error
import re
import socket
from random import randint

def input_database(): # SOHA데이터 베이스 정보를 파라미터로 입력 받아 설정
	# 변수 선언
	global master_ip
	global master_port
	global master_svc
	dec_msg='Input Proxy Listener by SOHA Database'
	usage_msg='Input Parameter 1.SOHA_IP_Address 2.SOHA_Mysql_Port 3.SOHA_SVC'

	# 파라미터 파싱
	type = ArgumentParser(description=dec_msg, usage=usage_msg)
	type.add_argument('ip_addr', type=str)
	type.add_argument('port', type=int)
	type.add_argument('soha_svc', type=str)
	param = type.parse_args()

	# 파싱된 파라미터 저장
	master_ip = param.ip_addr
	master_port = param.port
	master_svc = param.soha_svc

def connection_database(ip_addr,port,soha_svc): # SOHA데이터베이스에 커넥션 후 커넥션 객체를 리턴
	# SOHA Mysql Connection
	try:
		soha_conn = mysql.connector.connect(host=ip_addr,port=port,database='(auth = (user_name = dgadmin))',user='(service = (svc = %s) (auth_type = 1))'%(soha_svc),password='petra@one1')
		
	except Error as e:
		print('SOHA Mysql_Connection Error',e)

	return soha_conn

def select_data(sql): # 인자값으로 SELECT 쿼리문을 받아 해당 select 쿼리 실행 후 결과 리턴
	#사용할 전역 변수 선언
	global master_ip,master_port,master_svc
	
	# 데이터베이스에 커넥션 후 인자로 받은 SQL문 실행 후 결과를 저장하여 리턴
	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()
	cursor.execute(sql)
	data = cursor.fetchall()
	
	return data

def search_data(reg,data): # 리턴된 튜플형의 데이터에서 정규표현식에 맞는 데이터 추출 (정규표현식,추출할 원시 데이터)
	#정규표현식을 사용하여 비교
	regex = re.compile(reg)
	tmp_data = regex.search(str(data))

	if tmp_data != None:
		match_data = tmp_data.group() # 졍규표현식으로 매칭된 데이터가 존재할때 데이터를 튜플형으로 저장
	
	return match_data

def insert_pt_database(): # PT_DATABASE 테이블에 데이터 삽입
	#사용할 전역 변수 선언
	global master_ip,master_port,master_svc
	global db_type
	global db_name
	
	db_type = ['11','12','13','15','16','20','23','29','31'] # Petra 테스트 자동화 프로그램이 현재 작성완료된 데이터베이스 타입을 고정으로 선언
	# 테스트 자동화는 DBMS별 DB명_trace로 이용하도록 고정되어 있어 DB_NAME을 고정으로 선언
	db_name = ['ORACLE_trace','SQLSERVER_trace','UDB_trace','SybaseASE_trace','MYSQL_trace','Tibero_trace','Cubrid_trace','Altibase6310_trace','HANADB_trace']
	
	#데이터 베이스 커넥션
	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()

	# 지원되는 DBMS의 수만큼 반복하여 ID값을 생성 후에 데이터 인서트
	for index in range(0,len(db_type)):
		# ID값 생성하여 db_id에 삽입
		select_sql = 'select nextval(\'PT_A_KEY_SEQ\') from dual'
		data = select_data(select_sql)
		db_id.append(search_data('\d+',data[0]))
		# 인서트 쿼리를 생성하여 데이터베이스에 인서트
		insert_sql = "insert into pt_database(DB_ID,DB_TYPE,DB_NAME,DB_GLOBAL_NAME,SYSTEM_ID) values(%s,%s,\'%s\',0,0)"%(db_id[index],db_type[index],db_name[index])
		cursor.execute(insert_sql)

def insert_pt_db_instance(): # PT_DB_INSTANCE 테이블에 데이터 삽입
	# 사용할 전역 변수 선언
	global master_ip,master_port,master_svc
	global db_type
	global db_name

	# 데이터베이스 커넥션
	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()

	# 지원되는 DBMS의 수만큼 반복하여 ID값을 생성 후에 데이터 인서트 
	for index in range(0,len(db_id)):
		# ID값 생성하여 instance_id에 삽입
		select_sql = 'select nextval(\'PT_A_KEY_SEQ\') from dual'
		data = select_data(select_sql)
		instance_id.append(search_data('\d+',data[0]))
		# 인서트 쿼리를 생성하여 데이터베이스에 인서트
		insert_sql = "insert into pt_db_instance(INSTANCE_ID,SYSTEM_ID,INSTANCE_NAME,DB_TYPE,LINK_NAME) values(%s,0,\'%s\',%s,\'INST_LINK_%s\')"%(instance_id[index],db_name[index],db_type[index],instance_id[index])
		cursor.execute(insert_sql)

def insert_pt_db_service(): # PT_DB_SERVICE 테이블에 데이터 삽입
	# 사용할 전역 변수 선언
	global master_ip,master_port,master_svc

	# 데이터베이스 커넥션
	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()

	# 지원되는 DBMS의 수만큼 반복하여 ID값을 생성 후에 데이터 인서트
	for i in range(0,len(db_id)):
		# ID값 생성하여 instance_id에 삽입
		select_sql = 'select nextval(\'PT_A_KEY_SEQ\') from dual'
		data = select_data(select_sql)
		service_id.append(search_data('\d+',data[0]))
		# 인서트 쿼리를 생성하여 데이터베이스에 인서트
		insert_sql = 'insert into pt_db_service(SERVICE_ID,DB_ID,INSTANCE_ID) values(%s,%s,%s)'%(service_id[i],db_id[i],instance_id[i])
		cursor.execute(insert_sql)

def use_port_check(port): # 포트번호를 인자로 받아 해당 포트가 사용중인지 확인
	# 소켓을 생성하여 인자로 받은 포트번호에 테스트 커넥션을 시도 // 테스트 커넥션이 성공한다면 0이 리턴
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	result = sock.connect_ex(('127.0.0.1',port))

	if result == 0:
		check_result = False # 해당 포트가 사용중일때 False리턴
	else:
		check_result = True # 해당 포트가 사용중이지 않을때 True리턴
	return check_result

def create_random_port(count): # 인자로 받은 수만큼의 랜덤 포트를 생성 생성되는 랜덤 포트 범위는 10000~65535
	# 생성된 포트가 저장될 리스트 선언
	port_list=[]

	# 인자로 받은 수만큼 반복
	for i in range(0,int(count)):
		# 10000~65535 사이 랜덤 포트 생성
		tmp_port = randint(10000,65535)
		# 현재 생성된 포트가 하나도 없을 경우
		if len(port_list) == 0:
			# 생성된 랜덤포트가 사용중인 포트인지 확인
			if use_port_check(tmp_port):
				port_list.insert(i,tmp_port) # 사용중이지 않다면 리스트에 삽입
			else:
				tmp_port = randint(10000,65535) # 사용중이라면 랜덤포트 다시 생성
		# 생성된 포트가 있을 경우
		else:
			j = i-1
			# 생성된 포트가 중복될 수 있으므로 중복 체크
			if port_list[j] == tmp_port:
				# 중복이 발생할 경우 랜덤 포트 재생성
				tmp_port = randint(10000,65535)
			# 중복이 없을 경우
			else:
				# 생성된 랜덤포트가 사용중인 포트인지 확인
				if use_port_check(tmp_port):
					port_list.insert(j,tmp_port) # 사용중이지 않다면 리스트에 삽입
				else:
					tmp_port = randint(10000,65535) # 사용중이라면 랜덤포트 다시 생성
	return port_list	

def insert_pt_listen_addr(): # PT_LISTEN_ADDR 테이블에 데이터 삽입
	# 사용할 전역 변수 선언
	global master_ip,master_port,master_svc
	global listen_port
	global listen_addr_id
	global db_type
	# 보안 대상에서 사용할 LISTEN_IP를 생성
	listen_port = create_random_port(len(db_id))

	# 데이터 베이스 커넥션
	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()
	
	# 지원되는 DBMS의 수만큼 반복하여 ID값을 생성 후에 데이터 인서트
	for i in range(0,len(db_id)):
		# ID값 생성하여 instance_id에 삽입
		select_sql = 'select nextval(\'PT_A_KEY_SEQ\') from dual'
		data = select_data(select_sql)
		listen_addr_id.append(search_data('\d+',data[0]))
		# 인서트 쿼리를 생성하여 데이터베이스에 인서트
		insert_sql = 'insert into pt_listen_addr(listen_addr_id,system_id,target_svc_type,listen_ip,listen_port) values(%s,0,%s,\'%s\',%s)'%(listen_addr_id[i],db_type[i],master_ip,listen_port[i])
		cursor.execute(insert_sql)

def insert_pt_listen_service(): # PT_LISTEN_SERVICE 테이블에 데이터 삽입
	# 사용할 전역 변수 선언
	global master_ip,master_port,master_svc
	global listen_svc_id
	global listen_addr_id
	global instance_id

	# 데이터 베이스 커넥션
	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()
	
	# 지원되는 DBMS의 수만큼 반복하여 ID값을 생성 후에 데이터 인서트
	for i in range(0,len(db_id)):
		# ID값 생성하여 instance_id에 삽입
		select_sql = 'select nextval(\'PT_A_KEY_SEQ\') from dual'
		data = select_data(select_sql)
		listen_svc_id.append(search_data('\d+',data[0]))
		# 인서트 쿼리를 생성하여 데이터베이스에 인서트
		insert_sql = 'insert into pt_listen_service(listen_svc_id,listen_addr_id,instance_id) values(%s,%s,%s)'%(listen_svc_id[i],listen_addr_id[i],instance_id[i])
		cursor.execute(insert_sql)

def insert_pt_prod_service(): # PT_PROD_SERVICE 테이블에 데이터 삽입
	# 사용할 전역 변수 선언
	global master_ip,master_port,master_svc
	global service_id
	global prod_id
	# 보안서비스를 생성할 제품이 마스터가 아닐 수 있으므로 해당 제품의 제품ID입력
	product_id = input('Please enter the product_id of the product to create the prod_service : ')

	# MASTER데이터베이스에 커넥션
	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()
	
	# 입력한 제품ID가 마스터에 등록이 되어있는지 확인하는 쿼리 실행
	select_linkname_sql = 'select product_id from ppmt_product where product_id=%s'%(product_id)
	tmp_id = select_data(select_linkname_sql)

	# 입력한 제품ID에 대한 정보가 마스터에 등록되어 있는지 확인
	if len(tmp_id) != 0:
		prod_id = search_data('\d+',tmp_id[0]) # 제품ID가 등록되어 있다면 제품ID를 저장
	else:
		print('Product id not found')
		exit() # 제품 ID가 없다면 제품 ID를 찾을 수 없다는 메세지 출력후 프로그램 종료

	# ID값을 생성하기 위한 SQL
	select_sql = 'select nextval(\'PT_A_KEY_SEQ\') from dual'
	data = select_data(select_sql)
	service_id = search_data('\d+',data[0])

	# 입력받은 제품 ID를 통하여 해당 제품에 보안 서비스를 추가
	prod_service_sql = 'insert into pt_prod_service(service_id,service_name,product_id,pd_svc_type) values(%s,\\\'petraAutoTest Listener\\\',%s,2)'%(service_id,prod_id)
	insert_sql = 'select * from ppmp_prod_exec_sql(0,\'%s\',0)'%(prod_service_sql)
	cursor.execute(insert_sql)

def diff_port(listen_port,listener_port): # 보안대상 포트와 중계리스너에서 사용할 포트가 겹치지 않는지 확인
	# 입력된 포트 수 만큼 반복하며 중복을 비교
	for i in range(0,len(listen_port)):
		if listen_port[i] == listener_port[i]:
			return True # 중복된 데이터가 있다면 True
	return False # 없다면 False

def insert_pact_inline_listener(): # PACT_INLINE_LISTENER 테이블에 데이터 삽입
	# 사용할 전역 변수 선언
	global master_ip,master_port,master_svc
	global listener_id
	global listen_addr_id
	global service_id
	global prod_id
	global listen_port
	listener_port=[]
	listener_id=[]

	# 마스터 데이터 베이스에 커넥션
	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()

	# 중계리스너를 생성할 제품이 설치된 IP정보를 가져와 설정
	linkname_select_sql = 'select soha_link from ppmt_product where product_id=%s'%(prod_id)
	cursor.execute(linkname_select_sql)
	linkname = cursor.fetchall()
	linkname = search_data('\w+_\d+',linkname[0])
	
	ip_select_sql = 'select host from pt_database_link_info where link_name=\'%s\''%(linkname)
	cursor.execute(ip_select_sql)
	listener_ip = cursor.fetchall()
	listener_ip = search_data('(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',listener_ip)

	# 중계리스너로 사용할 포트 생성
	listener_port = create_random_port(len(listen_port))
	
	# 중복이 발생하지 않을때까지 무한 루프
	while True:
		if diff_port(listen_port,listener_port):
			listener_port = create_random_port(len(listen_port)) # 중복이 발생한 포트가 있다면 중계리스너로 사용할 포트 전체 재생성
		else:
			break # 중복이 발생하지 않을 경우 무한 루프 종료

	# 지원되는 DBMS의 수만큼 반복하여 ID값을 생성 후에 데이터 인서트
	for i in range(0,len(listen_addr_id)):
		# 지원되는 DBMS의 수만큼 반복하여 ID값을 생성
		select_sql = 'select nextval(\'PT_A_KEY_SEQ\') from dual'
		data = select_data(select_sql)
		listener_id.append(search_data('\d+',data[0]))
	
		# 인서트 쿼리 생성 후 인서트
		insert_sql = 'insert into pact_inline_listener(active_flag,listener_id,service_id,test_mode,bridge_flag,listen_addr_id,listen_ip,listen_port)'
		insert_sql += ' values(0,%s,%s,0,0,%s,\'%s\',%s)'%(listener_id[i],service_id,listen_addr_id[i],listener_ip,listener_port[i])
		cursor.execute(insert_sql)

def update_param(): # DG_SYS_PARAM의 START_RELAY_SERVERS값을 기본 1에서 10으로 업데이트
	# 사용할 전역 변수 선언
	global master_ip,master_port,master_svc
	global prod_id

	# 데이터베이스 커넥션
	conn = connection_database(master_ip,master_port,master_svc)
	cursor = conn.cursor()

	# 중계리스너가 생성된 제품의 파라미터를 업데이트
	sql = 'select * from ppmp_prod_exec_sql(%s,\'UPDATE DG_SYS_PARAM SET(VAL_NUMBER, LAST_UPDATE) = (10, sysdate()) WHERE PARAM_NAME = \\\'START_RELAY_SERVERS\\\'\',0)'%(prod_id)
	cursor.execute(sql)

def main():
	#전역 변수 선언 및 초기화
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

	#함수 호출
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
