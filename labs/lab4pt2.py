import argparse
import boto3
import urllib.request
import os

def download_file(url, filename):
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"File downloaded: {filename}")
    except Exception as e:
        print(f"Download failed: {e}")
        exit(1)

def upload_to_s3(file_name, bucket_name):
    s3 = boto3.client('s3')
    object_name = os.path.basename(file_name)
    
    try:
        s3.upload_file(file_name, bucket_name, object_name)
        print(f"File uploaded to S3: s3://{bucket_name}/{object_name}")
        return object_name
    except Exception as e:
        print(f"File upload failed: {e}")
        exit(1)

def generate_presigned_url(bucket_name, object_name, expires_in):
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_name},
        ExpiresIn=expires_in
    )
    return url

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download, upload, and presign an S3 file.")
    parser.add_argument("file_url", help="URL of the file to download")
    parser.add_argument("bucket_name", help="S3 bucket name")
    parser.add_argument("expires_in", type=int, help="Presigned URL expiration time (seconds)")

    args = parser.parse_args()
    
    local_file = "downloaded_file.gif"  # Change if needed
    download_file(args.file_url, local_file)
    s3_object = upload_to_s3(local_file, args.bucket_name)
    presigned_url = generate_presigned_url(args.bucket_name, s3_object, args.expires_in)

    print(f"Presigned URL (Expires in {args.expires_in} seconds):\n{presigned_url}")
