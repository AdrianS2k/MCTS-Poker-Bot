import random
import time
import math
from collections import Counter
from itertools import combinations


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
        cards_as_strings = [card_to_string(card) for card in cards]

        # Set them to specific keys for counting occurrences
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)

        flush_suit = None
        for suit, count in suit_counts.items():
            if count >= 5:  # if there are 5 of one suit then there is a flush
                flush_suit = suit
                break
        # ace = 12
        unique_ranks = sorted(set(ranks))  # need to account for Ace in front
        if 12 in unique_ranks:
            unique_ranks = [0] + unique_ranks

        # check straight "This hand contains five cards of sequential rank in at least two different suits"
        straight = False
        upper_card = None
        for i in range(len(unique_ranks) - 4):
            window = unique_ranks[i:i + 5]
            if window[4] - window[0] == 4 and len(window) == 5:  #
                straight = True
                upper_card = window[4]
                # print("there's a straight!")

        # check for a straight flush "This hand contains five cards in sequence, all of same suit"
        straight_flush = False
        royal_flush = False
        if flush_suit is not None:
            cards = [card for card in cards if card // 13 == flush_suit]
            flush_ranks = sorted(set([card % 13 for card in cards]))
            for i in range(len(flush_ranks) - 4):
                window = flush_ranks[i: i+5]
                if window[4] - window[0] == 4 and len(window) == 5:
                    if window == [8, 9, 10, 11,12]:
                        royal_flush = True
                        # print("there's a royal flush")
                    else:
                        straight_flush = True
                        # print("there's a straight flush!")
                    upper_card = window[4]
                    break

        if royal_flush: # royal flush
            return (10, [upper_card])
        elif straight_flush: # straight flush
            return (9, [upper_card])
        elif 4 in rank_counts.values(): # 4 of a kind
            card = [r for r, c in rank_counts.items() if c == 4][0]
            take = max(r for r in ranks if r != card) # grab other highest card
            return (8, [card, take])
        elif 3 in rank_counts.values() and 2 in rank_counts.values(): # full house
            threeCard = [r for r, c in rank_counts.items() if c == 3][0]
            twoCard = [r for r, c in rank_counts.items() if c == 2][0]
            return (7, [threeCard, twoCard])
        elif flush_suit: # regular flush
            flush_cards = sorted([r for i, r in enumerate(ranks) if suits[i] == flush_suit], reverse=True)[:5]
            return (6, flush_cards)
        elif straight:  # regular straight
            return (5, [upper_card])
        elif 3 in rank_counts.values() and 2 not in rank_counts.values(): # 3 of a kind and 2 randoms
            threeCard = [r for r, c in rank_counts.items() if c == 3][0]
            firstCard = max(r for r in ranks if r != threeCard)
            secondCard = max(r for r in ranks if r != threeCard and r != firstCard)
            return (3, [threeCard, firstCard, secondCard])
        elif list(rank_counts.values()).count(2) >= 2:  # two pairs
            pairs = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)[:2]
            other = max(r for r in ranks if r not in pairs)
            return (2, pairs + [other])
        elif 2 in rank_counts.values(): # one pair
            pairCard = [r for r, c in rank_counts.items() if c == 2][0]
            firstCard = max(r for r in ranks if r != pairCard)
            secondCard = max(r for r in ranks if r != pairCard and r != firstCard)
            thirdCard = max(r for r in ranks if r != pairCard and r != firstCard and r != secondCard)
            return (1, [pairCard, firstCard, secondCard, thirdCard])
        else:
            top = sorted(ranks, reverse=True)[: 5]
            return (0, top)
    
    def estimate_win_probability(self, time_limit=10):
        start_time = time.time()
        wins = 0
        known = set(self.hole_cards + self.community_cards)
        full_deck = create_deck()
        deck = [c for c in full_deck if c not in known]
        hand_list = list(combinations(deck, 2))


        stats = {hand: {'wins': 0, 'runs': 0} for hand in hand_list}
        total_runs = 0
        # start simulation
        while time.time() - start_time < time_limit:
            total_runs += 1
            # selection using UCB1
            best_hand = None
            best_score = float('-inf')
            for hand, data in stats.items():
                runs = data['runs']
                if runs == 0:
                    ucb = float('inf')
                else:
                    win_rate = data['wins'] / runs
                    ucb = win_rate + 2.0 * math.sqrt(math.log(total_runs) / runs)
                if ucb > best_score:
                    best_score = ucb
                    best_hand = hand


            temp = [c for c in deck if c not in best_hand]
            random.shuffle(temp)
            opponent_hand = list(best_hand)
            remaining_board_cards = 5 - len(self.community_cards)
            future = draw(temp, remaining_board_cards)
            full_community = self.community_cards + future

            bot_score = self.evaluate_hand(self.hole_cards + full_community)
            opponent_score = self.evaluate_hand(opponent_hand + full_community)
            if bot_score > opponent_score:
                stats[best_hand]['wins'] += 1
            stats[best_hand]['runs'] += 1
        wins = [data['wins'] / data['runs'] for data in stats.values() if data['runs'] >0] # mean of hand win rates
        return sum(wins) / len(wins) if wins else 0

    

    def make_decision(self):
        prob = self.estimate_win_probability()
        print(f"Estimated Win Probability: {prob:3f}")
        return "Stay" if prob >= 0.5 else "FOLD"
    

if __name__ == "__main__":
    full_deck = create_deck()
    bot_hand = draw(full_deck, 2)
    community_cards = draw(full_deck, 3)
    bot = PokerBot(bot_hand, community_cards)

    print("Bot cards:", [card_to_string(c) for c in bot_hand])
    print("Community cards:", [card_to_string(c) for c in community_cards])

    decision = bot.make_decision()
    print("Bot decision:", decision)

# def test_evaluate_hand():
#     bot = PokerBot([], [])

#     def make_card(rank, suit):
#         return SUITS.index(suit) * 13 + RANKS.index(rank)

#     # Test 1: Pair of Aces
#     hand1 = [make_card('A', 'S'), make_card('A', 'H'), make_card('5', 'C'),
#              make_card('8', 'D'), make_card('2', 'S'), make_card('9', 'H'), make_card('J', 'C')]
    
#     # Test 2: Flush (all hearts)
#     hand2 = [make_card('2', 'H'), make_card('5', 'H'), make_card('9', 'H'),
#              make_card('J', 'H'), make_card('Q', 'H'), make_card('3', 'S'), make_card('K', 'D')]

#     # Test 3: Straight (5-6-7-8-9)
#     hand3 = [make_card('5', 'S'), make_card('6', 'D'), make_card('7', 'C'),
#              make_card('8', 'H'), make_card('9', 'S'), make_card('J', 'D'), make_card('3', 'H')]

#     # Run evaluate_hand (currently returns random, will improve later)
#     print("Pair of Aces hand score:", bot.evaluate_hand(hand1))
#     print("Flush hand score:", bot.evaluate_hand(hand2))
#     print("Straight hand score:", bot.evaluate_hand(hand3))

