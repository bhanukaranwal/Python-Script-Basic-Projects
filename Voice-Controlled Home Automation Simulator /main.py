# Voice-Controlled Home Automation Simulator — main.py

class SmartHomeSimulator:
    def __init__(self):
        # Simulated home devices with states
        self.devices = {
            'lights': False,           # False=off, True=on
            'thermostat': 22,          # temperature in Celsius
            'media_player': 'stopped', # 'playing', 'paused', 'stopped'
            'security_alarm': False    # False=disarmed, True=armed
        }

    def process_command(self, command: str):
        command = command.lower()
        response = "Sorry, I didn't understand the command."

        if 'light' in command:
            if 'on' in command:
                self.devices['lights'] = True
                response = "Lights turned on."
            elif 'off' in command:
                self.devices['lights'] = False
                response = "Lights turned off."
        elif 'temperature' in command or 'thermostat' in command:
            import re
            match = re.search(r'\\b(\\d+)( degree)?s?\\b', command)
            if match:
                temp = int(match.group(1))
                self.devices['thermostat'] = temp
                response = f"Thermostat set to {temp} degrees Celsius."
            else:
                response = f"Current thermostat temperature is {self.devices['thermostat']} Celsius."
        elif 'play' in command and 'music' in command:
            self.devices['media_player'] = 'playing'
            response = "Music started playing."
        elif 'pause' in command and 'music' in command:
            self.devices['media_player'] = 'paused'
            response = "Music paused."
        elif 'stop' in command and 'music' in command:
            self.devices['media_player'] = 'stopped'
            response = "Music stopped."
        elif 'security' in command or 'alarm' in command:
            if 'arm' in command or 'activate' in command:
                self.devices['security_alarm'] = True
                response = "Security alarm armed."
            elif 'disarm' in command or 'deactivate' in command:
                self.devices['security_alarm'] = False
                response = "Security alarm disarmed."
        return response

if __name__ == '__main__':
    smart_home = SmartHomeSimulator()

    print("Welcome to the Voice-Controlled Home Automation Simulator!")
    print("Type your commands (e.g., 'turn lights on', 'set thermostat to 24', 'play music') or 'exit' to quit.")

    while True:
        command = input("Say a command: ")
        if command.lower() == 'exit':
            print("Goodbye!")
            break
        response = smart_home.process_command(command)
        print(response)

# Next steps:
# - Add a speech-to-text input using SpeechRecognition or similar
# - Create a GUI showing device states in real time
# - Integrate reinforcement learning for automated energy optimization
# - Implement scheduling/automation rules ("turn on lights at 7 PM")
