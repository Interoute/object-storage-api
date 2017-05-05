import requests
from awsauth import S3Auth
import base64
import hashlib

INTEROUTE_S3_KEY = 'XXXXXXXXX'
INTEROUTE_S3_SECRET = 'XXXXXXXXX'

OSauth = S3Auth(INTEROUTE_S3_KEY, INTEROUTE_S3_SECRET, service_url='s3-eu.object.vdc.interoute.com')

# Load the CORS configuration from file 'CORS.cfg' and calculate the encoded MD5 checksum
with open('CORS.cfg') as fh:
   corsConfig = fh.read()
corsMD5hash = hashlib.md5()
corsMD5hash.update(corsConfig)
corsMD5encoded = base64.b64encode(corsMD5hash.digest())

# XML data strings for new bucket in different regions (default region EU is selected when LocationConstraint is not specified)
createBucketCH = '<CreateBucketConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><LocationConstraint>ch</LocationConstraint></CreateBucketConfiguration>'
createBucketDE = '<CreateBucketConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><LocationConstraint>de</LocationConstraint></CreateBucketConfiguration>'

# Create a bucket in the DE region
## requests.put('http://my-de-bucket.s3-de.object.vdc.interoute.com', auth=OSauth, data=createBucketDE)

# PUT the CORS configuration to an existing bucket (replace 'mybucket' with an actual bucket name)
## requests.put('http://mybucket.s3-eu.object.vdc.interoute.com/?cors', auth=OSauth, data=corsConfig, headers={'content-md5':corsMD5encoded})

# PUT a new object into an existing bucket (replace 'mybucket' with an actual bucket name)
## objecttext = 'The purpose of the object'
## requests.put('http://mybucket.s3-eu.object.vdc.interoute.com/testobject.txt', auth=OSauth, data=objecttext)

# GET contents of an object (replace 'mybucket' with an actual bucket name)
## r1 = requests.get('http://mybucket.s3-eu.object.vdc.interoute.com/testobject.txt', auth=OSauth)

# XML data strings for enabling or suspending versioning status of a bucket (use with a '?versioning' request)
versioningEnabled = '<VersioningConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Status>Enabled</Status></VersioningConfiguration>'
versioningSuspended = '<VersioningConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Status>Suspended</Status></VersioningConfiguration>'

# Example of Versioning enable (the bucket must already exist)
## requests.put('http://testversioning.s3-eu.object.vdc.interoute.com/?versioning', auth=OSauth, data=versioningEnabled)



