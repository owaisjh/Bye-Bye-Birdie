import glob, os
from google.cloud import storage

def upload_local_directory_to_gcs(local_path, bucket, gcs_path):
    assert os.path.isdir(local_path)
    for local_file in glob.glob(local_path + '/**'):
        print(local_file)
        if not os.path.isfile(local_file):
           upload_local_directory_to_gcs(local_file, bucket, gcs_path + "/" + os.path.basename(local_file))
        else:
           remote_path = os.path.join(gcs_path, local_file[1 + len(local_path):])
           blob = bucket.blob(remote_path)
           blob.upload_from_filename(local_file)


storage_client = storage.Client.from_service_account_json('creds.json')  # login credentials for gcp
bucket_name = 'big-data-1-project-storage'
bucket = storage_client.get_bucket(bucket_name)

local_path = 'joined-data-final'

BUCKET_FOLDER_DIR = 'cleaned-data/joined-data-final'



upload_local_directory_to_gcs(local_path, bucket, BUCKET_FOLDER_DIR)

