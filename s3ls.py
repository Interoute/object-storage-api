#! /usr/bin/env python
#
# Python script for the Interoute Object Storage API:
#   Name: s3ls.py:
#   Purpose: Show bucket and object contents in 'ls' style for an Object Storage account
#   Requires: class S3Auth in the file awsauth.py
# See the repo: https://github.com/Interoute/object-storage-api
#
# You can pass options via the command line: type 'python s3ls.py -h'
# for usage information
#
# Copyright (C) Interoute Communications Limited, 2017
#
# References:
#   

'''
from __future__ import print_function
from collections import OrderedDict
from copy import deepcopy
import base64
import json
import os
import sys
import pprint
import time
import datetime
import dateutil.parser
import pytz
import textwrap
import re
'''

import argparse
import requests
from awsauth import S3Auth

# STEP: Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default=os.path.join(os.path.expanduser('~'), '.s3cfg'),
                    help="path/name of the config file to be used for the API URL and API keys (default is ~/.s3cfg)")
parser.add_argument("-r", "--region", help="Object Storage region")
config_file = parser.parse_args().config
## *** PROCESS parser.parse_args().region
## *** WHAT TO DO FOR THE DEFAULT REGION?? 

## *** IF CONFIG FILE NOT INPUT AND DEFAULT FILE IS MISSING, THEN EXIT WITH ERROR
## *** IF CONFIG FILE IS INPUT BUT NOT FOUND, THEN EXIT WITH ERROR

# STEP: Extract the config information

##S3_URL = 'XXXXXXXXX'
##S3_KEY = 'XXXXXXXXX'
##S3_SECRET = 'XXXXXXXXX'

# STEP: Generate the S3 authorisation object
OSauth = S3Auth(S3_KEY, S3_SECRET, service_url=S3_URL)

# STEP: ..............
print("Cluster configuration '%s':" % (outfile))
print(json.dumps(zonesDict))
with open(outfile, 'w') as outf:
   json.dump(zonesDict, outf)
print("Cluster configuration data written to output file. Program terminating.")



