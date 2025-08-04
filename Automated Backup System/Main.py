import os
import shutil
from datetime import datetime

def backup_files():
    print("\nWelcome to Automated Backup System!")
    source = input("Enter source folder path: ")
    backup_root = input("Enter backup folder path: ")
    if not os.path.exists(source):
        print("Source folder does not exist.")
        return
    if not os.path.exists(backup_root):
        os.makedirs(backup_root)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_folder = os.path.join(backup_root, f"backup_{timestamp}")
    shutil.copytree(source, backup_folder)
    print(f"Backup created at {backup_folder}")

if __name__ == '__main__':
    backup_files()
