'''
Author: Deven Aman
Date: 3/13/2022

Description: functions for accessing the EPA AQS data from their API
documentation:  https://aqs.epa.gov/aqsweb/documents/data_api.html#meta

codes: https://www.epa.gov/aqs/aqs-code-list
'''



import requests
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



#account information (modify this for your account)
email='devenjamesaman@gmail.com'
key='goldcat95'






###############################################################################################
'''
METADATA 
Returns information about the API. 
Note, is it not necessary to check the API availibility before each service request 
(the system does this internally and will return an error message if there is a problem). 
The intent of this service is to let you know the system is up before you start a long job.
'''
###############################################################################################

def metadata_isAvail():
    endpoint='metaData/isAvailable'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key
    response = requests.get(url)
    return response.json()

#test call
#print(metadata_isAvail())

def metadata_knownIssues():
    endpoint='metaData/issues'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key
    response = requests.get(url)
    return response.json()

#test call
#print(metadata_knownIssues())

def metadata_revisionHistory():
    endpoint='metaData/revisionHistory'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key
    response = requests.get(url)
    return response.json()

#test call
#print(metadata_revisionHistory())

'''
#this doesnt work i think
def metadata_fieldsByService(service):
    endpoint='metaData/revisionHistory'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key+'&service='+service
    response = requests.get(url)
    return response.json()

#print(metadata_fieldsByService(service='sampleData'))
'''



###############################################################################################
'''
LISTS
This service provides the variable values you many need to create other service requests. 
'''
###############################################################################################

'''
description: returns json list of all available states, cbsas, classes, pqaos, or mas depending on whats needed.
(call input as True if you want it to return the json API response)

inputs: 
    states (bool): US states 
    cbsas (bool): CBSAs (Core Based Statistical Areas)	
    classes (bool): Parameter Classes (groups of parameters, like criteria or all)
    pqaos (bool): PQAOs (primary quality assurance organizations)
    mas (bool): MAs (monitoring agencies)	

output: API response as a json list
'''
def list_values_needed(states=False,cbsas=False, 
                       classes=False,pqaos=False,mas=False):
    responses=[]
    if states:     
        endpoint='list/states'
        url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key
        responses.append(requests.get(url).json())
    if cbsas:     
        endpoint='list/cbsas'
        url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key
        responses.append(requests.get(url).json())
    if classes:     
        endpoint='list/classes'
        url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key
        responses.append(requests.get(url).json())
    if pqaos:     
        endpoint='list/pqaos' 
        url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key
        responses.append(requests.get(url).json())
    if mas:     
        endpoint='list/mas'
        url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key
        responses.append(requests.get(url).json())
        
    return responses

#test call
#print(list_values_needed(states=True,classes=True))



'''
description: gets the state code from state input 

input: state (str)
(state input should have first letter of each word capitalized, space inbetween each word)

output: code for the input state (str)
'''
def state_code(state):
    states_list = list_values_needed(states=True)
    for i in states_list[0]['Data']:
        #print(i)
        if i['value_represented']==state:
            code=i['code']
    return code

#test call    
#print(get_code_from_state(state='Iowa'))



'''
description: returns county code for a given county and state.
    
input: 
    state (str)
    (state input should have first letter of each word capitalized, space inbetween each word)
    
    county (str)
    (county input should have first letter of each word capitalized)

output: county code of that state

returns code not found if the county is not in the state given
'''
def county_code(state,county):
    sc=state_code(state)
    
    endpoint='list/countiesByState'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key+'&state='+sc
    response=requests.get(url).json()

    code=''
    for i in response['Data']:
        #print(i)
        if i['value_represented']==county:
            code=i['code']
    if code=='':
        return 'code not found'
    else:
       return code

#test calls
#print(county_code(state='North Carolina',county='Ashe')) #should return "009"
#print(county_code(state='North Carolina',county='Ashe County')) #should return "code not found"


'''
description: returns all sites in a given county
    
input: 
    state (str)
    (state input should have first letter of each word capitalized, space inbetween each word)
    
    county (str)
    (county input should have first letter of each word capitalized)

output: sites codes and description of site (if available) as json list

'''
def sitesByCounty(state,county):
    sc=state_code(state)
    cc=county_code(state,county)

    endpoint='list/sitesByCounty'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key+'&state='+sc+'&county='+cc
    response=requests.get(url).json()
    return response['Data']

#test call
#print(sitesByCounty(state='North Carolina', county='Wake'))



'''
description: returns all parameters in a given parameter class
    
input: 
    pc (str): class of parameter

output: parameters of the given class as json list and codes of each class

'''

