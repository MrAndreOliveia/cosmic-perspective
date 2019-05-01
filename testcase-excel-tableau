"""
		Title: correct_data.py        					 										 
		Description: Compares the underlying data of a Tableau report to the template formulas
		Creation Date: 4-Jun 2018		
		Last Update: 8-Jun 2018																	 
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


def delete_old_versions(file_path):
	if os.path.exists(file_path) == True:
		os.remove(file_path)
		print('Old version deleted.')
		step_number = 1
		step_name = 'Delete old data'
		check = 'OK'		
		test_logs = write_log(step_number,step_name,check)


def get_data(tableauServer,tableauProject,tableauWorkbook,tableauView,format,filters): 

	url = tableauServer + '/' + tableauProject + '/views/' + tableauWorkbook + '/' + tableauView + '.' + format + '?:embed=y&' + filters

	#url = 'https://t-star-tableau.escb.eu/t/STAR/views/10_NII-UnderlyingDataTable/RelevantSubmissionLoadIDs.csv?:embed=y&Bank%20Name=PTCGD'

	chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

	webbrowser.get(chrome_path).open(url)

		
def read_data(file_path):

	if os.path.exists(file_path) == True:
		df = pd.read_csv(file_path)
		#print(df)
		
		baseline_value_tableau = df['Weighted Value (by Rwa Lr Expo) trigger']
		#print(baseline_value_tableau)
		
		step_number = 3
		step_name = 'Read data from csv file'
		check = 'OK'		
		test_log = write_log(step_number,step_name,check)	
	else:	
		sys.exit
		
	return baseline_value_tableau

	
def write_log(step_number,step_name,check):
	with open('log.csv', 'a') as log:	
		t = datetime.datetime.now()
		t = t.strftime('%Y-%m-%d %H:%M:%S')
		log.write("%s, %s, %s, %s \n" %(t, step_number, step_name, check))
		log.close()
		

def read_template(template_path):

	sheet_name = 'CSV_CAP'
	if os.path.exists(template_path) == True:
		df_template = pd.read_excel(template_path, sheetname = sheet_name)
		#print(df_template)
		
		df_template_P = df_template['Unnamed: 13']
		#print(df_template_P)
		
		baseline_value_template = df_template_P.iloc[66]
		#print(baseline_value_template)

		step_number = 4
		step_name = 'Read data from bank template'
		check = 'OK'		
		test_log = write_log(step_number,step_name,check)			
	
	else:	
		sys.exit
	
	return baseline_value_template
		

def compare_data(template_value, tableau_value):
	
	compare = np.allclose(template_value, tableau_value, atol=1e-3)
	step_number = 5
	step_name = 'Compare bank template and Tableau report'
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
	tableauWorkbook = '02_RiskDriverReport'
	tableauView = 'CET1RatioandLeverageRatio-HeatMapandBoxPlot-PeerComparison'
	format = 'csv'
	filters = 'CYCLE=1&BANK_SHORT_NAME=GRALP&View=Bank%20View&Ratio%20Type=CET1%20Ratio%20TR'
	
	file_name = tableauView + '.' + format
	template_name = 'Bank_GRALP.xlsx'
	
	file_path = os.path.join(os.path.expanduser('~'),'Downloads',file_name)
	template_path = os.path.join(os.path.expanduser('~'),'Downloads',template_name)
	
	#username = 'STAR_USER_33'
	#password = 'Frank123!'

	##### STEP 1: DELETE OLD VERSIONS OF DATA #####	
	print("\n1. Checking for old versions of data...")
	old_data = delete_old_versions(file_path)
	
	
	##### STEP 2: GET TABLEAU DATA #####
	print("\n2. Getting data from " + tableauView + ". Please input the Tableau credentials and the download will start automatically...")
	csv_data = get_data(tableauServer,tableauProject,tableauWorkbook,tableauView,format,filters)

	##### STEP 3: READ TABLEAU DATA #####	
	while not os.path.exists(file_path):
		time.sleep(1)
	if os.path.exists(file_path): 
		print("\n3. Reading data from file " + tableauView + "." + format + "...")
		step_number = 2
		step_name = 'Get data from Tableau report'
		check = 'OK'		
		test_log = write_log(step_number,step_name,check)
		
		tableau_value = read_data(file_path)
		print(tableau_value)
	else:
		raise ValueError('There is no file in directory!')	
	
	##### STEP 4: READ TEMPLATE DATA #####	
	print("\n4. Reading data from file " + template_name + "...")
	template_value = read_template(template_path)
	print(template_value)

	##### STEP 5: COMPARE OUTPUTS #####	
	print("\n5. Comparing data from the bank template and the Tableau report... ")
	print(compare_data(template_value, tableau_value))

	
		
if __name__ == '__main__':
	main()
