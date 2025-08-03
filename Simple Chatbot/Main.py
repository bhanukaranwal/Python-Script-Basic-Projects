def simple_chatbot():
    print("Hi, I'm PyBot! Type 'bye' to exit.")
    while True:
        user = input("You: ").lower()
        if 'hello' in user or 'hi' in user:
            print("PyBot: Hello! 😊")
        elif 'how are you' in user:
            print("PyBot: I'm just code, but I'm feeling byte-tastic!")
        elif 'bye' in user:
            print("PyBot: Goodbye! 👋")
            break
        else:
            print("PyBot: Tell me more!")

if __name__ == '__main__':
    simple_chatbot()
