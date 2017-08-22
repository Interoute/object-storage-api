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
#   https://stackoverflow.com/questions/8356501/python-format-tabular-output
#   https://stackoverflow.com/questions/9535954/printing-lists-as-tabular-data
#   https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
# https://stackoverflow.com/questions/1915564/python-convert-a-dictionary-to-a-sorted-list-by-value-instead-of-key
# https://duckduckgo.com/?q=python+itemgetter&t=lm&ia=qa

import ConfigParser
import argparse
import requests
from awsauth import S3Auth
import os
import sys
import json
import xml.dom.minidom
import xml.etree.ElementTree as ET
from math import log

# Function pretty_size to pretty print object size values
# Reference: https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def pretty_size(n,pow=0,b=1024,u='',pre=['']+[p for p in 'KMGTP']):
    pow,n=min(int(log(max(n*b**pow,1),b)),len(pre)-1),n*b**pow
    return "%%.%if%%s%%s"%abs(pow%(-pow-1))%(n/b**float(pow),pre[pow],u)

# Tabular print function
# Reference: https://stackoverflow.com/questions/8356501/python-format-tabular-output
def print_table(table):
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        print "" + "  ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line)) + ""

# Tabular print with 'state' given by shell text colour sequence (last two items of each row of list)
# Assume first element of table_with_state is a list of column headers
def print_table_with_state(table_with_state):
    numcols = len(table_with_state[0]) - 2
    table = [row[:numcols] for row in table_with_state]
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table_with_state:
        print line[numcols] + "" + "  ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line[:numcols])) + "" + line[numcols+1]

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

# The list of all of the regions, as defined in the JSON file 

regions = [s for s in OSdata.keys()]

# STEP: Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default=os.path.join(os.path.expanduser('~'), '.s3cfg'),
                    help="path/name of the config file to be used for the S3 URL and S3 keys (default is ~/.s3cfg)")
parser.add_argument("-r", "--region", default='', help="display for the specified Object Storage region (default is all regions)")
parser.add_argument("-b", "--bucketsonly", action='store_true', help="display only bucket information (without content)")
parser.add_argument("-n", "--namesfilter", default='', help="filter output by simple substring matching of the folder/object name string against this string (default is no filter)")
parser.add_argument("-s", "--storagepolicy", action='store_true', help="display the storage policy information")
parser.add_argument("-p", "--permissions", action='store_true', help="display the ACL permissions for each bucket")
parser.add_argument("-o", "--colored", action='store_true', help="use colorised output (green indicates ACL public permission setting for the bucket - object permission is NOT checked)")
parser.add_argument("-H", "--humanreadable", action='store_true', help="show human-readable size values for objects (powers of 1024)")
## ** ADD OPTION FOR FILTERING ONLY 'PUBLIC' PERMISSIONS WHICH CAN BE OF SEVERAL TYPES (ACL, static website, time-limited share, and?)
## ** ADD OPTION RECURSIVE (INCLUDE ALL LEVELS BELOW AN INITIAL BUCKET/FOLDER LEVEL) OR NON-RECURSIVE (LIST ONLY OBJECTS/FOLDERS AT AN INITIAL LEVEL)
## ** ADD OPTION FOR 'FLAT' DISPLAY OF FULL PATH "BUCKETNAME/FOLDER1/FOLDER2/.../OBJECT" (DEFAULT) OR HIERARCHICAL-INDENTED OUTPUT
## ** ADD OPTIONS FOR SHOWING VERSIONING INFORMATION??
config_file = parser.parse_args().config
region_selected = parser.parse_args().region.upper()
bucketsOnlyDisplay = parser.parse_args().bucketsonly
coloredOutput = parser.parse_args().colored
storagePolicyDisplay = parser.parse_args().storagepolicy
permissionsDisplay = parser.parse_args().permissions
humanreadableSizeDisplay = parser.parse_args().humanreadable
namesFilter = parser.parse_args().namesfilter

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

# Set up Dict for bucket data, with keys=the bucket names
bucketsDataDict = {}
for b in allBuckets.find("s3:Buckets", ns).findall('s3:Bucket', ns):
   bname = b.find('s3:Name', ns).text
   bucketsDataDict[bname] = {}
   bucketsDataDict[bname]['name'] = bname
   bucketsDataDict[bname]['created'] = b.find('s3:CreationDate', ns).text.split('.')[0]
   locationResp = ET.fromstring(requests.get('https://' + bname + "." + OSdata[regions[0]]['apiEndpoint'] + '/?location', auth=OSauth).text).text
   # Default region has blank value for '?location'
   if not(locationResp): 
      bucketsDataDict[bname]['region'] = regions[0]
   else:
      bucketsDataDict[bname]['region'] = locationResp.upper()
   if storagePolicyDisplay:
      bucketsDataDict[bname]['storagepolicyid'] = requests.get('https://' + bname + "." + OSdata[bucketsDataDict[bname]['region']]['apiEndpoint'], auth=OSauth).headers['x-gmt-policyid']   
      bucketsDataDict[bname]['storagepolicyname'] = [sp['storagePolicyInternalName'] for sp in OSdata[bucketsDataDict[bname]['region']]['storagePolicies'] if sp['storagePolicyId']==bucketsDataDict[bname]['storagepolicyid']][0]

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
             prmslist += [{'type': 'user', 'name':grant.find('s3:Grantee', ns).find('s3:DisplayName', ns).text, 'permission':grant.find('s3:Permission', ns).text}]
             publicTest += [False]
         elif gtype == 'Group':
             groupName = grant.find('s3:Grantee', ns).find('s3:URI', ns).text.split('/')[-1]
             prmslist += [{'type': 'group', 'name':groupName, 'permission':grant.find('s3:Permission', ns).text}]
             if groupName == "AllUsers":
                publicTest += [True]
             else:
                publicTest += [False]
      bucketsDataDict[bname]['accessACL'] = prmslist
      # if any of the grants permit public access then set 'publicFlag' to True
      bucketsDataDict[bname]['publicFlag'] = any(publicTest)

