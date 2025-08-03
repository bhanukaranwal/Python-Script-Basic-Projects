import json
import csv

def json_to_csv(json_file, csv_file):
    with open(json_file) as f:
        data = json.load(f)
    keys = data[0].keys()
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Converted {json_file} to {csv_file}")

def csv_to_json(csv_file, json_file):
    with open(csv_file) as f:
        reader = list(csv.DictReader(f))
    with open(json_file, 'w') as f:
        json.dump(reader, f, indent=4)
    print(f"Converted {csv_file} to {json_file}")

if __name__ == '__main__':
    mode = input("1. JSON to CSV 2. CSV to JSON: ")
    if mode == '1':
        jf = input("Enter JSON file: ")
        cf = input("Enter output CSV file: ")
        json_to_csv(jf, cf)
    elif mode == '2':
        cf = input("Enter CSV file: ")
        jf = input("Enter output JSON file: ")
        csv_to_json(cf, jf)
    else:
        print("Invalid.")
