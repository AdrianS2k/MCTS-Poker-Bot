import random
import time 

#card constants
SUITS = ["S", "H", "C", "D"]
RANKS = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]

def create_deck():
    deck = list(range(52))
    random.shuffle(deck)
    return deck

def draw(deck, n):
    cards = deck[:n]
    del deck[:n]
    return cards

def card_to_string(card_id):
    rank = RANKS[card_id % 13]
    suit = SUITS[card_id // 13]

    return f"{rank}{suit}"
deck = create_deck()
bot_hand = draw(deck, 2)
opponent_hand = draw(deck,2)
table_hand = draw(deck, 5)

def evaluate_hand(cards):
    return random.random()


start_time = time.time()

wins = 0
total_runs = 0
while True:
    if time.time() - start_time >= 10:
        break
    new_deck = create_deck()
    bot = draw(new_deck, 2)
    opponent = draw(new_deck, 2)
    table = draw(new_deck, 5)
    bot_score = evaluate_hand(table + bot)
    opponent_score = evaluate_hand(table + opponent)
    if bot_score > opponent_score:
        wins += 1
    total_runs += 1
   

print("wins: ")
print(total_runs)
print("Win probability: ", wins / total_runs)