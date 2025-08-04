import os
import shutil
from datetime import datetime

def smart_file_organizer():
    print("\nWelcome to Smart File Organizer!")
    folder = input("Enter folder path to organize: ").strip()
    if not os.path.exists(folder):
        print("Folder does not exist.")
        return

    # Define sorting rules: expand as you like!
    rules = {
        'images': ['jpg', 'jpeg', 'png', 'gif', 'bmp'],
        'documents': ['pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx', 'ppt', 'pptx'],
        'videos': ['mp4', 'avi', 'mov', 'mkv'],
        'audio': ['mp3', 'wav', 'aac'],
        'archives': ['zip', 'rar', '7z', 'tar', 'gz']
    }

    log_file = os.path.join(folder, "organizer_log.txt")
    with open(log_file, "a") as log:
        log.write(f"Organizing started at {datetime.now()}\n")
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath):
                ext = filename.split('.')[-1].lower()
                moved = False
                for category, exts in rules.items():
                    if ext in exts:
                        dest_dir = os.path.join(folder, category)
                        os.makedirs(dest_dir, exist_ok=True)
                        shutil.move(filepath, os.path.join(dest_dir, filename))
                        log.write(f"Moved {filename} to {category}\n")
                        print(f"Moved {filename} to folder '{category}'")
                        moved = True
                        break
                if not moved:
                    other_dir = os.path.join(folder, "others")
                    os.makedirs(other_dir, exist_ok=True)
                    shutil.move(filepath, os.path.join(other_dir, filename))
                    log.write(f"Moved {filename} to others\n")
                    print(f"Moved {filename} to folder 'others'")
        log.write(f"Organizing completed at {datetime.now()}\n\n")

if __name__ == '__main__':
    smart_file_organizer()
