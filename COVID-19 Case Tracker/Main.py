import requests
import matplotlib.pyplot as plt

def covid_tracker():
    print("\nWelcome to Real-Time COVID-19 Case Tracker!")
    country = input("Enter country code (e.g. US, IN, GB): ").upper()
    days = int(input("Enter number of days to fetch data for (e.g. 30): "))
    api_url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays={days}"
    response = requests.get(api_url)
    if response.status_code != 200:
        print("Failed to fetch data. Check country code.")
        return
    data = response.json()
    try:
        cases = data['timeline']['cases']
    except KeyError:
        print("Invalid data received.")
        return
    dates = list(cases.keys())
    values = list(cases.values())

    print(f"\nDaily COVID-19 cases for {country} over last {days} days:")
    for d, v in zip(dates, values):
        print(f"{d}: {v}")

    # Simple plot
    plt.plot(dates, values, marker='o')
    plt.title(f"COVID-19 Cases in {country}")
    plt.xlabel('Date')
    plt.ylabel('Total Cases')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    covid_tracker()
