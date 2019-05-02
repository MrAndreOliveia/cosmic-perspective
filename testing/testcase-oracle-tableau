"""
		Title: top_down_view.py        					 										 
		Description: Compares the underlying data of a Tableau report to the template formulas
		Creation Date: 01-Jul 2018		
		Last Update: 04-Jul 2018																	 
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

		
def read_tableau_data(file_path):
		
	df_tableau = pd.read_csv(r'C:\Users\oliveia\Downloads\OverviewTableTopDownView.csv' )
	#print(df_tableau)

	val_tableau = df_tableau.loc[(df_tableau['SCENARIO'].isin(['Adverse'])) & (df_tableau['SOURCE'] == 'Top-Down projections' ) & (df_tableau['YEAR'] == 2018), 'VALUE']
	#print(val_tableau)
	
	#if os.path.exists(file_path) == True:

	step_number = 2
	step_name = 'Get data from Tableau report'
	check = 'OK'		
	test_log = write_log(step_number,step_name,check)
	
	if os.path.exists(r'C:\Users\oliveia\Downloads\OverviewTable-TopDownView.csv') == True:	
		#df_tableau = pd.read_csv(file_path)
		#print(df_tableau)
		
		"""
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
		"""	
	else:
		sys.exit

	return val_tableau

	
def write_log(step_number,step_name,check):
	with open('log.csv', 'a') as log:	
		t = datetime.datetime.now()
		t = t.strftime('%Y-%m-%d %H:%M:%S')
		log.write("%s, %s, %s, %s \n" %(t, step_number, step_name, check))
		log.close()
		

def query_db():

	#Logging
	step_number = 3
	step_name = 'Get data from Oracle database'

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
	
		SQL1 = "call set_role_perm_for_username('RUMPELSTIELZCHEN')"
	
		SQL2 = """
	
		select bank_short_name, Exercise, Template, Val_type, view_type_short_name, Scenario, Year, value
		from v_tableau 
		where 
		(
		load_id = 
		(
			select Load_id from relevant_loads 
			where bank_short_name = 'LUBCE' 
			and relevant_load_identifier = 'LATEST_SUBMISSION'
			and exercise = 'STAR-2018'
		)
		or 
		train_id = 
		(
			select distinct train_id from relevant_loads 
			where relevant_load_identifier = 'LATEST_BSA'
			and train_view_type_short_name = 'TD'
			and submission_load_id = 
		(
			select Load_id from relevant_loads 
			where bank_short_name = 'LUBCE' 
			and relevant_load_identifier = 'LATEST_SUBMISSION'
		and exercise = 'STAR-2018'
			)
		)
		)
		and template = 'CSV_P' || chr(38) || 'L' and val_type like 'Net interest income'
		order by view_type_short_name desc, scenario, year	
		"""
	
		#Execute query
		cur.execute(SQL1)
	
		#cur.execute(SQL2)
		df_oracle = pd.read_sql(SQL2, con=db)
		
		#print(df_oracle)
		#load_id = df_oracle['SUB_LOAD_ID'] 
		
		val_oracle = df_oracle.loc[(df_oracle['SCENARIO'].isin(['Adverse'])) & (df_oracle['VIEW_TYPE_SHORT_NAME'] == 'TD' ) & (df_oracle['YEAR'] == '2018'), 'VALUE']
		#print(val_oracle)
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
		
	return val_oracle
						
					

def compare_data(value_tableau, value_oracle):
	
	value_tableau_float = pd.to_numeric(value_tableau, 'float')
	value_oracle_float = pd.to_numeric(value_oracle, 'float')
	sort_value_tableau = value_tableau_float.sort_values(ascending = True).reset_index(drop = True)
	sort_value_oracle = value_oracle_float.sort_values(ascending = True).reset_index(drop = True)
	
	compare = np.allclose(sort_value_tableau, sort_value_oracle, atol=1e-3)
	#print(compare)
	step_number = 4
	step_name = 'Compare Load IDs'
	
	if compare == True:
		check = 'OK'	
	else:
		check = 'Fail'
	test_log = write_log(step_number,step_name,check)	

	return compare



	
def main():
	##### STEP 0: INITIALIZATION #####
	tableauServer = 'https://t-star-tableau.escb.eu/t'
	tableauProject = 'STAR'
	tableauWorkbook = '08_TopDownViewReport'
	tableauView = 'OverviewTable-TopDownView'
	format = 'csv'
	filters = 'CYCLE=1&BANK_SHORT_NAME=LUBCE&PNL_CAP_ITEM=NII'
	
	file_name = tableauView + '.' + format
	
	file_path = os.path.join(os.path.expanduser('~'),'Downloads',file_name)
	
	#username = 'STAR_USER_33'
	#password = 'Frank123!'

	##### STEP 1: DELETE OLD VERSIONS OF DATA #####	
	print("\n1. Checking for old versions of data...")
	step_number = 1
	old_data = delete_old_versions(file_path,step_number)
	
	##### STEP 2: GET DATA FROM TABLEAU #####
	print("\n2. Getting data from " + tableauView + ". Please input the Tableau credentials and the download will start automatically...")
	csv_data = get_data(tableauServer,tableauProject,tableauWorkbook,tableauView,format,filters)


	##### STEP 3: READ DATA FROM TABLEAU #####		
	print("\n3. Reading data from file " + tableauView + "." + format + "...")	
	value_tableau = read_tableau_data(file_path)
	
	##### STEP 4: READ DATA FROM ORACLE #####	
	print("\n4. Reading data from oracle...")
	value_oracle = query_db()	

	print(value_tableau)
	print(value_oracle)
	
	##### STEP 5: COMPARE OUTPUTS #####	
	print("\n5. Comparing data from the bank template and the Tableau report... ")
	print(compare_data(value_tableau, value_oracle))
	


		
if __name__ == '__main__':
	main()
