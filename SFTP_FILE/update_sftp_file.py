import paramiko
from google.cloud import storage
import os
import io
import stat
import json

CONFIG_FILE = "config.json"
GCS_LOG_FILE = "processed_files.log"

config = json.load(open(CONFIG_FILE, "r"))
client = storage.Client()
bucket = client.bucket(config["GCS_BUCKET"])

def connect_sftp():
    """Establish and return an SFTP connection."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=config["SFTP_HOST"],
        port=config["SFTP_PORT"],
        username=config["SFTP_USERNAME"],
        password=config["SFTP_PASSWORD"]
    )
    return ssh.open_sftp()

def fetch_processed_files():
    """Fetch processed files list with timestamps from GCS log."""
    blob = bucket.blob(GCS_LOG_FILE)
    try:
        if blob.exists():
            processed_data = blob.download_as_text()
            return {parts[0]: parts[1] for line in processed_data.splitlines() if (parts := line.split(",")) and len(parts) == 2}
    except Exception as e:
        print(f"Error reading log file: {e}")
    return {}

def update_processed_files(processed_files):
    """Update processed log file in GCS."""
    blob = bucket.blob(GCS_LOG_FILE)
    blob.upload_from_string("\n".join(f"{fname},{timestamp}" for fname, timestamp in processed_files.items()))
    print(f"Updated log file: {GCS_LOG_FILE}")

def upload_to_gcs(file_obj, gcs_path):
    """Upload file to Google Cloud Storage."""
    blob = bucket.blob(gcs_path)
    blob.upload_from_file(file_obj, rewind=True)
    print(f"Uploaded to GCS: {gcs_path}")

def process_sftp_directory(sftp, remote_dir, gcs_prefix, processed_files, new_processed_files):
    """Process SFTP directory and upload only new or modified files to GCS."""
    for item in sftp.listdir_attr(remote_dir):
        remote_path = f"{remote_dir}/{item.filename}"
        gcs_path = f"{gcs_prefix}/{item.filename}"
        file_timestamp = str(item.st_mtime)

        if stat.S_ISDIR(item.st_mode):
            process_sftp_directory(sftp, remote_path, gcs_path, processed_files, new_processed_files)
        else:
            if gcs_path in processed_files:
                if processed_files[gcs_path] == file_timestamp:
                    print(f"Skipping (already processed & timestamp unchanged): {gcs_path}")
                    continue
                else:
                    print(f"File updated: {gcs_path} (Old: {processed_files[gcs_path]}, New: {file_timestamp})")
            
            print(f"Fetching: {remote_path} -> Uploading to GCS: {gcs_path}")
            with io.BytesIO() as file_obj:
                sftp.getfo(remote_path, file_obj)
                file_obj.seek(0)
                upload_to_gcs(file_obj, gcs_path)

            new_processed_files[gcs_path] = file_timestamp

def main():
    """Triggered by Cloud Scheduler via HTTP."""
    sftp = connect_sftp()
    processed_files = fetch_processed_files()
    new_processed_files = {}

    try:
        process_sftp_directory(sftp, "/public", "sftp_raw", processed_files, new_processed_files)
    finally:
        sftp.close()

    if new_processed_files:
        processed_files.update(new_processed_files)
        update_processed_files(processed_files)

    print("SFTP Processing Completed, Moving Towards BigQuery Insertion")
    return "Execution Completed", 200
