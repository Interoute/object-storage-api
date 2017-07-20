# Utility program to generate XML tables from the JSON data "interoute-object-storage-refdata.json"
# XML output is ready to be inserted into documentation files DOC104 and DOC106

# JSON file location:
#   /home/phillip/Interoute/github-Interoute/object-storage-api/interoute-object-storage-refdata.json
#   https://raw.githubusercontent.com/Interoute/object-storage-api/master/interoute-object-storage-refdata.json

# Written in Python version 2 by Phillip Kent, phillip.kent@interoute.com
# version: 2017-03-28

import json
import os
import sys
import subprocess

# Output files:
outfile1 = "DOC-table-object-storage-regions.xml"
outfile2 = "DOC-table-object-storage-policies.xml"
outfile3 = "DOC-table-object-storage-static-websites.xml"

# Data file and path
json_file = 'interoute-object-storage-refdata.json'
json_filepath =  '/home/phillip/Interoute/github-Interoute/object-storage-api/'

# Region names in list order required for the tables
regionList = ['EU', 'DE', 'CH']

# Load the JSON data file
if os.path.isfile(json_filepath + json_file):
    with open(json_filepath + json_file) as fh:
        OSdata = json.load(fh)
else:
    sys.exit("ERROR: Input JSON file not found. Program terminating")

## get commit date for JSON data file: 'git log -1 --format=%ci interoute-object-storage-refdata.json'
dataCommitDate = subprocess.check_output(["git", "log", "-1", "--format=%ci", json_file]).strip()

# Write output file: outfile1
# Only writing table body to the file, not using the preamble and postamble
##xmlPreamble = ""
'''
<informaltable>
<tgroup cols='3' align='left' colsep='1' rowsep='1'>
<colspec colname='c1' colwidth='1.0*'/>
<colspec colname='c2' colwidth='2.0*'/>
<colspec colname='c3' colwidth='2.5*'/>
<thead>
<row>
 <entry>Region</entry>
 <entry>Data centres</entry>
 <entry>API endpoint (S3 'host base')</entry>
</row>
</thead>
<tbody>
'''

##xmlPostamble = ""
'''
</tbody>
</tgroup>
</informaltable>
'''

with open(outfile1, 'w') as outf:
   ##outf.write(xmlPreamble)
   outf.write("<!-- Region data version date: \'%s\' -->\n" % dataCommitDate)
   for r in regionList:
       outf.write("<row>\n <entry>%s</entry>\n" % OSdata[r]['regionName'])
       outf.write(" <entry>%s</entry>\n" % (', '.join(map(lambda x: '%s (%s)'%(x['name'],x['country']), OSdata[r]['dataCentres']))))
       outf.write(" <entry>%s</entry>\n</row>\n" % OSdata[r]['apiEndpoint'])
   ##outf.write(xmlPostamble)

# Write output file: outfile2
# Only writing table body to the file, not using the preamble and postamble
##xmlPreamble = ""
'''
<informaltable>
<tgroup cols='5' align='left' colsep='1' rowsep='1'>
<colspec colname='c1' colwidth='1.3*'/>
<colspec colname='c2' colwidth='0.3*'/>
<colspec colname='c3' colwidth='0.5*'/>
<colspec colname='c4' colwidth='1.2*'/>
<colspec colname='c5' colwidth='1.5*'/>
<thead>
<row>
 <entry>Storage policy ID</entry>
 <entry>Object Storage region</entry>
 <entry>Replication type</entry>
 <entry>Replication data centres</entry>
 <entry>Notes</entry>
</row>
</thead>
<tbody>
'''

##xmlPostamble = ""
'''
</tbody>
</tgroup>
</informaltable>
'''

with open(outfile2, 'w') as outf:
   ##outf.write(xmlPreamble)
   outf.write("<!-- Region data version date: \'%s\' -->\n" % dataCommitDate)
   for r in regionList:
       for p in OSdata[r]['storagePolicies']:
           outf.write("<row>\n <entry>%s</entry>\n" % p['storagePolicyId'])
           outf.write(" <entry>%s</entry>\n" % OSdata[r]['regionName'])
           outf.write(" <entry>%s</entry>\n" % p['replicationType'])
           outf.write(" <entry>%s</entry>\n" % (', '.join(map(lambda x: '%s (%s)'%(x['name'],x['copies']), p['replicationDataCentres']))))
           outf.write(" <entry>%s</entry>\n</row>\n" % p['storagePolicyDescription'])
   ##outf.write(xmlPostamble)


# Write output file: outfile3
# Only writing table body to the file, not using the preamble and postamble
##xmlPreamble = ""
'''
<informaltable>
<tgroup cols='2' align='left' colsep='1' rowsep='1'>
<colspec colname='c1' colwidth='1.0*'/>
<colspec colname='c2' colwidth='3.0*'/>
<thead>
<row>
 <entry>Bucket region</entry>
 <entry>Static website URL</entry>
 </row>
</thead>
<tbody>
'''

##xmlPostamble = ""
'''
</tbody>
</tgroup>
</informaltable>
'''

with open(outfile3, 'w') as outf:
   ##outf.write(xmlPreamble)
   outf.write("<!-- Region data version date: \'%s\' -->\n" % dataCommitDate)
   for r in regionList:
       outf.write("<row>\n <entry>%s</entry>\n" % OSdata[r]['regionName'])
       outf.write(" <entry>http://<replaceable>bucketname</replaceable>.s3-website-%s.object.vdc.interoute.com</entry>\n</row>\n" % OSdata[r]['regionName'].lower())
   ##outf.write(xmlPostamble)

