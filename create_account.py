# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 01:23:40 2022

AQS EPA API account signup
EPA will send an email to the given email 
and  give you a key to be able to make multiple API requests



key from email: goldcat95
"""

import requests

email='devenjamesaman@gmail.com'
api_url="https://aqs.epa.gov/data/api/signup?email="+email

response = requests.get(api_url)

response.json()