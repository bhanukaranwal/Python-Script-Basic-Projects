import hashlib

class URLShortener:
    def __init__(self):
        self.url_map = {}

    def shorten(self, long_url):
        url_hash = hashlib.md5(long_url.encode()).hexdigest()[:6]
        self.url_map[url_hash] = long_url
        return f"http://short.ly/{url_hash}"

    def retrieve(self, short_code):
        code = short_code.split('/')[-1]
        return self.url_map.get(code, "URL not found")

if __name__ == "__main__":
    shortener = URLShortener()
    while True:
        op = input("1. Shorten\n2. Retrieve\n3. Exit\nChoose: ")
        if op == '1':
            url = input("Enter URL: ")
            print("Shortened URL:", shortener.shorten(url))
        elif op == '2':
            s_url = input("Enter short URL: ")
            print("Original URL:", shortener.retrieve(s_url))
        elif op == '3':
            break
        else:
            print("Invalid choice.")
