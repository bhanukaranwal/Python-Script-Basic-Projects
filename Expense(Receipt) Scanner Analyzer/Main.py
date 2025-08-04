import os
import csv
from PIL import Image
import pytesseract

def expense_scanner():
    print("\nWelcome to Expense/Receipt Scanner!")
    folder = input("Enter folder path containing receipt images: ").strip()
    output_csv = input("Enter output CSV filename (e.g., expenses.csv): ").strip()

    if not os.path.exists(folder):
        print("Folder does not exist.")
        return

    header = ['Filename', 'Extracted Text Snippet']
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

        for filename in os.listdir(folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                print(f"Processing {filename}...")
                img_path = os.path.join(folder, filename)
                try:
                    text = pytesseract.image_to_string(Image.open(img_path))
                    snippet = text[:200].replace('\n', ' ').strip()
                except Exception as e:
                    snippet = f"Error reading image: {e}"
                writer.writerow([filename, snippet])
    print(f"\nData extraction complete! Saved to {output_csv}")

if __name__ == '__main__':
    print("\nNOTE: This requires Tesseract OCR engine installed on your system.")
    expense_scanner()
