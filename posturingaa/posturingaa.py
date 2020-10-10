# -*- coding: utf-8 -*-
"""Main module.


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
import Environment
import time
import base64
import Credentials
import ComputerList
#import Orbital_token
import OrbitalQuery
import GetSetGroup
#from GetSetGroup import *
import NodeBatch
import sys
import os
import Orbital_getJob
import pyjokes


Environment.ParentGroupName = input(" Enter the Group name to check the Complaince :")
Environment.ProgramtoSearch = input("Enter the software would like to check installation status :")
AMPSession=Environment.AMPSession
#print(Environment.ParentGroupName)

if not os.path.exists('AMPPosture'):
    os.makedirs('AMPPosture')
os.chdir('AMPPosture')

if not os.path.exists(Environment.ParentGroupName):
    os.makedirs(Environment.ParentGroupName)

## Create the new Group and make it as Child to the group under Posture
if (GetSetGroup.ChildGroup()== 'True'):
    sys.exit(' Please Make sure all EPs are Complaint for earlier process before starting a new Check')
## Get Computer list filtered by Parent Group ID. Which is retrived from above ChildGroup funtion call.
EPList= ComputerList.Getlist()
CGroup= Environment.ChildGroupID
MoveGroupParams={"group_guid":CGroup}
url= Credentials.AMP_Cloud + '/v1/computers/' 


#Move all computers to child Group
TotalEPCount=0
for computer in EPList['data']:
     TotalEPCount= TotalEPCount+1
     #print(computer['connector_guid'], computer['hostname'])
     response = Environment.AMPSession.patch(url+'/'+ computer['connector_guid'] , params=MoveGroupParams)

posture={'ParentGroupName': Environment.ParentGroupName,'ParentGroupID':Environment.ParentGroupID,'ChildGroupName':Environment.ChildGroupName,'ChildGruopID':Environment.ChildGroupID,'ProgramName':Environment.ProgramtoSearch }
with open(Environment.ParentGroupName+"/posturedetails.txt", 'w+') as outfile:        
        json.dump(posture,outfile)
print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
print(' Moved all End Points to the child group :'+ Environment.ChildGroupName)
print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

# Do the Compliance check for all the EPs in a Batches. 
NodeBatch.PrepareNodeBatch()

### Query the each Batch of End Points for specific program installed or not        
OrbitalQuery.QueryOrbital()

### Sent the Quesry to the EndPoints with the timer expiry 1 minute. Pls change as per the requirement.
### Wait till Expire time to rpocess teh Job Results.
print ('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print (' Dear Admin I have sent the query to End Points. Sit back and relax for a minute, will come back with the results ')
print ('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

print('\n Mean while Enjoy the joke!!')
print(pyjokes.get_joke())
time.sleep(30)  
print('\n  Enjoy another joke!!')
print(pyjokes.get_joke())
time.sleep(30)   

  ##### Above Query creats Jobs in Orbital with the results.  
Orbital_getJob.GetJobResults()  
print (' COMPLETED MY JOB, ALL THE BEST FOR NEXT SETP !! BE READY TO ANSWER GOOD NUMBER OF CALLS, ONCE YOU START ISOLATION PROCESS')
print('Bye')