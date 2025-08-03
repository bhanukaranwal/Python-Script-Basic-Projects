import random

def trivia_tournament():
    questions = [
        ("What is the largest planet in the solar system?", "jupiter"),
        ("Who wrote 'Harry Potter'?", "j.k. rowling"),
        ("What is the capital city of Japan?", "tokyo"),
        ("In what year did the Titanic sink?", "1912"),
    ]
    players = []
    for num in range(2):
        pname = input(f"Enter Player {num+1} name: ")
        players.append({"name": pname, "score": 0})
    for q, a in questions:
        for player in players:
            ans = input(f"{player['name']}, {q} ").strip().lower()
            if ans == a:
                print("Correct!")
                player['score'] += 1
            else:
                print("Nope!")
    print("Final Scores:")
    for p in players:
        print(f"{p['name']}: {p['score']}")
    top_score = max(p["score"] for p in players)
    winners = [p["name"] for p in players if p["score"] == top_score]
    if len(winners) > 1:
        print(f"It's a tie! Randomly picking a winner...")
        print(f"The winner is {random.choice(winners)}!")
    else:
        print(f"The winner is {winners[0]}!")

if __name__ == "__main__":
    trivia_tournament()
