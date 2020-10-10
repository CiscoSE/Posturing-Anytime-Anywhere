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
import Credentials
import Environment
import sys
import GetSetGroup
def Getlist():
    ####################################################################################################  
    # This Funtion retrive all the computers in a given group
    # If no Enpoints are in the group then removes the Child group created by earlier funtion.
    # If EPs are prsent will create a file with JSON object EP Name, AMP connector ID and Program to search.
    # Sorting the data on local mechine to aviod huge API calls to retrive data.
    #################################################################################################### 

   
    EPdetails={}
    EPdetails['node']=[]
    count = 1
    
    url = Credentials.AMP_Cloud + '/v1/computers' + "?group_guid[]=" + Environment.ParentGroupID
   
    

    response = Environment.AMPSession.get(url)

    response_json = response.json()
    #print (response_json)
    metadata=response_json['metadata']
    results=metadata['results']
    #print('\nChild ID is now '+ Environment.ChildGroupID)
    if (results['total'] == 0 ):
        GetSetGroup.RemoveChildGroup(Environment.ChildGroupID)
        print ("\n**************************************************************")
        print("\n  No End Points in the Group Given. Reverted the Changes made.")
        sys.exit("\n************************************************************")
    
    for computer in response_json['data']:
        if(computer ['isolation']['available']== False):
                #print('\nChild ID'+ Environment.ChildGroupID)
                
                print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                print(' \"Allow Endpoint Isolate\" Option is not Enabled the group policy')
                print(' \n Removed the Child Group Created.')
                GetSetGroup.RemoveChildGroup(Environment.ChildGroupID)
                sys.exit('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        else:        
                #EPListFile.write(computer['hostname']+'\n')
                EPdetails['node'].append({'hostname': computer['hostname'],'connector_guid':computer['connector_guid'],'number': count})
                count=count+1
    with open(Environment.ParentGroupName+"/EPdetails.txt", "w+") as outfile:
        json.dump(EPdetails,outfile)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print(' Retrived the End Point detials in the group :'+ Environment.ParentGroupName)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    return (response_json)
#Getlist()
