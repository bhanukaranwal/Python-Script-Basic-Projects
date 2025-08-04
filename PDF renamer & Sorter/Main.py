import os

def pdf_renamer_sorter():
    folder = input("Enter path to folder with PDFs: ")
    if not os.path.exists(folder):
        print("Folder not found.")
        return
    count = 1
    for filename in os.listdir(folder):
        if filename.endswith('.pdf'):
            new_name = f"Document_{count}.pdf"
            os.rename(os.path.join(folder, filename), os.path.join(folder, new_name))
            print(f"Renamed {filename} to {new_name}")
            count += 1
    print("PDFs renamed.")

if __name__ == '__main__':
    pdf_renamer_sorter()
