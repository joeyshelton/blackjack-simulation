# hand.py

class Hand:
    """
    Represents a hand of cards for a player or dealer.
    """

    def __init__(self, bet=0):
        self.cards = []
        self.bet = bet
        self.is_split = False
        self.is_double_down = False
        self.is_surrendered = False
        self.is_complete = False

    def add_card(self, card):
        self.cards.append(card)

    def get_values(self):
        """
        Returns all possible hand values considering Aces as 1 or 11.
        """
        values = [0]
        for card in self.cards:
            if card.rank == 'A':
                temp_values = []
                for val in values:
                    temp_values.extend([val + 1, val + 11])
                values = temp_values
            else:
                for i in range(len(values)):
                    values[i] += card.get_value()
        return set(values)

    def get_best_value(self):
        """
        Returns the highest hand value less than or equal to 21.
        If all values are over 21, returns the minimum value.
        """
        values = self.get_values()
        valid_values = [v for v in values if v <= 21]
        return max(valid_values) if valid_values else min(values)

    def is_blackjack(self):
        return len(self.cards) == 2 and self.get_best_value() == 21

    def is_bust(self):
        return self.get_best_value() > 21

    def can_split(self, rules):
        if len(self.cards) != 2:
            return False
        if self.cards[0].rank != self.cards[1].rank:
            if rules.splitting_rules.get('can_split_unlike_tens', False):
                # Check if both cards are 10-value cards
                return (self.cards[0].get_value() == 10 and self.cards[1].get_value() == 10)
            else:
                return False
        return True

    def can_double_down(self, rules):
        total = self.get_best_value()
        return total in rules.double_down_allowed_on

# Test for Hand class
if __name__ == "__main__":
    from cards import Card
    hand = Hand(bet=100)
    hand.add_card(Card('A', 'Hearts'))
    hand.add_card(Card('K', 'Spades'))
    print(f"Hand value(s): {hand.get_values()}")  # Output: {21, 31}
    print(f"Best hand value: {hand.get_best_value()}")  # Output: 21
    print(f"Is Blackjack: {hand.is_blackjack()}")  # Output: True
