"""
		Title: relevant_loads.py        					 										 
		Description: Compares the underlying data of a Tableau report to the template formulas
		Creation Date: 27-Jun 2018		
		Last Update: 29-Jun 2018																	 
		Author: André Oliveira																	 
"""
import webbrowser
import pandas as pd
import os
import csv
import time
import datetime
import sys
import numpy as np
import cx_Oracle
import sys


def delete_old_versions(file_path,step_number):
	if os.path.exists(file_path) == True:
		os.remove(file_path)
		print('Old version deleted.')

		step_name = 'Delete old data'
		check = 'OK'		
		test_logs = write_log(step_number,step_name,check)


def get_data(tableauServer,tableauProject,tableauWorkbook,tableauView,format,filters): 

	url = tableauServer + '/' + tableauProject + '/views/' + tableauWorkbook + '/' + tableauView + '.' + format + '?:embed=y&' + filters

	#url = 'https://t-star-tableau.escb.eu/t/STAR/views/10_NII-UnderlyingDataTable/RelevantSubmissionLoadIDs.csv?:embed=y&Bank%20Name=PTCGD'

	chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

	webbrowser.get(chrome_path).open(url)

		
def read_tableau_data(file_path,filter_column,filter_var,filter_output):

	if os.path.exists(file_path) == True:
		df_loadid = pd.read_csv(file_path)
		loadid = df_loadid.loc[(df_loadid['Exercise'].isin(['STAR-2018'])) & (df_loadid[filter_column] == filter_var), filter_output]
		
		#print(loadid)
		if filter_output == 'Load ID':
			step_number = 3
			step_name = 'Read LoadID'
			check = 'OK'		
			test_log = write_log(step_number,step_name,check)	
		
		elif filter_output == 'Train ID':			
			step_number = 8
			step_name = 'Read TrainID'
			check = 'OK'		
			test_log = write_log(step_number,step_name,check)	
	else:	
		sys.exit

	return loadid	

	
def write_log(step_number,step_name,check):
	with open('log.csv', 'a') as log:	
		t = datetime.datetime.now()
		t = t.strftime('%Y-%m-%d %H:%M:%S')
		log.write("%s, %s, %s, %s \n" %(t, step_number, step_name, check))
		log.close()
		

def query_db_loadid():

	#Logging
	step_number = 4
	step_name = 'Get LoadID from Oracle database'

	username = 'USER'
	password = 'PASSWORD'
	hostname = 'HOSTNAME'
	port = 1234
	database = 'DBNAME'

	auth_string = username + '/' + password + '@' + hostname + ':' + '/' + database

	conn_str = auth_string

	try:
		db = cx_Oracle.connect(conn_str)
	
		print("Connected to the Oracle " + db.version + " database.")
	
		cur = db.cursor()
	
		sql1 = """
		Select 
		b.BANK_SHORT_NAME as Bank_Name, rl.EXERCISE as Exercise, rl.CYCLE as Submission_Cycle, 
		rl.TEMPLATE_VERSION as Template_Version, rl.RLOAD_IDENT_SHORT_NAME as Relevant_Load_Identifier, 
		rl.LOAD_ID as Sub_Load_ID
		from RELEVANT_LOAD rl join BANK b on rl.BANK_ID = b.BANK_ID
		where RLOAD_IDENT_SHORT_NAME in ('LATEST_SUBMISSION','LATEST_ACCEPTED') and Bank_short_name in ('GRALP')
		order by b.BANK_SHORT_NAME
		"""
	
		#Execute query
		#cur.execute(sql1)
	
		df_oracle = pd.read_sql(sql1, con=db)
		
		load_id = df_oracle['SUB_LOAD_ID'] 

		#Print result
		#results = cur.fetchall()

		check = 'OK'		
	
	except:
		print('Error connecting to database!')
		check = 'Fail'	
	
	finally:
		#Close cursor and connection
		#cur.close()
		db.close()		
		test_log = write_log(step_number,step_name,check)
		
	return load_id
						
		
def query_db_trainid():

	#Logging
	step_number = 9
	step_name = 'Get TrainID from Oracle database'

	username = 'STAR_ST2018_DATA'
	password = 'STAR_ST2018_DATA'
	hostname = 'xt02tst-scan.tadnet.net'
	port = 1521
	database = 't4srstar_svc.tst.tns'

	auth_string = username + '/' + password + '@' + hostname + ':' + '/' + database

	#conn_str = u'STAR_ST2018_DATA/STAR_ST2018_DATA@xt02tst-scan.tadnet.net:1521/t4srstar_svc.tst.tns'

	conn_str = auth_string

	try:
		db = cx_Oracle.connect(conn_str)
	
		print("Connected to the Oracle " + db.version + " database.")
	
		cur = db.cursor()

		sql2 = """
		Select distinct
		b.BANK_SHORT_NAME as Bank_Name, rl.EXERCISE as Exercise, 
		rl.RLOAD_IDENT_SHORT_NAME as Relevant_Load_Identifier, 
		cast(rl.TRAIN_ID as varchar2(255)) as Train_ID,
		evt.view_type_short_name
		from RELEVANT_LOAD rl 
		join BANK b on rl.BANK_ID = b.BANK_ID
		join E_VIEW_TYPE evt on rl.train_view_type_id = evt.view_type_id
		where RLOAD_IDENT_SHORT_NAME in ('LATEST_BSA')
		and Bank_short_name in ('GRALP')
		order by b.BANK_SHORT_NAME
		"""
	
		#Execute query
		#cur.execute(sql1)
	
		df_oracle = pd.read_sql(sql2, con=db)
		
		train_id = df_oracle['TRAIN_ID'] 
		

		#Print result
		#results = cur.fetchall()

		check = 'OK'	
	
	#except:
	#	print('Error connecting to database!')
	
	finally:
		#Close cursor and connection
		#cur.close()
		db.close()
		test_log = write_log(step_number,step_name,check)
			
	return train_id
										

