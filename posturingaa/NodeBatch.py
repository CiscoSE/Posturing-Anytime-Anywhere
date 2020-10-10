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


import os
import re
import json
import Environment
#import string
####################################################################################################  
# This fundtion will do follwoing tasks
# will read the EPDetals file created in Computerlist function.
# Will create a batch of 25 endpoints per line and write them into file
####################################################################################################  

def PrepareNodeBatch():
    #EPListFile=open("EPList.txt", "r")
    NodeList= open(Environment.ParentGroupName+"/NodeList.txt", "w+")
    EPListFile=open(Environment.ParentGroupName+"/EPdetails.txt", "r")          
    EPdata=json.load(EPListFile)
    #EPListFile.readline()
    Nodesline=''
    EPCount= 1
    Nodelinecount= 0
    for node in EPdata['node']:
        #if (EPCount==node['number']):
            #print("i am here")
            #NodeList.write(Nodesline+'\n')
            #break
        if (EPCount==1):
            Nodesline="host:"+ node['hostname']
            EPCount=EPCount+1
        else:
            if (EPCount<25):
                Nodesline= Nodesline+','+ "host:"+node['hostname']
                EPCount=EPCount+1
                #print (Nodesline)
                Nodelinecount=Nodelinecount+1
            else:
                if(EPCount==25):
                    Nodesline= Nodesline+','+ "host:"+node['hostname']
                    NodeList.write(Nodesline+'\n')
                    EPCount=1
                    Nodesline=''
    
    #print ('Count is' ,EPCount)
    if(Nodesline != ''):
        NodeList.write(Nodesline+'\n') 
        Nodelinecount=Nodelinecount+1          
    EPListFile.close()
    NodeList.close()
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print (' Total End points processed: '+ str(EPCount) + '  into '+ str(Nodelinecount) )
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    
    return()

#PrepareNodeBatch1()