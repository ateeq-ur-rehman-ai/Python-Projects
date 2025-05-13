import paramiko
import os

SFTP_HOST = "my.dreamscollective.com"
SFTP_PORT = 222
SFTP_USERNAME = "prpone@sftp.thepeachtreepartners.com"
SFTP_PASSWORD = "Admin@prpone!"

REMOTE_DIR = "/public"
LOCAL_DIR = "downloaded_files"

def connect_sftp():
    """Establish an SFTP connection and return the SFTP client."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SFTP_HOST, port=SFTP_PORT, username=SFTP_USERNAME, password=SFTP_PASSWORD)
        return ssh, ssh.open_sftp()
    except Exception as e:
        print(f"SFTP Connection Failed: {e}")
        return None, None

def download_files():
    """Download all files from the remote directory."""
    ssh, sftp = connect_sftp()
    
    if not sftp:
        return
    
    try:
        # Ensure local download folder exists
        if not os.path.exists(LOCAL_DIR):
            os.makedirs(LOCAL_DIR)

        # Get list of files in remote directory
        files = sftp.listdir(REMOTE_DIR)
        print(f"Found {len(files)} files in {REMOTE_DIR}")

        for file in files:
            remote_path = f"{REMOTE_DIR}/{file}"
            local_path = os.path.join(LOCAL_DIR, file)

            try:
                print(f"Downloading: {file} ...")
                sftp.get(remote_path, local_path)
                print(f"{file} downloaded successfully!")
            except PermissionError:
                print(f"Permission Denied: {file}")
            except Exception as e:
                print(f"Error downloading {file}: {e}")

    finally:
        sftp.close()
        ssh.close()
        print("SFTP Connection Closed.")

download_files()
