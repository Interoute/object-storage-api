import requests
from awsauth import S3Auth

ACCESS_KEY = 'ACCESS_KEY_XXX'
SECRET_KEY = 'SECRET_KEY_XXX'

OSauth = S3Auth(ACCESS_KEY, SECRET_KEY, service_url='s3-eu.object.vdc.interoute.com')

# PUT a new object into an existing bucket (replace 'mybucket' with an actual bucket name)
## objecttext = 'The purpose of the object'
## r1 = requests.put('http://mybucket.s3-eu.object.vdc.interoute.com/testobject.txt', auth=OSauth, data=objecttext)

# GET contents of an object (replace 'mybucket' with an actual bucket name)
r2 = requests.get('http://mybucket.s3-eu.object.vdc.interoute.com/testobject.txt', auth=OSauth)



