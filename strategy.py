# strategy.py

class Strategy:
    """
    Base class for player strategies.
    """

    def decide_action(self, hand, dealer_up_card, rules):
        raise NotImplementedError("Strategy must implement decide_action method.")



class BasicStrategy(Strategy):
    """
    Implements a basic Blackjack strategy.
    """

    def decide_action(self, hand, dealer_up_card, rules):
        best_value = hand.get_best_value()
        if best_value < 17:
            return 'hit'
        else:
            return 'stand'



# Test for BasicStrategy class
if __name__ == "__main__":
    from hand import Hand
    from cards import Card
    strategy = BasicStrategy()
    hand = Hand()
    hand.add_card(Card('9', 'Hearts'))
    hand.add_card(Card('7', 'Diamonds'))
    action = strategy.decide_action(hand, None, None)  # Dealer's up card and rules are not used here
    print(f"Decided action: {action}")  # Output: 'hit'