def compare_data_load(load_id_tableau, load_id_oracle):
	
	compare = np.allclose(load_id_tableau, load_id_oracle, atol=1e-3)
	step_number = 5
	step_name = 'Compare Load IDs'
	if compare == True:
		check = 'OK'	
	else:
		check = 'Fail'
	test_log = write_log(step_number,step_name,check)	

	return compare

	
def compare_data_train(train_id_tableau, train_id_oracle):
	
	#Sort datasets
	sort_train_id_tableau = train_id_tableau.sort_values(ascending = True).reset_index(drop = True)
	sort_train_id_oracle = train_id_oracle.sort_values(ascending = True).reset_index(drop = True)
	
	#Check if dataset are the same
	compare_data_train = sort_train_id_tableau.isin(sort_train_id_oracle)
	#print(compare_data_train)
	
	check_compare = compare_data_train.all()
	#print(check_compare)
	
	step_number = 10
	step_name = 'Compare Train IDs'
	if check_compare == True:
		check = 'OK'	
	else:
		check = 'Fail'
	test_log = write_log(step_number,step_name,check)	

	return check_compare

	
def main():
	##### STEP 0: INITIALIZATION LOADID #####
	tableauServer = 'https://t-star-tableau.escb.eu/t'
	tableauProject = 'STAR'
	tableauWorkbook = '13_RelevantLoadsReport'
	tableauView = 'RelevantSubmissionLoadIDs'
	format = 'csv'
	filters = 'CYCLE=1&BANK_SHORT_NAME=GRALP'
	
	
	file_name = tableauView + '.' + format
	
	file_path = os.path.join(os.path.expanduser('~'),'Downloads',file_name)
	
	#username = 'STAR_USER_33'
	#password = 'Frank123!'

	##### STEP 1: DELETE OLD VERSIONS OF DATA #####	
	print("\n1. Checking for old versions of data...")
	step_number = 1
	old_data = delete_old_versions(file_path,step_number)
	
	##### STEP 2: GET LOAD ID FROM TABLEAU #####
	print("\n2. Getting data from " + tableauView + ". Please input the Tableau credentials and the download will start automatically...")
	csv_data_loadid = get_data(tableauServer,tableauProject,tableauWorkbook,tableauView,format,filters)

	##### STEP 3: READ LOAD ID FROM TABLEAU #####	
	while not os.path.exists(file_path):
		time.sleep(1)
	if os.path.exists(file_path): 
		print("\n3. Reading data from file " + tableauView + "." + format + "...")
		step_number = 2
		step_name = 'Get data from Tableau report'
		check = 'OK'		
		test_log = write_log(step_number,step_name,check)
		
		filter_column = 'Relevant Load Identifier'
		filter_var = 'LATEST_SUBMISSION'
		filter_output = 'Load ID'
		load_id_tableau = read_tableau_data(file_path,filter_column,filter_var,filter_output)
		print(load_id_tableau)
	else:
		raise ValueError('There is no file in directory!')	
	
	##### STEP 4: READ LOAD ID FROM ORACLE #####	
	print("\n4. Reading data from oracle...")
	load_id_oracle = query_db_loadid()

	##### STEP 5: COMPARE LOAD ID OUTPUTS #####	
	print("\n5. Comparing data from the bank template and the Tableau report... ")
	print(compare_data_load(load_id_tableau, load_id_oracle))
	
	##### STEP 6: INITIALIZATION TRAINID #####
	tableauView = 'RelevantBSATrainIDs'
	
	file_name = tableauView + '.' + format
	
	file_path = os.path.join(os.path.expanduser('~'),'Downloads',file_name)
	
	#username = 'STAR_USER_33'
	#password = 'Frank123!'

	##### STEP 7: DELETE OLD VERSIONS OF DATA #####	
	print("\n6. Checking for old versions of data...")
	step_number = 6
	old_data = delete_old_versions(file_path,step_number)
	
	##### STEP 8: GET TRAIN ID FROM TABLEAU #####
	print("\n7. Getting data from " + tableauView + ". Please input the Tableau credentials and the download will start automatically...")
	csv_data_trainid = get_data(tableauServer,tableauProject,tableauWorkbook,tableauView,format,filters)
	
	##### STEP 9: READ LOAD ID FROM TABLEAU #####	
	while not os.path.exists(file_path):
		time.sleep(1)
	if os.path.exists(file_path): 
		print("\n8. Reading data from file " + tableauView + "." + format + "...")
		step_number = 7
		step_name = 'Get data from Tableau report'
		check = 'OK'		
		test_log = write_log(step_number,step_name,check)
		
		filter_column = 'Relevant Load Identifier'
		filter_var = 'LATEST_BSA'
		filter_output = 'Train ID'
		train_id_tableau = read_tableau_data(file_path,filter_column,filter_var,filter_output)
		print(train_id_tableau)
	else:
		raise ValueError('There is no file in directory!')	
		
	##### STEP 10: READ TRAIN ID FROM ORACLE #####	
	print("\n9. Reading data from oracle...")
	train_id_oracle = query_db_trainid()
	print(train_id_oracle)
	
	##### STEP 11: COMPARE LOAD ID OUTPUTS #####	
	print("\n10. Comparing data from the bank template and the Tableau report... ")
	print(compare_data_train(train_id_tableau, train_id_oracle))
	
		
if __name__ == '__main__':
	main()
