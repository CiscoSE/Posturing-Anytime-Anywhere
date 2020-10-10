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


import json
import requests
import Environment
import Credentials
import time
import os
import sys
import GetSetGroup

####################################################################################################  
# This fundtion will do follwoing tasks
# Reads Endpoints form the Child Group.
# Send a Isolation signal to all tje End points.
# Also writes the End point name, guid, status of Isolation and Unlock code in a file.
# Pls update the code if you would like to Ioslate in batches.
####################################################################################################  


def isolateEP():
    isolationdata={}
    isolationdata['node']=[]   
    ParentGroupName = input(" Enter the Parent Group name to check the Complaince :")
    if not os.path.exists('AMPPosture'):
        #os.makedirs('AMPPosture')
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print('No Complaince process running on this Group. Please check')
        sys.exit('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    os.chdir('AMPPosture')
    #with open(ParentGroupName+ "/posturedetails.txt", "r") as outfile:
    #    posturedetails=json.load(outfile)
    
    Pdet=open(ParentGroupName+"/posturedetails.txt", "r")
    posturedetails=json.load(Pdet)
    #Pdet.close()

    url = Credentials.AMP_Cloud + '/v1/computers' + "?group_guid[]=" + posturedetails['ChildGruopID']
    response = Environment.AMPSession.get(url)

    response_json = response.json()
    #print (json.dumps(response_json,indent=2))
    metadata=response_json['metadata']
    results=metadata['results']
    if (results['total'] == 0 ):
        #GetSetGroup.RemoveChildGroup(posturedetails['ChildGruopID'])
        print ("\n***************************************************************************")
        print("\n  No End Points in the Group. Trying to Delete the Child Group")
        GetSetGroup.RemoveChildGroup(posturedetails['ChildGruopID'])
        sys.exit("\n*************************************************************************")
        
    for EP in response_json['data']:  
            #print(json.dumps (EP,indent=2))
            #print('is it false',EP ['isolation']['available'])
            if(EP ['isolation']['available']== False):
                print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                print(' \"Allow Endpoint Isolate\" Option is not Enabled the group policy')
                print(' \n Removed the Child Group Created.')
                sys.exit('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            else:
                isolationurl= Credentials.AMP_Cloud + '/v1/computers/'+ EP['connector_guid']+ '/isolation'
                isolationresponse=Environment.AMPSession.get(isolationurl)
                isolationresult= isolationresponse.json()['data']
                #print(isolationresult)
                if (isolationresult['status']=='not_isolated'):
                    isolationresponse=Environment.AMPSession.put(isolationurl)
                    isolationresult= isolationresponse.json()['data']
                    #print("\nIsolation Response: ",json.dumps(isolationresult,indent=2))
                    #print('status '+ isolationresult['status'],'unlock_code'+ isolationresult['unlock_code'])
                    print('Sent an isolate signal to Endpoint: '+ EP['hostname'] + ' Present status of Endpoint is: '+ isolationresult['status'])
                    #isolationdata['node'].append({'hostname': EP['hostname'],'AMPID':EP['connector_guid'],'status':isolationresult['status'],'unlock_code': isolationresult['unlock_code']})
                else:
                    print('Not able to isolate Endpoint: '+ EP['hostname'] + ' Present status of Endpoint is: '+ isolationresult['status'])
                isolationdata['node'].append({'hostname': EP['hostname'],'AMPID':EP['connector_guid'],'status':isolationresult['status'],'unlock_code': isolationresult['unlock_code']})
    with open(ParentGroupName+"/isolationdata.txt", 'w+') as outfile:        
        json.dump(isolationdata,outfile)          
   
    return()

isolateEP()
