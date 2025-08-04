import os
import shutil

def organize_files():
    print("\nWelcome to File Organizer!")
    folder = input("Enter the path of folder to organize: ")
    if not os.path.exists(folder):
        print("Folder not found.")
        return
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath):
            ext = filename.split('.')[-1].lower()
            dest_dir = os.path.join(folder, ext + '_files')
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            shutil.move(filepath, os.path.join(dest_dir, filename))
            print(f"Moved {filename} to {dest_dir}")
    print("Organization complete!")

if __name__ == '__main__':
    organize_files()
