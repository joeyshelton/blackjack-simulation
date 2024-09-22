# main.py

from game import Game
from players import Player, Dealer
from rules import Rules
from hand import Hand
from cards import Card
from strategy import Strategy

class HumanStrategy(Strategy):
    """
    Strategy that prompts the user for decisions.
    """

    def decide_action(self, hand, dealer_up_card, rules):
        while True:
            # Display hand and dealer's up card
            print(f"\nYour hand: {[str(card) for card in hand.cards]}")
            print(f"Dealer's up card: {dealer_up_card}")
            print(f"Hand value(s): {sorted(hand.get_values())}")

            # Get possible actions
            actions = ['hit', 'stand']
            if hand.can_split(rules) and len(hand.cards) == 2:
                actions.append('split')
            if hand.can_double_down(rules) and len(hand.cards) == 2:
                actions.append('double')
            if rules.surrender_allowed != 'none' and len(hand.cards) == 2:
                actions.append('surrender')

            action = input(f"Choose an action ({'/'.join(actions)}): ").lower()
            if action in actions:
                return action
            else:
                print("Invalid action. Please try again.")

class HumanPlayer(Player):
    def __init__(self, bankroll=1000, name="You"):
        super().__init__(bankroll=bankroll, strategy=HumanStrategy(), name=name)

def main():
    rules = Rules()
    player = HumanPlayer(bankroll=1000)
    dealer = Dealer()
    game = Game(players=[player], dealer=dealer, rules=rules)

    while True:
        game.start_round()
        print(f"\n{player.name}'s bankroll: {player.bankroll}")

        # Check if player wants to continue
        if player.bankroll < game.table_limits[0]:
            print("You don't have enough bankroll to continue.")
            break
        cont = input("Do you want to play another round? (y/n): ").lower()
        if cont != 'y':
            break

if __name__ == "__main__":
    main()
