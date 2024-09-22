# game.py

from cards import Shoe
from hand import Hand
from players import Player, Dealer
from rules import Rules

class Game:
    """
    Manages the flow of the game.
    """

    def __init__(self, players, dealer, rules, table_limits=(10, 1000)):
        self.players = players
        self.dealer = dealer
        self.rules = rules
        self.table_limits = table_limits
        self.shoe = Shoe(number_of_decks=rules.number_of_decks)
        self.shoe.shuffle()
        self.current_round = 0
        self.round_over = False

    def start_round(self):
            self.current_round += 1
            print(f"--- Starting Round {self.current_round} ---")
            self.dealer.clear_hands()
            for player in self.players:
                player.clear_hands()
                bet = self.get_player_bet(player)
                player.place_bet(bet)
            self.deal_initial_cards()
            self.check_for_blackjacks()
            if not self.round_over:
                self.player_actions()
                self.dealer_actions()
            self.settle_bets()
            self.check_shoe()

    def get_player_bet(self, player):
        # For testing, we can use a fixed bet
        return self.table_limits[0]

    def deal_initial_cards(self):
        # Deal two cards to each player and one to the dealer
        for player in self.players:
            for hand in player.hands:
                card1 = self.shoe.deal_card()
                card2 = self.shoe.deal_card()
                player.receive_card(hand, card1)
                player.receive_card(hand, card2)
        dealer_hand = Hand()
        dealer_hand.add_card(self.shoe.deal_card())
        dealer_hand.add_card(self.shoe.deal_card())
        self.dealer.hands.append(dealer_hand)

    def player_actions(self):
        for player in self.players:
            for hand in player.hands:
                if hand.is_complete:
                    continue  # Skip hands that are already complete
                self.play_hand(player, hand)


    def play_hand(self, player, hand):
        while True:
            action = player.decide_action(hand, self.dealer_up_card(), self.rules)
            if action == 'hit':
                card = self.shoe.deal_card()
                player.receive_card(hand, card)
                if hand.is_bust():
                    break
            elif action == 'stand':
                break
            elif action == 'double':
                if self.rules.double_down_allowed_on and hand.can_double_down(self.rules):
                    player.double_down(hand)
                    card = self.shoe.deal_card()
                    player.receive_card(hand, card)
                    break
                else:
                    print("Double down not allowed.")
                    continue
            elif action == 'split':
                if hand.can_split(self.rules):
                    new_hand = player.split_hand(hand)
                    player.receive_card(hand, self.shoe.deal_card())
                    player.receive_card(new_hand, self.shoe.deal_card())
                    self.play_hand(player, hand)
                    self.play_hand(player, new_hand)
                    return
                else:
                    print("Split not allowed.")
                    continue
            elif action == 'surrender':
                if self.rules.surrender_allowed != 'none':
                    player.surrender(hand)
                    break
                else:
                    print("Surrender not allowed.")
                    continue
            else:
                print(f"Unknown action '{action}'.")
                break

    def dealer_up_card(self):
        return self.dealer.hands[0].cards[0]

    def dealer_actions(self):
        hand = self.dealer.hands[0]
        print(f"\nDealer's initial hand: {[str(card) for card in hand.cards]}")
        self.dealer.play_hand(hand, self.rules, self.shoe)
        print(f"Dealer's final hand: {[str(card) for card in hand.cards]} with value {hand.get_best_value()}")

    def settle_bets(self):
        dealer_hand = self.dealer.hands[0]
        dealer_value = dealer_hand.get_best_value()
        dealer_blackjack = dealer_hand.is_blackjack()
        dealer_bust = dealer_hand.is_bust()
        print(f"\nDealer's hand {[str(card) for card in dealer_hand.cards]} with value {dealer_value}")
        for player in self.players:
            for hand in player.hands:
                if hand.is_surrendered:
                    print(f"{player.name} surrendered. Half of the bet is returned.")
                    continue
                player_value = hand.get_best_value()
                player_blackjack = hand.is_blackjack()
                if player_blackjack:
                    if dealer_blackjack:
                        # Both player and dealer have blackjack: push
                        player.bankroll += hand.bet
                        result = 'push'
                    else:
                        # Player has blackjack, dealer does not
                        payout = hand.bet + hand.bet * self.rules.blackjack_payout
                        player.bankroll += payout
                        result = 'blackjack'
                elif dealer_blackjack:
                    # Dealer has blackjack, player does not
                    result = 'lose'
                elif hand.is_bust():
                    result = 'lose'
                elif dealer_bust or player_value > dealer_value:
                    payout = hand.bet * 2
                    player.bankroll += payout
                    result = 'win'
                elif player_value == dealer_value:
                    player.bankroll += hand.bet
                    result = 'push'
                else:
                    result = 'lose'
                print(f"{player.name}'s hand {[str(card) for card in hand.cards]} with value {player_value}: {result}")



    def check_shoe(self):
        # Reshuffle the shoe if necessary
        if len(self.shoe.cards) < (self.rules.number_of_decks * 52) * 0.25:
            print("Reshuffling the shoe.")
            self.shoe = Shoe(number_of_decks=self.rules.number_of_decks)
            self.shoe.shuffle()

    def reset_for_next_round(self):
        # This method can be used if additional cleanup is needed
        pass

    def check_for_blackjacks(self):
        self.round_over = False
        dealer_hand = self.dealer.hands[0]
        dealer_blackjack = dealer_hand.is_blackjack()

        for player in self.players:
            for hand in player.hands:
                player_blackjack = hand.is_blackjack()
                if player_blackjack:
                    if dealer_blackjack:
                        # Both have blackjack: push
                        player.bankroll += hand.bet
                        print(f"{player.name} and dealer both have blackjack. It's a push.")
                    else:
                        # Player has blackjack, dealer does not
                        payout = hand.bet + (hand.bet * self.rules.blackjack_payout)
                        player.bankroll += payout
                        print(f"{player.name} has blackjack and wins!")
                    # Mark hand as completed
                    hand.is_complete = True

        # If dealer has blackjack and players do not
        if dealer_blackjack:
            print("Dealer has blackjack.")
            for player in self.players:
                for hand in player.hands:
                    if not hand.is_blackjack():
                        # Player loses bet
                        print(f"{player.name} loses. Dealer has blackjack.")
                    # Mark hand as completed
                    hand.is_complete = True

        # Determine if the round is over
        all_hands_complete = all(
            all(hand.is_complete for hand in player.hands) for player in self.players
        )
        if all_hands_complete:
            self.round_over = True



# Test for Game class
if __name__ == "__main__":
    from players import Player, Dealer
    from rules import Rules
    from strategy import BasicStrategy

    rules = Rules()
    strategy = BasicStrategy()
    player = Player(bankroll=1000, strategy=strategy, name="Alice")
    dealer = Dealer()
    game = Game(players=[player], dealer=dealer, rules=rules)

    # Simulate 5 rounds
    for _ in range(5):
        game.start_round()
