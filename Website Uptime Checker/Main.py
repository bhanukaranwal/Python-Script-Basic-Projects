import requests

def website_uptime_checker():
    urls = input("Enter website URLs (comma separated): ").split(',')
    for url in urls:
        url = url.strip()
        if not url.startswith('http'):
            url = 'http://' + url
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"{url} is UP!")
            else:
                print(f"{url} might be down (status {response.status_code})")
        except Exception as e:
            print(f"{url} is DOWN! Error: {e}")

if __name__ == '__main__':
    website_uptime_checker()
