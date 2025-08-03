def encode_decode():
    print("1. Encode a secret\n2. Decode a message")
    choice = input("Pick an option: ")
    if choice == '1':
        text = input("Type your secret message: ")
        code = ''.join(chr(ord(c)+3) for c in text)
        print("Your encoded message:", code)
    elif choice == '2':
        code = input("Type the encoded message: ")
        text = ''.join(chr(ord(c)-3) for c in code)
        print("Your decoded message:", text)
    else:
        print("Invalid option!")

if __name__ == '__main__':
    encode_decode()
