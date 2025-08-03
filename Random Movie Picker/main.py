import random

def movie_picker():
    movies = ["Inception", "Spider-Man", "The Lion King", "Up", "Avengers", "Finding Nemo", "Toy Story"]
    print("Can’t decide what to watch?")
    input("Press Enter for a movie recommendation: ")
    print(f"You should watch: {random.choice(movies)}!")

if __name__ == "__main__":
    movie_picker()
