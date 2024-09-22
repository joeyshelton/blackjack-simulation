# rules.py

class Rules:
    """
    Encapsulates all game rule variations.
    """

    def __init__(
        self,
        blackjack_payout=1.5,
        number_of_decks=6,
        dealer_hits_soft_17=False,
        double_down_allowed_on=None,
        double_after_split_allowed=True,
        splitting_rules=None,
        surrender_allowed='none',
        insurance_offered=True,
        insurance_payout=2.0
    ):
        self.blackjack_payout = blackjack_payout
        self.number_of_decks = number_of_decks
        self.dealer_hits_soft_17 = dealer_hits_soft_17
        self.double_down_allowed_on = double_down_allowed_on or [9, 10, 11]
        self.double_after_split_allowed = double_after_split_allowed
        self.splitting_rules = splitting_rules or {
            'max_splits': 3,
            'can_split_aces': True,
            'resplit_aces_allowed': False,
            'can_split_unlike_tens': False,
        }
        self.surrender_allowed = surrender_allowed  # 'late', 'early', 'none'
        self.insurance_offered = insurance_offered
        self.insurance_payout = insurance_payout
        self.validate_rules()

    def validate_rules(self):
        # Add validation logic if necessary
        pass


# Test for Rules class
if __name__ == "__main__":
    rules = Rules()
    print(f"Blackjack payout: {rules.blackjack_payout}")  # Output: 1.5
    print(f"Dealer hits soft 17: {rules.dealer_hits_soft_17}")  # Output: False
