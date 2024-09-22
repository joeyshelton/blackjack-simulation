import random

class Card:
    """
    Represents a single playing card in Blackjack.
    """
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10',
             'J', 'Q', 'K', 'A']
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    VALUES = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10,
        'K': 10, 'A': 11  # Ace can be 1 or 11; initially 11
    }

    def __init__(self, rank, suit):
        if rank not in self.RANKS:
            raise ValueError(f"Invalid rank '{rank}'.")
        if suit not in self.SUITS:
            raise ValueError(f"Invalid suit '{suit}'.")
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def get_value(self):
        return self.VALUES[self.rank]


class Deck:
    """
    Represents a standard deck of 52 playing cards.
    """

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if not self.cards:
            raise IndexError("No more cards in the deck.")
        return self.cards.pop()


class Shoe(Deck):
    """
    Represents a shoe containing multiple decks.
    """

    def __init__(self, number_of_decks=6):
        self.number_of_decks = number_of_decks
        self.cards = [Card(rank, suit)
                      for _ in range(number_of_decks)
                      for suit in Card.SUITS
                      for rank in Card.RANKS]
        self.shuffle()



# # Test for Card class
# if __name__ == "__main__":
#     card = Card('A', 'Hearts')
#     print(card)            # Output: A of Hearts
#     print(card.get_value())  # Output: 11

# # Test for Deck class
# if __name__ == "__main__":
#     deck = Deck()
#     print(f"Total cards in deck: {len(deck.cards)}")  # Output: 52
#     card = deck.deal_card()
#     print(f"Dealt card: {card}")  # Output: Random card
#     print(f"Cards left in deck: {len(deck.cards)}")  # Output: 51

# Test for Shoe class
if __name__ == "__main__":
    shoe = Shoe(number_of_decks=6)
    print(f"Total cards in shoe: {len(shoe.cards)}")  # Output: 312 (6 * 52)
    card = shoe.deal_card()
    print(f"Dealt card: {card}")
    print(f"Cards left in shoe: {len(shoe.cards)}")  # Output: 311
