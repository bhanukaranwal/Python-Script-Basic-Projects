def goal_saving_calculator():
    target = float(input("Enter your financial goal (amount): ₹"))
    years = int(input("In how many years do you aim to achieve it? "))
    rate = float(input("Expected annual interest/growth rate (%)? "))
    per_yr = (target / ((1+rate/100)**years))
    print(f"You'd need to save about ₹{per_yr:.2f} per year at {rate}% to reach ₹{target} in {years} years.")

if __name__ == "__main__":
    goal_saving_calculator()
