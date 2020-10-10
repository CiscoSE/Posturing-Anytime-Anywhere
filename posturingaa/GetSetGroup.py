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
import sys
import Environment

def ChildGroup():
#############################################################################################    
# This Function will complete follwoing tasks
# Retrive all Groups filtered by Groupname given.
# The result will have all the Groups contains the name given by end user.
# Will find the exact match and stores the GUID of the group.
# Creates a new group with the extension '_Compiance'.
# If a group with the extension already there then will exit the process.
# After creating the new group will make it as Child group to the group mentioned by user.
############################################################################################
    
    EPListFile=open(Environment.ParentGroupName+"/EPList.txt", "w+")
    Environment.ChildGroupName = Environment.ParentGroupName +'_Compliance'
    

    ## Step 1:  Get the detials of group in the treatement.
    #############################################
    DuplicateProc = 'False'
    url = Credentials.AMP_Cloud + '/v1/groups?name=' + Environment.ParentGroupName 
     
    response = Environment.AMPSession.get(url)
    response_json = response.json()
    #print (json.dumps(response_json,indent=2))
    for j in response_json['data']:
         if (j['name']==Environment.ParentGroupName):
            Environment.ParentGroupID =(j['guid'])
         else:
            if(j['name']==Environment.ChildGroupName):
                DuplicateProc='True'
    #print('Parent ID' + Environment.ParentGroupID)
    if (Environment.ParentGroupID==''):
        print("\n ************************************")
        print("\n* No such Group Exits. Pls check. ")
        sys.exit("\n *********************************")


    ###  Step 2: Create a new group
    #####################################
    if (DuplicateProc=='True'):
        print("Other Process is already working Can not proceed")
        sys.exit("Other Process is already working Can not proceed")

    url= Credentials.AMP_Cloud + '/v1/groups'
    parameters = {'name':Environment.ChildGroupName,'description': 'Created for Compliance. Will be deleted'}


    response = Environment.AMPSession.post(url, params=parameters)
    
    ## Step 3: Get the Group ID of new Group created.
    ##################################

    url = Credentials.AMP_Cloud + '/v1/groups?name=' + Environment.ChildGroupName

    response = Environment.AMPSession.get(url)
    
    response_json = response.json()
    for k in response_json['data']:
        #print('Newly Ctreated Child ID ' + k['guid'])
        Environment.ChildGroupID=k['guid']
    

    ## Step 4: Make New group as child Group.

    Childurl= Credentials.AMP_Cloud + '/v1/groups/' + str(Environment.ChildGroupID) + '/parent'
    parameters = {"parent_group_guid":Environment.ParentGroupID}
    response = Environment.AMPSession.patch(Childurl, params=parameters)
    
    return(DuplicateProc)

def RemoveChildGroup(ChildGroupID):
     #print('Remove Child   ' + ChildGroupID)
     url = Credentials.AMP_Cloud + '/v1/groups/' + ChildGroupID
     response = Environment.AMPSession.delete(url)
     response_json = response.json()
     print ('\nRemove Child    ',response, ChildGroupID)
     if (response.status_code==200 or response.status_code==202):
        if(response_json['data']['deleted']=='true'):
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print("Deleted the Child Group Successfully")
            sys.exit('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            #print (json.dumps(response_json,indent=2))
            #return(response_json['data']['deleted'])
     else:
         print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
         print( "Error while trying to delete. Error code: ", response.status_code)
         sys.exit('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
     return()
#ChildGroup()
