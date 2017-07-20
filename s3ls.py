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
import pprint
import time
import datetime
import dateutil.parser
import pytz
import textwrap
import re
'''

import ConfigParser
import argparse
import requests
from awsauth import S3Auth
import os
import sys
import xml.dom.minidom
import xml.etree.ElementTree as ET

# function to prettyprint XML
def xmlp(xmlString):
   print xml.dom.minidom.parseString(xmlString).toprettyxml()

# STEP: Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default=os.path.join(os.path.expanduser('~'), '.s3cfg'),
                    help="path/name of the config file to be used for the S3 URL and S3 keys (default is ~/.s3cfg)")
parser.add_argument("-r", "--region", help="Object Storage region")
config_file = parser.parse_args().config
## *** PROCESS parser.parse_args().region
## *** WHAT TO DO FOR THE DEFAULT REGION?? 

## *** TO BE ADDED: IF CONFIG FILE NOT INPUT AND DEFAULT FILE IS MISSING, THEN EXIT WITH ERROR

# STEP: Extract the config information
# Using Python module ConfigParser (reference: https://docs.python.org/2/library/configparser.html)
## *** The config 'section' is assumed to be 'default'
config = ConfigParser.ConfigParser()
if os.path.isfile(config_file):
    config.readfp(open(config_file))
    S3_HOST_BASE = config.get('default','host_base')
    S3_URL = 'https://' + S3_HOST_BASE
    S3_KEY = config.get('default','access_key')
    S3_SECRET = config.get('default','secret_key')
else:
   sys.exit("FATAL: Config file not found")

# STEP: Generate the S3 authorisation object
OSauth = S3Auth(S3_KEY, S3_SECRET, service_url=S3_URL)

# STEP: .................

print("raw XML...")
r = requests.get(S3_URL, auth=OSauth)
xmlp(r.text)
allbuckets = ET.fromstring(r.text)
for child in allbuckets:
    print child.tag, child.attrib





