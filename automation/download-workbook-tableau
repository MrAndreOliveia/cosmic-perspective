####
# This script contains functions that download a workbook
# from a Tableau server default project, using pre-defined input variables.
# 
# Python 2.7.9 or late
#
# Run the script in terminal by entering:
#   python download_workbook.py <server_address> <username>
####

from version import VERSION
import requests # Contains methods used to make HTTP requests
import xml.etree.ElementTree as ET # Contains methods used to build and parse XML
import sys
import math
import getpass
import ssl
import os
import re

import zipfile # Necessary to unzip TWBX files 

# You will need to search for the section: INITIALIZATION to enter the technical user name and password.


# The namespace for the REST API is 'http://tableausoftware.com/api' for Tableau Server 9.0
# or 'http://tableau.com/api' for Tableau Server 9.1 or later
xmlns = {'t': 'http://tableau.com/api'}


ssl._create_default_https_context = ssl._create_unverified_context


def _encode_for_display(text):
    """
    Encodes strings so they can display as ASCII in a Windows terminal window.
    This function also encodes strings for processing by xml.etree.ElementTree functions.
    Returns an ASCII-encoded version of the text.
    Unicode characters are converted to ASCII placeholders (for example, "?").
    """
    return text.encode('ascii', errors="backslashreplace").decode('utf-8')


# ---------------Sign In-------------------
def sign_in(server, username, password, site=""):
    url = server + "/api/2.2/auth/signin"

    # Builds the request
    xml_request = ET.Element('tsRequest')
    credentials_element = ET.SubElement(xml_request, 'credentials', name=username, password=password)
    ET.SubElement(credentials_element, 'site', contentUrl=site)
    xml_request = ET.tostring(xml_request)

    # Make the request to server
    server_response = requests.post(url, data=xml_request,  verify=False)
    

    # ASCII encode server response to enable displaying to console
    server_response = _encode_for_display(server_response.text)

    # Reads and parses the response
    parsed_response = ET.fromstring(server_response)

    # Gets the auth token and site ID
    token = parsed_response.find('t:credentials', namespaces=xmlns).get('token')
    site_id = parsed_response.find('.//t:site', namespaces=xmlns).get('id')
    user_id = parsed_response.find('.//t:user', namespaces=xmlns).get('id')
    
    return token, site_id, user_id
 

    

def sign_out(server, auth_token):
    """
    Destroys the active session and invalidates authentication token.
    'server'        specified server address
    'auth_token'    authentication token that grants user access to API calls
    """
    url = server + "/api/2.2/auth/signout"
    server_response = requests.post(url, headers={'x-tableau-auth': auth_token}, verify=False)
    return



def main():
    ##### STEP 0: INITIALIZATION #####
    # Please enter you credentials
    server = "https://tableau.ecb.de/"
    username = "USERNAME" 
    password ="PASSWORD"

    ##### STEP 1: Sign in #####
    print("\n1. Signing in as " + username)
    auth_token, site_id, user_id, = sign_in(server, username, password)
    print("this is the token: "+auth_token)
    print("this is site id: "+site_id)
    print("this is the user id: "+user_id)
 


    # ---------------START DOWNLOAD -------------------
    # Please choose the server in production or in acceptance
    # Please change the workbook id, which is after https://tableau.ecb.de/api/2.2/sites/d0356794-bb9d-4c5c-b43d-ec384a2baf5a/workbooks/


    print("---Start Query---")
    url = server+"api/2.2/sites/d0356794-bb9d-4c5c-b43d-ec384a2baf5a/workbooks/751dfcbe-e58b-48e8-8d7d-498d58a7dacc/content".format(site_id)
    server_response3 = requests.get(url, headers={'x-tableau-auth': auth_token}, verify=False)


    print("---Download File---")
    filename = re.findall(r'filename="(.*)"', server_response3.headers['Content-Disposition'])[0]
    with open(filename, "wb") as f:
    	f.write(server_response3.content)
    print(filename)


    print("---Check if packaged workbook---")    
    if filename.find("x"):
    	zf = zipfile.ZipFile(filename, 'r')
    	print(zf.namelist())
    	for file in zf.namelist():
     		if file.endswith(".twb"):
     			zf.extract(file)	
    			zf.close()	
    		else:
    			zf.close()
			pass
    	zf.close()
    else:
    	zf.close()
	print("No TWBX file found. No unzip necessary.")
    

# ---------------Sign Out-------------------
    print("\n5. Signing out and invalidating the authentication token")
    sign_out(server, auth_token)


if __name__ == "__main__":
    main()
