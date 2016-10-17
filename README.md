# object-storage-api [UNDER CONSTRUCTION]

Programs and files for using the API for [Interoute Object Storage](https://cloudstore.interoute.com/objectstorage).

## Set up a CORS policy for buckets created via the API

If you create a bucket via an API call, for example using the [s3cmd](http://s3tools.org/s3cmd) client tool:

```sh
$ s3cmd mb s3://newbucket
```
Then you also need to set a 'CORS policy' for the bucket. Download the [CORS.cfg](https://raw.githubusercontent.com/Interoute/object-storage-api/master/CORS.cfg) file to your local machine, and do: 

```sh
$ s3cmd setcors CORS.cfg s3://newbucket
```

If you do not do this, the new bucket and its contents will not be correctly visible to the Object Storage GUI.

