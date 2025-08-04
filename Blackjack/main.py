import random

def blackjack():
    print("\nWelcome to Blackjack!")
    # Card deck where face cards are 10, Ace is 11 (or 1 if over 21)
    def deal_card():
        cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        return random.choice(cards)

    def calculate_score(hand):
        score = sum(hand)
        # Adjust for Aces if bust
        while score > 21 and 11 in hand:
            hand[hand.index(11)] = 1
            score = sum(hand)
        return score

    player = [deal_card(), deal_card()]
    dealer = [deal_card(), deal_card()]
    while True:
        print(f"Your cards: {player} (score: {calculate_score(player)})")
        print(f"Dealer's visible card: {dealer[0]}")
        if calculate_score(player) == 21:
            print("Blackjack! You win!")
            return
        if calculate_score(player) > 21:
            print("Bust! You lose.")
            return
        move = input("Hit or stand? ").lower()
        if move == "hit":
            player.append(deal_card())
        elif move == "stand":
            break
        else:
            print("Please type 'hit' or 'stand'.")
    while calculate_score(dealer) < 17:
        dealer.append(deal_card())
    print(f"\nDealer's cards: {dealer} (score: {calculate_score(dealer)})")
    p_score = calculate_score(player)
    d_score = calculate_score(dealer)
    if d_score > 21 or p_score > d_score:
        print("You win!")
    elif d_score == p_score:
        print("It's a draw.")
    else:
        print("Dealer wins!")

if __name__ == "__main__":
    blackjack()
