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

def GenerateToken():

    # Generate Access Token
    cid = Credentials.Orbital_client_id +':'+ Credentials.Orbital_key
    encoded_base64= base64.b64encode(cid.encode('ascii')).decode('utf-8')

    headers = {
        'Authorization':'Basic {}'.format(encoded_base64),
       'Content-Type':'application/json', 'Accept':'application/json'
    }
    request_token = requests.post(Credentials.token_url, headers=headers)
    token_dict = request_token.json()
    #print(request_token.json())

    new_token = token_dict['token']
    new_token_expiry = token_dict['expiry']
 
    # Display token information
    #print('Your new token has been generated and can be found below:'
        #'\n Your Token: {} '
    #    '\n Your Token Expires in ~10mins: {} UTC'
    #    '\n Current local time:            {}'
    #    '\n Current local time in Epoch:   {}'.format(new_token, new_token_expiry, time.asctime(), round(time.time())))
 
    #Set new token to access token
    access_token = new_token    
    return (access_token)