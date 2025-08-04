import requests

def weather_fetcher():
    api_key = 'YOUR_API_KEY'   # Sign up at openweathermap.org for a free key
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    city = input('Enter city name: ')
    url = f"{base_url}appid={api_key}&q={city}&units=metric"
    try:
        response = requests.get(url).json()
        if response['cod'] != 200:
            print('City not found.')
            return
        temp = response['main']['temp']
        desc = response['weather'][0]['description']
        print(f"Current temperature in {city}: {temp}°C")
        print(f"Weather description: {desc}")
    except Exception as e:
        print('Error fetching weather data:', e)

if __name__ == "__main__":
    weather_fetcher()
