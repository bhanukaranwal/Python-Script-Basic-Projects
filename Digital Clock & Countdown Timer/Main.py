import time
import threading

def digital_clock():
    print("Press Ctrl+C to stop digital clock.")
    try:
        while True:
            print(time.strftime("%H:%M:%S"), end='\r')
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nClock stopped.")

def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        print(f"Time left: {i}s", end='\r')
        time.sleep(1)
    print("\nCountdown finished!")

if __name__ == "__main__":
    choice = input("Choose: 1. Digital Clock 2. Countdown Timer: ")
    if choice == '1':
        digital_clock()
    elif choice == '2':
        seconds = int(input("Enter seconds: "))
        countdown_timer(seconds)
    else:
        print("Invalid choice.")
