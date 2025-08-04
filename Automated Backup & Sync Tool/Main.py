import os
import shutil
from datetime import datetime
import filecmp

def automated_backup():
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
    os.makedirs(backup_folder)

    log_file = os.path.join(backup_root, 'backup_log.txt')
    with open(log_file, "a") as log:
        log.write(f"Backup started at {datetime.now()}\n")

        def copy_files(src, dest):
            names = os.listdir(src)
            for name in names:
                full_src = os.path.join(src, name)
                full_dest = os.path.join(dest, name)

                if os.path.isfile(full_src):
                    if os.path.exists(full_dest):
                        if not filecmp.cmp(full_src, full_dest, shallow=False):
                            shutil.copy2(full_src, full_dest)
                            log.write(f"Updated file: {full_dest}\n")
                            print(f"Updated file: {full_dest}")
                    else:
                        shutil.copy2(full_src, full_dest)
                        log.write(f"Copied file: {full_dest}\n")
                        print(f"Copied file: {full_dest}")

                elif os.path.isdir(full_src):
                    if not os.path.exists(full_dest):
                        os.makedirs(full_dest)
                    copy_files(full_src, full_dest)

        copy_files(source, backup_folder)
        log.write(f"Backup completed at {datetime.now()}\n\n")
        print(f"Backup completed! All updates are in {backup_folder} and logged.")

if __name__ == '__main__':
    automated_backup()
