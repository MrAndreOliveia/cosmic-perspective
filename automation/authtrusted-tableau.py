###
# Script to automate the generation of a trusted
# authentication ticket to access the Tableau Server
# without input of username and password
###

import requests  
  
# replace these with configData  
tabServer = 'https://tableau.ecb.de/'  
tabUser = 'USERNAME'  
passwd = 'PASSWORD'
viewname = '/views/DataInventory/Home'
url = tabServer + viewname
  
# get the ticket ID  
r = requests.post(tabServer, data={'username': tabUser,'password': passwd}, verify=False)  

print(r.status_code) 


# get the ticket ID  
ra = requests.get(url, verify=False)  

print(ra.status_code) 
