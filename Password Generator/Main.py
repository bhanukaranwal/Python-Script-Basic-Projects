import random
import string

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

if __name__ == "__main__":
    l = int(input("Enter desired password length (default 12): ") or 12)
    print(f"Generated Password: {generate_password(l)}")
