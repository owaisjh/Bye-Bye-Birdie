import glob, os
from google.cloud import storage



bucket_name = 'big-data-1-project-storage'
prefix = 'cleaned-data/owais/weather.csv/'
dl_dir = '/home/oah4/project/weather.csv/'



storage_client = storage.Client.from_service_account_json('creds.json')  # login credentials for gcp
bucket_name = 'big-data-1-project-storage'
bucket = storage_client.get_bucket(bucket_name)
blobs = bucket.list_blobs(prefix)  # Get list of files

for blob in storage_client.list_blobs(bucket_name, prefix=prefix):
    filename = blob.name.replace('/', '_') 

    blob.download_to_filename(dl_dir + filename)