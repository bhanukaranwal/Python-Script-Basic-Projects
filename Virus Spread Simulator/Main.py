import random

def virus_spread_simulator():
    print("\nWelcome to Virus Spread Simulator!")
    population = 100
    infected = 1
    immune = 0
    days = 0
    while infected > 0 and infected < population:
        print(f"\nDay {days}: Infected={infected}, Immune={immune}, Susceptible={population - infected - immune}")
        new_infections = 0
        for _ in range(infected):
            # Each infected can infect 0-2 new people each day randomly
            new_infections += random.randint(0, 2)
        new_infections = min(new_infections, population - infected - immune)
        print(f"New infections today: {new_infections}")
        choice = input("Choose action: 'lockdown' to reduce spread, 'no' for no action: ").lower()
        if choice == 'lockdown':
            new_infections = max(0, new_infections // 3)
            print("Lockdown reduces new infections dramatically!")
        recovered = infected // 4  # 25% recover per day
        infected += new_infections - recovered
        immune += recovered
        days += 1
    if infected == 0:
        print(f"\nVirus defeated in {days} days! Population healthy with {immune} immune.")
    else:
        print(f"\nInfection has spread to entire population in {days} days.")

if __name__ == '__main__':
    virus_spread_simulator()
