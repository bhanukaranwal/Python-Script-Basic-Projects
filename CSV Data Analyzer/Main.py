import csv

def load_csv(file):
    with open(file, newline='') as f:
        reader = list(csv.DictReader(f))
    return reader

def analyze_data(data):
    print(f"Total records: {len(data)}")
    if data:
        print("Fields:", ', '.join(data[0].keys()))

def show_menu():
    print("1. Display Data")
    print("2. Filter by Field")
    print("3. Exit")

def filter_data(data, field, value):
    return [row for row in data if row.get(field) == value]

if __name__ == "__main__":
    fname = input("CSV file name: ")
    data = load_csv(fname)
    analyze_data(data)
    while True:
        show_menu()
        ch = input("Choice: ")
        if ch == '1':
            for row in data:
                print(row)
        elif ch == '2':
            field = input("Field: ")
            value = input("Value: ")
            filtered = filter_data(data, field, value)
            print(f"Found {len(filtered)} records.")
            for row in filtered:
                print(row)
        elif ch == '3':
            break
        else:
            print("Invalid.")
