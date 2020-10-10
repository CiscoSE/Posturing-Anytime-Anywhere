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
#import OrbitalQuery
import Orbital_token
import Environment
import sys

####################################################################################################  
# This fundtion will do follwoing tasks
# Reads the JobIDs form the file.
# Retrives all the endpoints results from each jobid.
# If the EP is aviable on the JobID then the given software is installed on the EP.
# will move these EPs to Parent group
# By the en of function, the Child group will have EPs without software or not acive at the time of query.
####################################################################################################  



def GetJobResults():

    batchnumber=1
    JobidList= open(Environment.ParentGroupName+"/OrbitalJobIDList.txt",'r')
    token=Orbital_token.GenerateToken()
    isolationdata={}
    isolationdata['node']=[]
    #with open('isolationdata.txt', 'w+') as outfile:
    #    isolationdata['node'].append({'hostname':'','AMPID':'','status':'','unlock_code':''})

    EPListFile=open(Environment.ParentGroupName+"/EPdetails.txt", "r")          
    EPdata=json.load(EPListFile)
    #Jobid = QueryOrbital()
    MoveGroupParams={"group_guid":Environment.ParentGroupID}
    #print(MoveGroupParams)
    url= Credentials.AMP_Cloud + '/v1/computers/' 
   
    linenumber=1
    for line in JobidList:
        if(linenumber < batchnumber):
            linenumber=linenumber+1
            #print(line)
        else:
            if (linenumber == batchnumber):
                Jobid=line
                #print("This is the Line", line)
                break
    
    # URL to query
    job_url = 'https://orbital.apjc.amp.cisco.com/v0/jobs/{}/results'.format(Jobid)
    #print("Completed URL: ", job_url)
 
    # Headers
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json', 'Accept': 'application/json'
    }
 
    # Send GET
    job_request = requests.get(job_url, headers=headers)
    
    # Print Results
    #print("HTTP Response Code: ", job_request)
    #print("Job Response: ", job_request.json())
 
    # Store response for later use
    job_results = job_request.json()
    #print("Job Response: ",json.dumps(job_results,indent=2))
    #print("kiran",job_results['results'])
    if (job_results['results']== None ):
        print ("\n*******************************************************************************************************")
        print("\n  No End Points in the JobID. Either all computers are Non complaint or Not active at the time of Query.")
        sys.exit("\n*****************************************************************************************************")
    
    for j in job_results['results']:
       #print (j['hostinfo']['hostname'])
       for node in EPdata['node']:
            if(j['hostinfo']['hostname'] == node['hostname']):
                print ('Moving Endpoint '+ node['hostname'] + ' to Parent group - As this has the required software')
                response = Environment.AMPSession.patch(url+'/'+ node['connector_guid'] , params=MoveGroupParams)
                #print (response)
    
    JobidList.close()    
    EPListFile.close()  
    print ("\n*******************************************************************************************************")
    print("\n  All Compliant end points are in Group : "+Environment.ParentGroupName )
    print("\n  All Non Compliant end points are in Group : "+Environment.ChildGroupName )
    print('\n Now you can use the Isolate.py to start ioslation process')
    
    return()

#GetJobResults()






    