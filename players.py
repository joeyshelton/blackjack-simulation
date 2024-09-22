from hand import Hand
from cards import Card

class Player:
    """
    Represents a player in the game.
    """

    def __init__(self, bankroll=1000, strategy=None, name="Player"):
        self.hands = []
        self.bankroll = bankroll
        self.strategy = strategy
        self.name = name

    def place_bet(self, amount):
        if amount > self.bankroll:
            raise ValueError("Bet amount exceeds bankroll.")
        self.bankroll -= amount
        hand = Hand(bet=amount)
        self.hands.append(hand)
        return hand

    def decide_action(self, hand, dealer_up_card, rules):
        if self.strategy:
            return self.strategy.decide_action(hand, dealer_up_card, rules)
        else:
            raise NotImplementedError("No strategy defined for player.")

    def receive_card(self, hand, card):
        hand.add_card(card)

    def split_hand(self, hand):
        if len(hand.cards) != 2:
            raise ValueError("Cannot split hand that doesn't have exactly two cards.")
        new_hand = Hand(bet=hand.bet)
        new_hand.add_card(hand.cards.pop())
        self.hands.append(new_hand)
        return new_hand

    def double_down(self, hand):
        additional_bet = hand.bet
        if additional_bet > self.bankroll:
            raise ValueError("Insufficient bankroll to double down.")
        self.bankroll -= additional_bet
        hand.bet += additional_bet
        hand.is_double_down = True

    def surrender(self, hand):
        hand.is_surrendered = True
        refund = hand.bet / 2
        self.bankroll += refund

    def clear_hands(self):
        self.hands = []


class Dealer(Player):
    """
    Represents the dealer in the game.
    """

    def __init__(self, name="Dealer"):
        super().__init__(bankroll=float('inf'), strategy=None, name=name)

    def play_hand(self, hand, rules, shoe):
        while self.must_hit(hand, rules):
            card = shoe.deal_card()  # Use the shoe passed as an argument
            self.receive_card(hand, card)

    def must_hit(self, hand, rules):
        value = hand.get_best_value()
        if value < 17:
            return True
        elif value == 17:
            if rules.dealer_hits_soft_17:
                # Check if hand is soft (contains an Ace counted as 11)
                values = hand.get_values()
                if any(v == 17 for v in values) and any(card.rank == 'A' for card in hand.cards):
                    return True
        return False

# Test for Player class
if __name__ == "__main__":
    from hand import Hand
    from cards import Card
    class MockStrategy:
        def decide_action(self, hand, dealer_up_card, rules):
            return 'stand'

    player = Player(bankroll=1000, strategy=MockStrategy())
    hand = player.place_bet(100)
    player.receive_card(hand, Card('8', 'Hearts'))
    player.receive_card(hand, Card('8', 'Diamonds'))
    print(f"Player bankroll: {player.bankroll}")  # Output: 900
    print(f"Hand cards: {[str(card) for card in hand.cards]}")  # Output: ['8 of Hearts', '8 of Diamonds']
    # Attempt to split
    try:
        if hand.can_split(None):  # Passing None as rules for now
            player.split_hand(hand)
    except Exception as e:
        print(e)  # Output: 'NoneType' object has no attribute 'splitting_rules'
