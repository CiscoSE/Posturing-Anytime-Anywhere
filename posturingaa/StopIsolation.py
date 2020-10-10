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
##################### Query ##########################
####################################################################################################  
# This function will do following tasks
# Take Hostname for validating the Posture
# Get the group info from AMP cloud and get the Group ID and program name form Posturing.txt file
# Run Orbital query on host and check for the installation status from Job ID created.
# If installed, stop isolation and move the end point to Parent group.
# If not continue in Isolated status.
 ####################################################################################################  


import json
import requests
import Environment
import string
import sys
import os
import Orbital_token
import time
import Credentials
from urllib3.exceptions import InsecureRequestWarning
def Stop():
    Endpointname = input(" Enter the Host name to validate the Complaince :")
    if not os.path.exists('AMPPosture'):
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print('NO Posturing was yet done. Please don not use this untill you AMP Endpoint client shows Isolated status')
        sys.exit('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    #os.makedirs('AMPPosture')
    os.chdir('AMPPosture')
    #Environment.ProgramtoSearch = input("Enter the software would like to check installation status :")
    #Endpointname='DESKTOP-H0NE6U0'
    #session = requests.session()

    #session.auth = (Credentials.AMP_client_id,Credentials.AMP_api_key)
    url= Credentials.AMP_Cloud + '/v1/computers/' 

    url = Credentials.AMP_Cloud + '/v1/computers' + "?hostname[]="+ Endpointname 
    ParentGroupName=''
    response = Environment.AMPSession.get(url)
    response_json = response.json()
    #print(json.dumps(response_json,indent=2))
    name=response_json['data']
    for cu in name:
        #print(na['policy']['name'])
        if (Endpointname == cu['hostname']):
            ParentGroupName= cu['policy']['name']
    if (ParentGroupName == ''):
            print('\n**********************************************************************')
            print('\nCheck your Hostname, if problem persist please contact Administrator')
            sys.exit('\n*******************************************************************')        
    #print('I am in Stop Isolation   ' + ParentGroupName)
    Pdet=open(ParentGroupName+"/posturedetails.txt", "r")
    posturedetails=json.load(Pdet)
    #ParentGroupName= string(Groupname[0:-11])
    #print (ParentGroupName)
    access_token=Orbital_token.GenerateToken()
    # Headers to send with POST
    headers = {
     'Authorization':'Bearer {}'.format(access_token),
     'Content-Type':'application/json', 'Accept':'application/json'
    }
 
    # Craft query/job expiry, must be 60 seconds or longer
    timer_expiry = int(time.time())+60
   
    MoveGroupParams={"group_guid":posturedetails['ParentGroupID']}
    pr = "mcafee"
    query = "SELECT name, version, install_location, install_source, language, publisher, uninstall_string, identifying_number  FROM programs WHERE name LIKE '%" + pr +"%'";
   
    payload = {
        "osQuery":[{"sql": query}],
        "nodes": ["host:"+ Endpointname],
        #"nodes": ["host:DESKTOP-H0NE6U0", "host:DESKTOP-ABC1CA8"],
        "expiry": timer_expiry,
    }
    # Format Payload before and after
    payload = json.dumps(payload)
    #print(payload)
    try:
        response = requests.post(Credentials.query_url, headers=headers, data=payload)
    
        #Display response code and json formatted result
        #print("\nHTTP response code: ", response)
 
        #Store Response in dictionary for later parsing
        response_results = response.json()
        #print(response_results)
        if (response.status_code == 400):
            print('\n**********************************************************************')
            print('\nCheck your Hostname, if problem persist please contact Administrator')
            sys.exit('\n*******************************************************************')
        JobID= response_results['ID']  
        ### Read the result of the Job executed in the last step. Query will run on one Endpoint
        ### If the result is not "none" then the Endpoint has the software installed. So we can move the system to Parent group.

        # URL to query
        job_url = 'https://orbital.apjc.amp.cisco.com/v0/jobs/{}/results'.format(JobID)
        #print("Completed URL: ", job_url)
    
        # Send GET
        job_request = requests.get(job_url, headers=headers)
        job_results=job_request.json()
        if (job_results['results']== None ):
            print ("\n*************************************************************************************************************")
            print("\n  Sorry Your End Point is not achived the complient status. Please install  " + pr+ " and validate once again")
            sys.exit("\n***********************************************************************************************************")
    
        # Get the AMP connector ID coresponding to Endpoint name give from the EPdetails file 
        # Search for earvy line and match the hostname

        EPListFile=open(ParentGroupName+"/EPdetails.txt", "r")          
        EPdata=json.load(EPListFile)
        for node in EPdata['node']:
                if(Endpointname == node['hostname']):
                     print ('Moving this Endpoint to parent group- As this has the required software')
                     response = Environment.AMPSession.patch(url+'/'+ node['connector_guid'] , params=MoveGroupParams)
                     AMPID= node['connector_guid']
                     print (response)
         #### End of logic to get eh connector ID

        #### Find the present status of the Endpoint and if it "Isolate" Stop Isolating and move the EP to Parent Group
        ### Need to change the follwoing code.
        url= Credentials.AMP_Cloud + '/v1/computers/' 
        for EP in response_json['data']:   
               isolationurl= Credentials.AMP_Cloud + '/v1/computers/'+ EP['connector_guid']+ '/isolation'
               isolationresponse=Environment.AMPSession.get(isolationurl)
               isolationresult= isolationresponse.json()['data']
               if(isolationresult['status']=='isolated'):
                   isolationresponse=Environment.AMPSession.delete(isolationurl)
                   isolationresult= isolationresponse.json()['data']
                   #print("\nIsolation Response: ",json.dumps(isolationresult,indent=2))
                   print('Isolation status '+ isolationresult['status'],'unlock_code'+ isolationresult['unlock_code'])
                   #isolationdata['node'].append({'hostname': EP['hostname'],'AMPID':EP['connector_guid'],'status':isolationresult['status'],'unlock_code': isolationresult['unlock_code']})
                   response = Environment.AMPSession.patch(url+'/'+ EP['connector_guid'] , params=MoveGroupParams)
               else:
                   if(isolationresult['status']=='not_isolated'):
                       print('\n********************************************************************************************************************')
                       print('\n Your End Point: '+ EP['hostname'] + ' is not in Isolation Status. Present status of Endpoint is: '+ isolationresult['status'])
                       print('\n********************************************************************************************************************')
                   else:
                       print('\n********************************************************************************************************************')
                       print('\n Not able to Stop isolate Endpoint: '+ EP['hostname'] + ' Present status of Endpoint is: '+ isolationresult['status'])
                       print('\n********************************************************************************************************************')
    except requests.exceptions.HTTPError as err:
        print('catch the error\n')
        print ("Error in connection --> "+str(err))
    return()               
Stop()