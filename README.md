# object-storage-api

Programs and files for using the API for [Interoute Object Storage](https://cloudstore.interoute.com/object-storage).

## Reference data file for Interoute Object Storage

The file [interoute-object-storage-refdata.json](https://raw.githubusercontent.com/Interoute/object-storage-api/master/interoute-object-storage-refdata.json) contains reference information for the regions, data centres and storage policies, in a JSON format.

## API client tool configuration file

Most S3-based client tools require a configuration file. Details differ for each tool but the essential settings are 'host_base' and 'host_bucket', which you can find in the sample configuration file [s3cfg](https://raw.githubusercontent.com/Interoute/object-storage-api/master/s3cfg), which is suitable for use with the [s3cmd](http://s3tools.org/s3cmd) client. 

The 'access_key' and 'secret_key' values for your Object Storage account can be found by logging in to the user interface (see the [User Guide](https://cloudstore.interoute.com/knowledge-centre/library/object-storage-user-guide) for details).

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

## Object Storage documentation

All of the documentation can be found here: [cloudstore.interoute.com/knowledge-centre/library/object-storage](https://cloudstore.interoute.com/knowledge-centre/library/object-storage)

