#! /usr/bin/env python
#
# Python script for the Interoute Object Storage API:
#   Name: s3ls.py
#   Purpose: Show bucket contents in 'ls' style for an Object Storage account
#   Requires: class S3Auth in the file awsauth.py
#   Requires: reference data file for Interoute Object Storage (locally or via Internet call to Github)
# See the repo: https://github.com/Interoute/object-storage-api
#
# You can pass options via the command line: type 'python s3ls.py -h' for usage information
#
# Copyright (C) Interoute Communications Limited, 2017
#
# References:
#   http://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html
#   https://docs.python.org/2/library/xml.etree.elementtree.html
#   https://stackoverflow.com/questions/34009992/python-elementtree-default-namespace
#   https://stackoverflow.com/questions/29785974/determine-s3-bucket-region


'''
from __future__ import print_function
from collections import OrderedDict
from copy import deepcopy
import base64
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
import json
import xml.dom.minidom
import xml.etree.ElementTree as ET

# function to prettyprint XML
def xmlp(xmlString):
   print xml.dom.minidom.parseString(xmlString).toprettyxml()

# STEP: Load the Object Storage data file (information about regions, storage policies etc)
json_file = 'interoute-object-storage-refdata.json'

# Load the JSON data file (local file OR via Github URL OR EXIT WITH ERROR)
if os.path.isfile(json_file):
   ##print("Reading interoute-object-storage-refdata.json from local...")
   with open(json_file) as fh:
       OSdata = json.load(fh)
else:
   ##print("Reading interoute-object-storage-refdata.json from Github...")
   try:
       jstring = requests.get('https://raw.githubusercontent.com/Interoute/object-storage-api/master/interoute-object-storage-refdata.json').text
       OSdata = json.loads(jstring)
   except:
       sys.exit("ERROR: Object Storage data file not found")
regions = [s for s in OSdata.keys()]

# STEP: Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default=os.path.join(os.path.expanduser('~'), '.s3cfg'),
                    help="path/name of the config file to be used for the S3 URL and S3 keys (default is ~/.s3cfg)")
parser.add_argument("-r", "--region", default='', help="display for the specified Object Storage region (default is all regions)")
parser.add_argument("-s", "--storagepolicies", action='store_true', help="display the storage policy information for each bucket")
parser.add_argument("-p", "--permissions", action='store_true', help="display the ACL permissions for each bucket/folder/object")
## ** ADD OPTION FOR FILTERING ONLY ACL PUBLIC PERMISSIONS
## ** ADD OPTION FOR SETTING AN INITIAL BUCKET (OR BUCKET/FOLDER) -- DEFAULT 'NON-RECURSIVE' TO SHOW CONTENTS AT TOP LEVEL OF THE BUCKET/FOLDER
## ** ADD OPTION  RECURSIVE (INCLUDE ALL LEVELS BELOW INITIAL BUCKET/FOLDER LEVEL) OR NON-RECURSIVE (LIST ONLY OBJECTS/FOLDERS AT THE INITIAL LEVEL)
## ** ADD OPTION FOR FLAT DISPLAY OF FOLDER1/FOLDER2/.../OBJECT OR HIERARCHICAL-INDENTED OUTPUT
## ** ADD OPTIONS FOR SHOWING VERSIONING INFORMATION??
## ** ADD OPTION FOR COLOURISED OUTPUT (OF PUBLIC PERMISSION STATUS)
coloredOutput = True
config_file = parser.parse_args().config
region_selected = parser.parse_args().region.upper()

if region_selected:
   if region_selected not in regions:
      sys.exit("FATAL: Requested region '%s' not found in the system regions list %s" % (region_selected, regions))

## *** TO BE ADDED: IF CONFIG FILE NOT INPUT AND DEFAULT FILE IS MISSING, THEN EXIT WITH ERROR

# STEP: Extract the config information
# Using Python module ConfigParser (reference: https://docs.python.org/2/library/configparser.html)
## *** The config 'section' is assumed to be 'default'
config = ConfigParser.ConfigParser()
if os.path.isfile(config_file):
    config.readfp(open(config_file))
    ##S3_HOST_BASE = config.get('default','host_base')
    ##S3_URL = 'https://' + S3_HOST_BASE
    S3_KEY = config.get('default','access_key')
    S3_SECRET = config.get('default','secret_key')
else:
   sys.exit("FATAL: Config file not found")

# STEP: Generate the S3 authorisation object
S3_URL = OSdata[regions[0]]['apiEndpoint']
OSauth = S3Auth(S3_KEY, S3_SECRET, service_url=S3_URL)

## print("Regions: %s" % regions)

# XML namespaces ('s3' is default)
ns = {"s3":"http://s3.amazonaws.com/doc/2006-03-01/"}

# Top-level GET returns Owner data and list of all bucket names
# Only need to do this for one region because contents of all regions are returned
resp = requests.get('https://' + OSdata[regions[0]]['apiEndpoint'], auth=OSauth)
##xmlp(resp.text)
allBuckets = ET.fromstring(resp.text)

# Set up Dict for bucket data, with keys = the bucket names
bucketsDataDict = {}
for b in allBuckets.find("s3:Buckets", ns).findall('s3:Bucket', ns):
   bname = b.find('s3:Name', ns).text
   bucketsDataDict[bname] = {}
   bucketsDataDict[bname]['name'] = bname
   bucketsDataDict[bname]['created'] = b.find('s3:CreationDate', ns).text.split('.')[0]
   #FOLLOWING CALL DOES NOT WORK BECAUSE YOU NEED TO ALREADY KNOW THE REGION FOR THE API CALL TO SUCCEED!
   #  requests.get('https://' + bname + "." + OSdata[regions[0]]['apiEndpoint'], auth=OSauth).headers['x-amz-bucket-region'].upper()
   locationResp = ET.fromstring(requests.get('https://' + bname + "." + OSdata[regions[0]]['apiEndpoint'] + '/?location', auth=OSauth).text).text
   # Default region has blank value for '?location'
   if not(locationResp): 
      bucketsDataDict[bname]['region'] = regions[0]
   else:
      bucketsDataDict[bname]['region'] = locationResp.upper()

# Get ACL permissions data for buckets (if region_selected option is input, only do this for buckets in the one specified region)
for bname in bucketsDataDict.keys():
   # check if showing content for all regions, or this bucket is in the specified region
   if not(region_selected) or (region_selected and bucketsDataDict[bname]['region'] == region_selected):
      aclResp = ET.fromstring(requests.get('https://' + bname + "." + OSdata[bucketsDataDict[bname]['region']]['apiEndpoint'] + '/?acl', auth=OSauth).text)
      prmslist = []
      publicTest = []
      grantslist = aclResp.find('s3:AccessControlList', ns).findall('s3:Grant', ns)
      for grant in grantslist:
         gtype = grant.find('s3:Grantee', ns).attrib['{http://www.w3.org/2001/XMLSchema-instance}type']
         if gtype == 'CanonicalUser':
             prmslist += [{'type': 'user', 'user':grant.find('s3:Grantee', ns).find('s3:DisplayName', ns).text, 'permission':grant.find('s3:Permission', ns).text}]
             publicTest += [False]
         elif gtype == 'Group':
             groupName = grant.find('s3:Grantee', ns).find('s3:URI', ns).text.split('/')[-1]
             prmslist += [{'type': 'group', 'group':groupName, 'permission':grant.find('s3:Permission', ns).text}]
             if groupName == "AllUsers":
                publicTest += [True]
             else:
                publicTest += [False]
      bucketsDataDict[bname]['publicFlag'] = any(publicTest)
      bucketsDataDict[bname]['accessACL'] = prmslist
      
# ** TEST OUTPUT **
# ** TO ADD: SORTING OF BUCKET OUTPUT BY: CREATE TIME, REGION, NAME (ASCENDING/DESCENDING IN EACH CASE)
# ** TO ADD: SORTING OF FOLDER/OBJECT OUTPUT BY: CREATE TIME, NAME (ASCENDING/DESCENDING IN EACH CASE)

for bname in bucketsDataDict.keys():
   # check if showing content for all regions, or this bucket is in the specified region
   if not(region_selected) or (region_selected and bucketsDataDict[bname]['region'] == region_selected):
      if coloredOutput and bucketsDataDict[bname]['publicFlag']:
         stateColorOn = "\x1b[32m"
         stateColorOff = "\x1b[0m"
      else:
         stateColorOn = ""
         stateColorOff = ""
      print("%s %s  %s  %s %s %s" % (stateColorOn, bucketsDataDict[bname]['created'], bucketsDataDict[bname]['region'], bucketsDataDict[bname]['name'], bucketsDataDict[bname]['accessACL'], stateColorOff))

      