#Build the content of the table header depending on the display options
headerRow = ["DATE", "REGION"]
if storagePolicyDisplay:
   headerRow += ["POLICY"]
## TO DO: "SIZE" should be omitted for option 'bucketsOnlyDisplay'
if not(bucketsOnlyDisplay):
   headerRow += ["SIZE"]
headerRow += ["NAME"]
if permissionsDisplay:
   headerRow += ["PERMISSIONS"]
headerRow += ["", ""]

outputTable = []

for bname in bucketsDataDict.keys():         
   # check if showing content for all regions, or this bucket is in the specified region
   if not(region_selected) or (region_selected and bucketsDataDict[bname]['region'] == region_selected):
      if coloredOutput and bucketsDataDict[bname]['publicFlag']:
         stateColorOn = "\x1b[32m"
         stateColorOff = "\x1b[0m"
      else:
         stateColorOn = ""
         stateColorOff = ""
      #Create output row for the bucket
      outputRow = [bucketsDataDict[bname]['created'], bucketsDataDict[bname]['region']]
      if storagePolicyDisplay:
         outputRow += [bucketsDataDict[bname]['storagepolicyname']]
      if not(bucketsOnlyDisplay):
         outputRow += [""]  # print blank as SIZE for a bucket - not displayed for 'bucketsOnlyDisplay'
      outputRow += [bucketsDataDict[bname]['name']]
      if permissionsDisplay:
         permissions = map(lambda x: "%s (%s)" % (x['name'], x['permission']), bucketsDataDict[bname]['accessACL'])
         permissionsString = ", ".join(permissions)
         outputRow += [permissionsString]
      outputRow += [stateColorOn, stateColorOff]
      outputTable += [outputRow]
      #Create output rows for the bucket contents
      if not(bucketsOnlyDisplay):
         bucketContents=ET.fromstring(requests.get('https://' + bname + "." + OSdata[bucketsDataDict[bname]['region']]['apiEndpoint'], auth=OSauth).text)
         for c in bucketContents.findall("s3:Contents", ns):
            # Key = the folder/object path and name
            cKey = c.find("s3:Key", ns).text
            if not(namesFilter) or cKey.find(namesFilter) != -1:
                thisIsFolder =  (cKey[-1] == '/')
                outputRow = [c.find("s3:LastModified", ns).text.split('.')[0], bucketsDataDict[bname]['region']] 
                if storagePolicyDisplay:
                   outputRow += [bucketsDataDict[bname]['storagepolicyname']]
                objectSize = int(c.find("s3:Size", ns).text)
                if thisIsFolder:
                   # for a folder, print 'f' for SIZE
                   outputRow += ["f"]
                elif humanreadableSizeDisplay:
                   outputRow += [pretty_size(objectSize)]
                else: 
                   outputRow += [str(objectSize)]
                outputRow += [ "  "+bucketsDataDict[bname]['name'] + "/" + cKey] 
                if permissionsDisplay:
                   outputRow += [""]
                outputRow += [stateColorOn, stateColorOff]
                outputTable += [outputRow]
      

# ** TO ADD: OPTIONAL SORTING OF BUCKET OUTPUT BY: DATE, REGION, NAME (ASCENDING/DESCENDING IN EACH CASE)
# ** TO ADD: SORTING OF OBJECT/FOLDER OUTPUT BY: DATE, SIZE, NAME (ASCENDING/DESCENDING IN EACH CASE)
# Default sort: primary=region ascending, secondary=name ascending 
if bucketsOnlyDisplay:
   if storagePolicyDisplay:
      outputTable.sort(key=lambda x: (x[1], x[3].strip()))
   else:
      outputTable.sort(key=lambda x: (x[1], x[2].strip()))
else:
   if storagePolicyDisplay:
      outputTable.sort(key=lambda x: (x[1], x[4].strip()))
   else:
      outputTable.sort(key=lambda x: (x[1], x[3].strip()))

# Print the results
if namesFilter:
   print("OUTPUT NAMES FILTER: '%s'" % namesFilter)
print_table_with_state([headerRow] + outputTable)

      
