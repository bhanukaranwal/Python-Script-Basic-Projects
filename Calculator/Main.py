def calculator():
    print("Simple Calculator")
    print("Operations: +, -, *, /, **, %")
    while True:
        try:
            expr = input("Enter calculation (e.g., 2 + 3) or 'exit': ")
            if expr.lower() == 'exit':
                break
            result = eval(expr)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Invalid input: {e}")

if __name__ == "__main__":
    calculator()
