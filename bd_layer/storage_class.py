import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import os
import json

import csv

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname,"service_key.json" )

cred = credentials.Certificate(json.loads(os.environ['SERVICE_KEY']))
#firebase_admin.initialize_app(cred, {"storageBucket": "redmine-bd.appspot.com/" })

db=firestore.client()

"""
const firebaseConfig = {
  apiKey: "AIzaSyAZ5x6BN6XI-5Uicff1dlFU90LOF5jwHj8",
  authDomain: "redmine-bd.firebaseapp.com",
  projectId: "redmine-bd",
  storageBucket: "redmine-bd.appspot.com",
  messagingSenderId: "637543841727",
  appId: "1:637543841727:web:a0d88e38a18c6dbb1deb0a",
  measurementId: "G-J5TXLT80SZ"
};
"""

#storage_db = storage._StorageClient(credentials=cred, project="redmine-bd", default_bucket="gs://redmine-bd.appspot.com/")

#bucket = storage_db.bucket()

#blob = bucket.blob("teste")

"""def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")
upload_blob(firebase_admin.storage.bucket().name, 'sample_image_file.jpg', 'images/beatiful_picture.jpg')
"""

def upload_blob_from_file(bucket_name, file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    bucket = storage.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(file_name)

    print(
        f"File{file_name} uploaded to {destination_blob_name} ."
    )

def download_blob_into_memory(bucket_name, blob_name):
    """Downloads a blob into memory."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # blob_name = "storage-object-name"

    #storage_client = storage._StorageClient(credentials=None, project="redmine-bd", default_bucket="redmine-bd.appspot.com")

    bucket = storage.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(blob_name)
    if blob.exists():
        contents = blob.download_as_text()
    
    else:
        print("nao existe")

        contents = "nothing"

    print(
        "Downloaded storage object {} from bucket {} as the following string: {}.".format(
            blob_name, bucket_name, contents
        )
    )

def delete_storage_firebase_blob(bucket_name, file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    bucket = storage.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    if blob.exists(file_name):
        blob.upload_from_file(file_name)
    
    else:
        print("nao existe")

    print(
        f"{destination_blob_name} with contents {file_name} uploaded to {bucket_name}."
    )


if __name__ == '__main__':

    download_blob_into_memory("redmine-bd.appspot.com", "bruno.adao-7459.cssv")

    #upload_blob_from_file("redmine-bd.appspot.com", "C:\\Users\\bruno\\Desktop\\projetos\\iphan\\cgti\\esr_project\\esr_back\\.\\temp\\bruno.adao-1583.csv", "text2.csv")