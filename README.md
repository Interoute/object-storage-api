# object-storage-api

Programs and files for using the API for [Interoute Object Storage](https://cloudstore.interoute.com/object-storage).

## Reference data file for Interoute Object Storage

The file [interoute-object-storage-refdata.json](https://raw.githubusercontent.com/Interoute/object-storage-api/master/interoute-object-storage-refdata.json) contains reference information for the regions, data centres and storage policies, in a JSON format.

This file is used by the utility program [s3ls.py](https://raw.githubusercontent.com/Interoute/object-storage-api/master/s3ls.py) (see below).

## API client tool configuration file

Most S3-based client tools require a configuration file. Details differ for each tool but the essential settings are 'host_base' and 'host_bucket', which you can find in the sample configuration file [s3cfg](https://raw.githubusercontent.com/Interoute/object-storage-api/master/s3cfg), which is suitable for use with the [s3cmd](http://s3tools.org/s3cmd) client. 

The 'access_key' and 'secret_key' values for your Object Storage account can be found by logging in to the user interface (see the [User Guide](https://cloudstore.interoute.com/knowledge-centre/library/object-storage-user-guide) for details).

## Object Storage API authorisation code for use with Python Requests

[awsauth.py](https://github.com/Interoute/object-storage-api/blob/master/awsauth.py) provides a class to generate authorisation data which can be used with the Python [Requests](http://docs.python-requests.org) module.

The code uses AWS Signature Version 2 from the S3 API standard.

Use of the code is explained in the [Interoute Object Storage API User Guide](https://cloudstore.interoute.com/knowledge-centre/library/object-storage-api-user-guide).

## Set up a CORS policy for buckets created via the API

If you create a bucket via an API call, for example using the [s3cmd](http://s3tools.org/s3cmd) client tool:

```sh
$ s3cmd mb s3://newbucket
```
Then you also need to set a 'CORS policy' for the bucket. Download the [CORS.cfg](https://raw.githubusercontent.com/Interoute/object-storage-api/master/CORS.cfg) file to your local machine, and do: 

```sh
$ s3cmd setcors CORS.cfg s3://newbucket
```

If you do not do this, the new bucket and its contents will not be correctly visible to the Object Storage user interface.

## Interoute Object Storage documentation

All of the documentation can be found here: [cloudstore.interoute.com/knowledge-centre/library/object-storage](https://cloudstore.interoute.com/knowledge-centre/library/object-storage)

## s3ls.py utility program

[s3ls.py](https://raw.githubusercontent.com/Interoute/object-storage-api/master/s3ls.py) is a work-in-progress utility which displays the contents of an Object Storage account (buckets, folders and objects) in the style of the Unix/Linux 'ls' command.

The current version does a *limited* check of access permissions, and flags public access objects with a green colour. Currently, the only check is on ACL permissions of buckets (not objects inside buckets). This is not the only way that objects may be exposed to public access. The design intention is that a rapid scan of an object storage account is possible to check on the public access status of all buckets and objects.

### Examples of using the program 

#### (1) Show bucket properties only ('-b') with ACL permissions ('-p')

```sh
$ python s3ls.py -b -p
DATE                 REGION  NAME             PERMISSIONS                                 
2017-07-22T16:40:04  CH      my-ch-bucket-2   Phillip Kent (FULL_CONTROL)                 
2017-07-22T16:41:33  DE      my-de-bucket-2   Phillip Kent (FULL_CONTROL)                 
2016-11-09T16:03:28  EU      cloudstorefiles  Phillip Kent (FULL_CONTROL), AllUsers (READ)
2017-07-22T16:33:26  EU      new-bucket-eu    Phillip Kent (FULL_CONTROL)                 
2017-02-09T09:51:31  EU      testversioning   Phillip Kent (FULL_CONTROL)                 
2016-11-09T16:03:51  EU      vdcexamples      Phillip Kent (FULL_CONTROL), AllUsers (READ)
```

#### (2) As example 1 with storage policies displayed ('-s') and restricting output to the region 'EU' only

```sh
$ python s3ls.py -b -p -s -r EU
DATE                 REGION  POLICY                NAME             PERMISSIONS                                 
2016-11-09T16:03:28  EU      AMS_LON_RP_2_1        cloudstorefiles  Phillip Kent (FULL_CONTROL), AllUsers (READ)
2017-07-22T16:33:26  EU      AMS_LON_SLO_RP_1_1_1  new-bucket-eu    Phillip Kent (FULL_CONTROL)                 
2017-02-09T09:51:31  EU      AMS_LON_SLO_RP_1_1_1  testversioning   Phillip Kent (FULL_CONTROL)                 
2016-11-09T16:03:51  EU      AMS_LON_RP_2_1        vdcexamples      Phillip Kent (FULL_CONTROL), AllUsers (READ)
```

#### (3) Show bucket contents with storage policies and human-readable object sizes ('-H')

(The output shown is abbreviated)

```sh
$ python s3ls.py -s -H
DATE                 REGION  POLICY                SIZE    NAME                                                                                                              
2017-07-22T16:40:04  CH      ZRH_GVA_RP_2_1                my-ch-bucket-2                                                                                                    
2017-07-22T16:41:33  DE      BER_FRA_RP_2_1                my-de-bucket-2                                                                                                    
2016-11-09T16:03:28  EU      AMS_LON_RP_2_1                cloudstorefiles                                                                                                   
2017-04-24T10:26:35  EU      AMS_LON_RP_2_1        f         cloudstorefiles/blog/                                                                                           
2017-04-24T10:32:34  EU      AMS_LON_RP_2_1        f         cloudstorefiles/blog/image/                                                                                     
2017-08-15T15:09:20  EU      AMS_LON_RP_2_1        42.3K     cloudstorefiles/blog/image/CloudStore-Blog-Grendel-Standby-disaster-recovery-image-diagram1.png                 
2017-08-15T15:09:21  EU      AMS_LON_RP_2_1        14.5K     cloudstorefiles/blog/image/CloudStore-Blog-Grendel-Standby-disaster-recovery-image-diagram2.png                 
2017-04-24T10:26:55  EU      AMS_LON_RP_2_1        f         cloudstorefiles/image/                                                                                          
2017-01-05T17:37:45  EU      AMS_LON_RP_2_1        33.3K     cloudstorefiles/image/image-DOC001-VDC2-Events-Events-view.png                                                  
2016-12-21T14:01:54  EU      AMS_LON_RP_2_1        70.2K     cloudstorefiles/image/image-DOC001-VDC2-MyServices-VDC-Control-Centre.png                                       
2017-02-09T09:51:31  EU      AMS_LON_SLO_RP_1_1_1          testversioning                                                                                                    
2017-07-22T16:08:02  EU      AMS_LON_SLO_RP_1_1_1  17        testversioning/testobject                                                                                       
2016-11-09T16:03:51  EU      AMS_LON_RP_2_1                vdcexamples                                                                                                       
2016-12-05T14:47:15  EU      AMS_LON_RP_2_1        720.2M    vdcexamples/CentOS64-template-121213.ova                                                                        
2016-12-05T17:21:28  EU      AMS_LON_RP_2_1        1.6G      vdcexamples/linuxmint-18-cinnamon-64bit.iso                                                                     
2016-12-05T17:21:28  EU      AMS_LON_RP_2_1        98        vdcexamples/linuxmint-18-sha256checksum.txt                                                                     
2017-06-22T12:24:56  EU      AMS_LON_RP_2_1        1.7G      vdcexamples/linuxmint-18.1-mate-64bit.iso
```

#### (4) Use the 'namesfilter' ('-n') option to filter the output

Filter the output by substring matching of object and folder names (this is *not* applied to bucket names), for example show only objects with names ending with the string '.jpg'

```sh
$ python s3ls.py -H -n .jpg
OUTPUT NAMES FILTER: '.jpg'
DATE                 REGION  SIZE    NAME                                                                                                              
2017-07-22T16:40:04  CH              my-ch-bucket-2                                                                                                    
2017-07-22T16:41:33  DE              my-de-bucket-2                                                                                                    
2016-11-09T16:03:28  EU              cloudstorefiles                                                                                                   
2017-08-16T08:45:52  EU      45.4K     cloudstorefiles/blog/image/CloudStore-Blog-Morrish-Data-location-location-image-Pins-marking-location-on-map.jpg
2017-04-24T16:38:12  EU      361.4K    cloudstorefiles/blog/image/CloudStore-blog-20141118-BigRedButton1.jpg                                           
2017-04-24T16:38:12  EU      327.5K    cloudstorefiles/blog/image/CloudStore-blog-20141118-BigRedButton2.jpg                                           
2017-08-04T16:25:45  EU      62.9K     cloudstorefiles/image/image-DOC085-RedHatCloudAccess-Register-Image-form.jpg                                    
2017-07-22T16:33:26  EU              new-bucket-eu                                                                                                     
2017-02-09T09:51:31  EU              testversioning                                                                                                    
2016-11-09T16:03:51  EU              vdcexamples
```


