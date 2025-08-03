import json

def load_json(filename):
    with open(filename) as f:
        return json.load(f)

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def view_students(data):
    for student in data:
        print(student)

def search_by_id(data, sid):
    for student in data:
        if student.get("id") == sid:
            print(student)
            return
    print("Not found.")

def filter_students(data, key, op, val):
    for student in data:
        if op == '>' and float(student[key]) > float(val):
            print(student)
        elif op == '<' and float(student[key]) < float(val):
            print(student)
        elif op == '=' and str(student[key]) == val:
            print(student)

def delete_by_id(data, sid):
    new_data = [s for s in data if s.get("id") != sid]
    return new_data

if __name__ == "__main__":
    fname = input("JSON file name: ")
    data = load_json(fname)
    while True:
        print("Options: 1. View 2. Search by ID 3. Filter 4. Delete by ID 5. Save & Exit")
        opt = input("Choice: ")
        if opt == '1':
            view_students(data)
        elif opt == '2':
            sid = input("Student ID: ")
            search_by_id(data, sid)
        elif opt == '3':
            key = input("Field (cgpa/age): ")
            op = input("Operator (>, <, =): ")
            val = input("Value: ")
            filter_students(data, key, op, val)
        elif opt == '4':
            sid = input("Student ID to delete: ")
            data = delete_by_id(data, sid)
            print("Deleted if found.")
        elif opt == '5':
            save_json(data, fname)
            break
