def bill_splitter():
    total = float(input("Total bill amount: ₹"))
    num = int(input("Number of people: "))
    for i in range(num):
        name = input(f"Name of person {i+1}: ")
        p = float(input(f"How much did {name} pay? ₹"))
        print(f"{name} paid ₹{p:.2f}")
    due = total/num
    print(f"Each person should pay: ₹{due:.2f}")

if __name__ == "__main__":
    bill_splitter()
