""".

Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""


import requests
import json
import time
import base64
import Credentials
import ComputerList
import Orbital_token
import Environment
import sys
#import Orbital_token
#import re

##################### Query ##########################
####################################################################################################  
# This fundtion will do follwoing tasks
# WIll read the Nodelist file created in the NodeBatch function.
# Every line in this file will have 25 Endpoints.
# Will execute Orbital Query per batch and stores the JobIDs in file.
 ####################################################################################################  

def QueryOrbital():
 access_token=Orbital_token.GenerateToken()
 NodeList= open(Environment.ParentGroupName+'/NodeList.txt', "r")
 JobIDList= open(Environment.ParentGroupName+"/OrbitalJobIDList.txt","w+")
 # Headers to send with POST
 headers = {
     'Authorization':'Bearer {}'.format(access_token),
     'Content-Type':'application/json', 'Accept':'application/json'
 }
 
 # Craft query/job expiry, must be 60 seconds or longer
 timer_expiry = int(time.time())+60
 #NodeList= open('NodeList.txt', "r")
 
 pr = Environment.ProgramtoSearch
 query = "SELECT name, version, install_location, install_source, language, publisher, uninstall_string, identifying_number  FROM programs WHERE name LIKE '%" + pr +"%'";
 count =1
 try:
    for line in NodeList:
        Nodeline=line.rstrip()
        if (Nodeline ==''):
            print ('########################################################')
            print(' No Endpoints in NodeList file, so not Exucuting the Query')
            sys.exit('######################################################')
        payload = {
            "osQuery":[{"sql": query}],
            "nodes": Nodeline.split(','),
            #"nodes": ["host:DESKTOP-H0NE6U0", "host:DESKTOP-ABC1CA8"],
            "expiry": timer_expiry,
        }
        # Format Payload before and after
        payload = json.dumps(payload)
        #print(payload)
        response = requests.post(Credentials.query_url, headers=headers, data=payload)
        count=count+1
        #Display response code and json formatted result
        #print("\nHTTP response code: ", response)
        if (response.status_code == 400) :
            print ('###################################################')
            print(' No Endpoints in NodeList file or currupted file')
            sys.exit('##################################################')
        #Store Response in dictionary for later parsing
        response_results = response.json()
        JobIDList.write(response_results['ID'])
        # Print JOB ID and Expiry
        print("Here is the Job ID: ", response_results['ID'])
        print("Epoch Job Expiry (60 seconds): ", response_results['expiry']) 
        ###################### END ##############################
 except requests.exceptions.HTTPError as err:
        print('catch the error\n')
        print ("Error in connection --> "+str(err))
 NodeList.close()
 JobIDList.close()
 print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
 print(' Done with sending the Query to End Points and JOBIDs are listed in the \"OrbitalJobIDList.txt\"')
 print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

 return ()

#QueryOrbital()