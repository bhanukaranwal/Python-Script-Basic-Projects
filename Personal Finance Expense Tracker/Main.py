import csv
import os

def finance_tracker():
    filename = 'expenses.csv'
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Category', 'Amount', 'Note'])

    def add_expense():
        date = input('Date (YYYY-MM-DD): ')
        category = input('Category: ')
        amount = input('Amount: ')
        note = input('Note: ')
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([date, category, amount, note])
        print('Expense added!')

    def view_expenses():
        with open(filename) as f:
            reader = csv.reader(f)
            print('\nAll Expenses:')
            for row in reader:
                print(', '.join(row))

    while True:
        print('\nExpense Tracker Menu:')
        print('1. Add Expense')
        print('2. View Expenses')
        print('3. Exit')
        choice = input('Enter choice: ')
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            break
        else:
            print('Invalid choice.')

if __name__ == "__main__":
    finance_tracker()
