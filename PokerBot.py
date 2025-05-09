import random
import time 
from collections import Counter


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

class PokerBot:
    def __init__(self, hole_cards, community_cards):
        self.hole_cards = hole_cards
        self.community_cards = community_cards

    def evaluate_hand(self, cards):
        ranks = [card % 13 for card in cards]
        suits = [card // 13 for card in cards]

        #Set them to specific keys for counting occurrences
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)

        flush_suit = None
        for suit, count in suit_counts.items():
            if count >= 5:
                flush_suit = suit
                break
        #ace = 12
        unique_ranks = sorted(set(ranks)) #need to account for Ace in front
        if 12 in unique_ranks:
            unique_ranks = [0] + unique_ranks
        return random.random()
    
    def estimate_win_probability(self, time_limit=10):
        start_time = time.time()
        wins = 0
        total_runs = 0

        while True:
            if time.time() - start_time >= time_limit:
                break
            deck = create_deck()
            known_cards = self.hole_cards + self.community_cards
            deck = [c for c  in deck if c not in known_cards]
            opponent_hand = draw(deck, 2)
            remaining_board_cards = 5 - len(self.community_cards)
            future_community = draw(deck, remaining_board_cards)

            full_community = self.community_cards + future_community

            bot_score = self.evaluate_hand(self.hole_cards + full_community)
            opponent_score = self.evaluate_hand(opponent_hand + full_community)
            if bot_score > opponent_score:
                wins += 1
            total_runs += 1
            



        return wins / total_runs if total_runs > 0 else 0
    
    def make_decision(self):
        prob = self.estimate_win_probability()
        print(f"Estimated Win Probability: {prob:3f}")
        return "Stay" if prob >= 0.5 else "FOLD"
    



def test_evaluate_hand():
    bot = PokerBot([], [])

    def make_card(rank, suit):
        return SUITS.index(suit) * 13 + RANKS.index(rank)

    # Test 1: Pair of Aces
    hand1 = [make_card('A', 'S'), make_card('A', 'H'), make_card('5', 'C'),
             make_card('8', 'D'), make_card('2', 'S'), make_card('9', 'H'), make_card('J', 'C')]
    
    # Test 2: Flush (all hearts)
    hand2 = [make_card('2', 'H'), make_card('5', 'H'), make_card('9', 'H'),
             make_card('J', 'H'), make_card('Q', 'H'), make_card('3', 'S'), make_card('K', 'D')]

    # Test 3: Straight (5-6-7-8-9)
    hand3 = [make_card('5', 'S'), make_card('6', 'D'), make_card('7', 'C'),
             make_card('8', 'H'), make_card('9', 'S'), make_card('J', 'D'), make_card('3', 'H')]

    # Run evaluate_hand (currently returns random, will improve later)
    print("Pair of Aces hand score:", bot.evaluate_hand(hand1))
    print("Flush hand score:", bot.evaluate_hand(hand2))
    print("Straight hand score:", bot.evaluate_hand(hand3))

test_evaluate_hand()
# if __name__ == "__main__":
#     full_deck = create_deck()
#     random.shuffle(full_deck)

#     bot_hand = draw(full_deck, 2)
#     community_cards = draw(full_deck, 3)  # Simulate the flop

#     bot = PokerBot(bot_hand, community_cards)

#     print("Bot hole cards:", [card_to_string(c) for c in bot_hand])
#     print("Community cards:", [card_to_string(c) for c in community_cards])
#     print("Decision:", bot.make_decision())