#can use the list_values_needed function to find the different parameter classes (pc), 
#or go to https://aqs.epa.gov/data/api/list/classes?email=test@aqs.api&key=test

def parametersByClass(pc):
    endpoint='list/parametersByClass'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key+'&pc='+pc
    response=requests.get(url).json()
    return response['Data']

#test call
#print(parametersByClass('CRITERIA')) #should return: https://aqs.epa.gov/data/api/list/parametersByClass?email=test@aqs.api&key=test&pc=CRITERIA






#skip monitors service (not needed right now)
#(Returns operational information about the samplers (monitors) used to collect the data. 
#Includes identifying information, operational dates, operating organizations, etc.)







###############################################################################################
'''
Sample Data
Returns sample data as a pandas dataframe - the finest grain data reported to EPA.
all test calls are the same as examples from AQS API documentation

Optional variables not accounted for in these functions: cbdate, cedate and duration. See variables used in service requests to see if these are something you need.
'''
###############################################################################################

def samp_bySite(param,bdate,edate,state,county,site):
    sc=state_code(state)
    cc=county_code(state,county)

    endpoint='sampleData/bySite'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key+'&param='+param+'&bdate='+bdate+'&edate='+edate+'&state='+sc+'&county='+cc+'&site='+site
    response=requests.get(url).json()

    if response['Header'][0]['status']=='Failed':
        print('pull request failed')
        return None
    
    return pd.DataFrame.from_dict(response['Data']) #returns data as pandas dataframe


#test call
#Example: returns all ozone data for the Millbrook School site (#0014) in Wake County, NC for June 18, 2017:
#d = samp_bySite(param='44201',bdate='20170618',edate='20170618',state='North Carolina',county='Wake',site='0014') 
#print(d)
#expected result: https://aqs.epa.gov/data/api/sampleData/bySite?email=test@aqs.api&key=test&param=44201&bdate=20170618&edate=20170618&state=37&county=183&site=0014

def samp_byCounty(param,bdate,edate,state,county):
    sc=state_code(state) #fetch state code for given county
    cc=county_code(state,county) #fetch county code for given county

    endpoint='sampleData/byCounty'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key+'&param='+param+'&bdate='+bdate+'&edate='+edate+'&state='+sc+'&county='+cc
    response=requests.get(url).json()

    if response['Header'][0]['status']=='Failed':
        print('pull request failed')
        return None
    
    return pd.DataFrame.from_dict(response['Data']) #returns data as pandas dataframe

#test call
#example: returns all FRM/FEM PM2.5 data for Wake County, NC between January and February 2016:
#d = samp_byCounty(param='88101',bdate='20160101',edate='20160228',state='North Carolina',county='Wake') 
#print(d)
#expected result: https://aqs.epa.gov/data/api/sampleData/byCounty?email=test@aqs.api&key=test&param=88101&bdate=20160101&edate=20160228&state=37&county=183


def samp_byState(param,bdate,edate,state):
    sc=state_code(state)

    endpoint='sampleData/byState'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key+'&param='+param+'&bdate='+bdate+'&edate='+edate+'&state='+sc
    response=requests.get(url).json()
    
    if response['Header'][0]['status']=='Failed':
        print('pull request failed')
        return None
    
    return pd.DataFrame.from_dict(response['Data']) #returns data as pandas dataframe

#test call
#Example: returns all benzene samples from North Carolina collected on May 15th, 1995:
#d = samp_byState(param='45201',bdate='19950515',edate='19950515',state='North Carolina') 
#print(d)
#expected result: https://aqs.epa.gov/data/api/sampleData/byState?email=test@aqs.api&key=test&param=45201&bdate=19950515&edate=19950515&state=37


'''
#The test for this isnt working for some reason, the pull request fails. may have something to do with the min/max lats/lons being a weird type?
def samp_byBox(param,bdate,edate, minlat, maxlat, minlon, maxlon):

    endpoint='sampleData/byState'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key+'&param='+param+'&bdate='+bdate+'&edate='+edate+'&minlat='+str(minlat)+'&maxlat='+str(maxlat)+'&minlon='+str(minlon)+'&maxlon='+str(maxlon)
    response=requests.get(url).json()

    if response['Header'][0]['status']=='Failed':
        print('pull request failed')
        return None
    
    return pd.DataFrame.from_dict(response['Data']) #returns data as pandas dataframe

#test call
#Example: returns all ozone samples in the vicinity of central Alabama for the first two days in May, 2015:
d = samp_byBox(param='44201',bdate='20150501',edate='20150502',minlat=33.3,maxlat=33.6,minlon=-87.0,maxlon=-86.7) 
print(d)
#expected result: https://aqs.epa.gov/data/api/sampleData/byBox?email=test@aqs.api&key=test&param=44201&bdate=20150501&edate=20150502&minlat=33.3&maxlat=33.6&minlon=-87.0&maxlon=-86.7
'''








