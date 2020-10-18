# Posture Anywhere and Anytime

  

  

# Problem in hand

  

Organisations are adopting Cloud first to deliver the applications to the users which gives better employee experience especially working form home. But also poses unique security risks to the organisation, it becomes impossible for the organisation to enforce AD policies, profiling and posturing of the devices unless employee connects on VPN.

  

- Most of the times employees will connect to customer networks then organisation VPN.

  

- But the security posture remains organisation responsibility.

  

  

# Solution

  

Using "CISCO Orbital capabilities" on AMP4E, solution that can posture an end user system and apply relevant policy. Example, isolation of an endpoint or Block access to SAAS applications temporarily forcing the user to take necessary actions. this actions can be notified in the form of custom webex notification or email.

  

  

# Features!

  

The script built here will search for a specific program installation status on a group of endpoints. Based on the installation status endpoints will be segregated into two groups

  

- Actual group contains all the end points has the software.

  

- A child group, created as apart of process will contains all remaining end points.

  

-

  

  

# Execution

  

Please do not delete any files created by the scripts. It will impact the execution.

  

First step is to configure Credentials.py file with API Keys and URLs. Pls start here.

  

Projects has three execution points.

| Starting point | Description|
| ----------- | ----------- |
*posturingAA.py* :| This is the first script to execute. All the end points in a group will be segregated into Two groups.|
*IsolateEP.py* | This will Isolate the endpoints in the newly created child group.|
StopIsolation.py | This is to unblock an endpoint. Will be executed by user. But should be from server only. As the script will be using the files created while posturing. As an example create a webpage and call this python script on click of a button. User has to enter the 'hostname'. If use can not share the unblock code provide in islationdata.txt |


  

- The execution of this scripts will create Folders and files on the local system, to prevent the thousands of API calls.

  

- When we first execute this script, it will create "AMPPosture" folder in the present working directory.

  

- In the same directory the script create folder with the AMP Group name on which we are working.

  

- In this way we can execute the multiple instances of script for different AMP Groups.

  

- But script will prevent from execution for the same Group, if the earlier process is not concluded and all endpoints achieved the complaint status.

  
| File name | Description|
| ----------- | ----------- |
EPdetails.txt | Will be created on ComputerList.py script. Holds details of all endpoint details like, Name, AMP GUID|
isolationdata.txt | This file will be created by IoslationEP.py . Holds the endpoints isolation status and unblock code.
NodeList.txt | This file will be created by Nodebatch.py script. Holds the string of 25 endpoint names as a single batch.|
OrbitalJobIDList.txt| This file will be created by OrbitalQuery.py. Hold the Orbital Job IDs created as a result of execution of the query.|
posturedetails.txt| This file will be created by posturingAA.py script. Holds details like Group we are working and Program name we are searching on endpoints for|

  

  

# Script Explanation

  

  

| Script name | Description
| ----------- | ----------- |
| posturingAA.py | Main script, will call multiple scripts in a sequence. By the end of this script All the Endpoints will be segregated in two groups. One group with all Complaint endpoint and rest in other group. |
| Credentials.py | This files contains API Keys and URLs |
| Environment.py | This file contains important Global variables. |
| ComputerList.py | This Function retrieve all the computers in a given group. <br  /> If no Endpoints are in the group then removes the Child group created by earlier function. If EPs are present will create a file with JSON object EP Name, AMP connector ID and Program to search.Sorting the data on local machine to avoid huge API calls to retrieve data. |
|Environment.py| This file contains important Global variables.|
|GetSetGroup.py| This Function will complete following tasks. Retrieve all Groups filtered by Group name given. The result will have all the Groups contains the name given by end user. Will find the exact match and stores the GUID of the group.Creates a new group with the extension '_Compliance'.If a group with the extension already there then will exit the process.After creating the new group will make it as Child group to the group mentioned by user.|
|NodeBatch.py| This function will do following tasks. Will read the EPDetals file created in Computerlist function. Will create a batch of 25 endpoints per line and write them into file.
|Orbital_token.py| This function will create a Token and return the same. |
|OrbitalQuery.py | This function will do following tasks. Will read the Nodelist file created in the NodeBatch function.Every line in this file will have 25 Endpoints.Will execute Orbital Query per batch and stores the JobIDs in file.|
|Orbital_getJob.py| This function will do following tasks.Reads the JobIDs form the file.Retrieves all the endpoints results from each jobid. If the EP is available on the JobID then the given software is installed on the EP will move these EPs to Parent group. By the en of function, the Child group will have EPs without software or not active at the time of query.

  

  

### Installation

  

  

Clone the repo

  

```sh

  

git clone https://github.com/CiscoSE/posturingAA.py.git

  

```

  

cd into directory

  

```sh

  

cd posturingAA

  

```

  

Create the virtual environment in a sub dir in the same directory

  

```sh

  

python3 -m venv venv

  

```

  

Start the virtual environment and install requirements.txt from the <posturingAA>

  

```sh

  

source venv/bin/activate

  

pip install -r requirements.txt

  

```

  

Execute the script as any other Python script form console. Developed using AMP API V1 and Orbital API V0 versions.

  

```sh

  

python posturingAA.py

  

```

  

  

### Development

  

  

Want to contribute? Great!

  

  

- You can try modifying the OrbitalQuery.py for multi condition posturing.

  

- If you would like to increase the number of hosts in Orbital query modify on Nodebatch.py

  

- Next step might be reading the ISE policy and convert it to Orbital queries.

  

  

Mod

  

  

License

  

----

  

  

BSD