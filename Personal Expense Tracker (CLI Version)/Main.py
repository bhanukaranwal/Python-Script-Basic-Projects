import json
import datetime

def load_data(filename='expenses.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except:
        return []

def save_data(expenses, filename='expenses.json'):
    with open(filename, 'w') as file:
        json.dump(expenses, file, indent=2)

def add_expense(expenses):
    amount = float(input("Amount spent: ₹"))
    category = input("Category (e.g., food, bills, fun): ").lower()
    note = input("Short note: ")
    date = input("Date (YYYY-MM-DD, blank for today): ")
    if not date:
        date = str(datetime.date.today())
    expenses.append({"amount": amount, "category": category, "note": note, "date": date})
    print("Expense added!")

def show_summary(expenses):
    from collections import defaultdict
    summary = defaultdict(float)
    for e in expenses:
        summary[e['category']] += e['amount']
    print("Expense Summary by Category:")
    for cat, total in summary.items():
        print(f"{cat.title()}: ₹{total:.2f}")

if __name__ == "__main__":
    expenses = load_data()
    while True:
        print("\n1. Add Expense\n2. View All\n3. Summary\n4. Save & Exit")
        choice = input("Choose: ")
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            for e in expenses:
                print(e)
        elif choice == "3":
            show_summary(expenses)
        elif choice == "4":
            save_data(expenses)
            print("Saved. Goodbye!")
            break
        else:
            print("Invalid.")
