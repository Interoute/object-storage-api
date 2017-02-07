import requests
from awsauth import S3Auth

ACCESS_KEY = 'ACCESS_KEY_XXXXXX'
SECRET_KEY = 'SECRET_KEY_XXXXXX'

OSauth = S3Auth(ACCESS_KEY, SECRET_KEY, service_url='s3-eu.object.vdc.interoute.com')

# Load the CORS configuration from file 'CORS.cfg' and calculate the encoded MD5 checksum
with open('CORS.cfg') as fh:
   corsConfig = fh.read()
corsMD5hash = hashlib.md5()
corsMD5hash.update(corsConfig)
corsMD5encoded = base64.b64encode(corsMD5hash.digest())

# PUT the CORS configuration to an existing bucket (replace 'mybucket' with an actual bucket name)
## requests.put('http://mybucket.s3-eu.object.vdc.interoute.com/?cors', auth=OSauth, data=corsConfig, headers={'content-md5':corsMD5encoded})

# PUT a new object into an existing bucket (replace 'mybucket' with an actual bucket name)
## objecttext = 'The purpose of the object'
## requests.put('http://mybucket.s3-eu.object.vdc.interoute.com/testobject.txt', auth=OSauth, data=objecttext)

# GET contents of an object (replace 'mybucket' with an actual bucket name)
## r1 = requests.get('http://mybucket.s3-eu.object.vdc.interoute.com/testobject.txt', auth=OSauth)



