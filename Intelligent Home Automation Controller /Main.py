import threading
import time

class SmartHome:
    def __init__(self):
        self.devices = {
            'light': False,
            'fan': False,
            'heater': False
        }

    def set_device(self, device, state):
        if device in self.devices:
            self.devices[device] = state
            print(f"{device.title()} turned {'ON' if state else 'OFF'}.")
        else:
            print(f"Unknown device '{device}'.")

    def schedule_device(self, device, state, delay_seconds):
        print(f"Scheduling to turn {device} {'ON' if state else 'OFF'} in {delay_seconds} seconds.")
        threading.Timer(delay_seconds, self.set_device, args=[device, state]).start()

    def status(self):
        print("\nCurrent Smart Home Status:")
        for device, is_on in self.devices.items():
            print(f" {device.title()}: {'ON' if is_on else 'OFF'}")

def smart_home_controller():
    home = SmartHome()
    print("\nWelcome to Smart Home Automation CLI")
    print("Commands:")
    print(" - on [device] / off [device]")
    print(" - schedule [device] on/off [seconds]")
    print(" - status")
    print(" - quit\n")

    while True:
        home.status()
        command = input("Enter command: ").lower().strip()
        if command == 'quit':
            print("Exiting Smart Home Controller. Goodbye!")
            break
        elif command == 'status':
            continue
        parts = command.split()
        if len(parts) == 2 and parts[0] in ['on', 'off']:
            home.set_device(parts[1], parts[0] == 'on')
        elif len(parts) == 4 and parts[0] == 'schedule' and parts[2] in ['on', 'off'] and parts[3].isdigit():
            device = parts[1]
            state = parts[2] == 'on'
            delay = int(parts[3])
            home.schedule_device(device, state, delay)
        else:
            print("Invalid command. Try: on light, off fan, schedule heater on 60, status, quit.")

if __name__ == '__main__':
    smart_home_controller()
