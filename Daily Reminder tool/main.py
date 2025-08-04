import time

def daily_reminder():
    reminders = []
    print("\nWelcome to Daily Reminder Tool!")
    while True:
        print("1. Add Reminder\n2. Start Reminding\n3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            reminder = input("Enter reminder text: ")
            delay = int(input("Remind after how many seconds? "))
            reminders.append((reminder, delay))
            print("Reminder added!")
        elif choice == '2':
            print("Starting reminders...")
            for reminder, delay in reminders:
                time.sleep(delay)
                print(f"Reminder: {reminder}")
            print("All reminders done.")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    daily_reminder()
