import requests
import matplotlib.pyplot as plt

def air_quality_dashboard():
    print("\nWelcome to the Real-Time Air Quality Dashboard!")
    # Ask for your city of interest (example: Delhi, London)
    city = input("Enter city name (e.g., Delhi, London): ")
    days = 7
    # Uses OpenAQ public API for PM2.5 measurements
    url = f"https://api.openaq.org/v2/measurements?city={city}&limit=100&parameter=pm25&order_by=datetime&sort=desc"
    try:
        response = requests.get(url)
        data = response.json()
        if 'results' not in data or not data['results']:
            print(f"No PM2.5 data found for {city}.")
            return
        # Get the latest measurements (up to one per day)
        results = data['results'][:days]
        dates = [r['date']['utc'][:10] for r in results][::-1]  # Latest to chronological
        values = [r['value'] for r in results][::-1]
        print(f"\nPM2.5 values for the last {days} measurements in {city}:")
        for d, v in zip(dates, values):
            print(f"{d}: {v} µg/m³")
        # Plot the results
        plt.plot(dates, values, marker='o')
        plt.title(f"Real-Time PM2.5 Levels in {city} (last {days} measurements)")
        plt.xticks(rotation=45)
        plt.xlabel('Date')
        plt.ylabel('PM2.5 (µg/m³)')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print("Error fetching or plotting data:", e)

if __name__ == '__main__':
    air_quality_dashboard()