###############################################################################################
'''
Monitors

Returns operational information about the samplers (monitors) used to collect the data. 
Includes identifying information, operational dates, operating organizations, etc.


'''
###############################################################################################



def mon_bySite(param,bdate,edate,state,county,site):
    sc=state_code(state)
    cc=county_code(state,county)

    endpoint='monitors/bySite'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key+'&param='+param+'&bdate='+bdate+'&edate='+edate+'&state='+sc+'&county='+cc+'&site='+site
    response=requests.get(url).json()

    if response['Header'][0]['status']=='Failed':
        print('pull request failed')
        return None
    
    return pd.DataFrame.from_dict(response['Data']) #returns data as pandas dataframe


#test call
#Example: returns list of SO2 monitors at the Hawaii Volcanoes NP site (#0007) in Hawaii County, HI that were operating on May 01, 2015. 
#(Note, all monitors that operated between the bdate and edate will be returned):
#d = mon_bySite(param='42401',bdate='20150501',edate='20150502',state='Hawaii',county='Hawaii',site='0007') 
#print(d)
#expected result: https://aqs.epa.gov/data/api/monitors/bySite?email=test@aqs.api&key=test&param=42401&bdate=20150501&edate=20150502&state=15&county=001&site=0007


def mon_byCounty(param,bdate,edate,state,county):
    sc=state_code(state) #fetch state code for given county
    cc=county_code(state,county) #fetch county code for given county

    endpoint='monitors/byCounty'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key+'&param='+param+'&bdate='+bdate+'&edate='+edate+'&state='+sc+'&county='+cc
    response=requests.get(url).json()

    if response['Header'][0]['status']=='Failed':
        print('pull request failed')
        return None
    
    return pd.DataFrame.from_dict(response['Data']) #returns data as pandas dataframe

#test call
#example:  returns all SO2 monitors in Hawaii County, HI that were operating on May 01, 2015:
#d = mon_byCounty(param='42401',bdate='20150501',edate='20150502',state='Hawaii',county='Hawaii') 
#print(d)
#expected result: https://aqs.epa.gov/data/api/monitors/byCounty?email=test@aqs.api&key=test&param=42401&bdate=20150501&edate=20150502&state=15&county=001


def mon_byState(param,bdate,edate,state):
    sc=state_code(state)

    endpoint='monitors/byState'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key+'&param='+param+'&bdate='+bdate+'&edate='+edate+'&state='+sc
    response=requests.get(url).json()
    
    if response['Header'][0]['status']=='Failed':
        print('pull request failed')
        return None
    
    return pd.DataFrame.from_dict(response['Data']) #returns data as pandas dataframe

#test call
#Example: returns SO2 monitors in Hawaii that were operating on May 01, 2015:
#d = mon_byState(param='42401',bdate='20150501',edate='20150502',state='Hawaii') 
#print(d)
#expected result: https://aqs.epa.gov/data/api/monitors/byState?email=test@aqs.api&key=test&param=42401&bdate=20150501&edate=20150502&state=15


'''
#The test for this isnt working for some reason, the pull request fails, may have something to do with the min/max lats/lons being a weird type?

def mon_byBox(param,bdate,edate, minlat, maxlat, minlon, maxlon):

    endpoint='monitors/byState'
    url="https://aqs.epa.gov/data/api/"+endpoint+"?email="+email+"&key="+key+'&param='+param+'&bdate='+bdate+'&edate='+edate+'&minlat='+str(minlat)+'&maxlat='+str(maxlat)+'&minlon='+str(minlon)+'&maxlon='+str(maxlon)
    response=requests.get(url).json()
    print(url)
    
    return pd.DataFrame.from_dict(response['Data']) #returns data as pandas dataframe

#test call
#Example: returns all ozone monitors in the vicinity of central Alabama that operated in 1995
d = mon_byBox(param='44201',bdate='19950101',edate='19951231',minlat=33.3,maxlat=33.6,minlon=-87.0,maxlon=-86.7) 
print(d)
#expected result: https://aqs.epa.gov/data/api/monitors/byBox?email=test@aqs.api&key=test&param=44201&bdate=19950101&edate=19951231&minlat=33.3&maxlat=33.6&minlon=-87.0&maxlon=-86.7
'''