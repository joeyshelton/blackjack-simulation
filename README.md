# Blackjack Simulation Library

Welcome to the **Blackjack Simulation Library**, a versatile Python library designed to simulate the game of Blackjack with various rule variations. This library is suitable for building command-line games, UI applications, strategy simulations, and Monte Carlo analyses.

---

## **Table of Contents**

- [Features](#features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Library Structure](#library-structure)
- [Usage Examples](#usage-examples)
  - [1. Command-Line Blackjack Game](#1-command-line-blackjack-game)
  - [2. UI Blackjack Game](#2-ui-blackjack-game)
  - [3. Strategy Simulation](#3-strategy-simulation)
  - [4. Monte Carlo Simulation](#4-monte-carlo-simulation)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

---

## **Features**

- **Comprehensive Rule Variations**: Customize Blackjack rules, including deck numbers, payout ratios, dealer actions, splitting rules, doubling down, surrender options, and more.
- **Modular Design**: Clean and organized code structure with classes for cards, hands, players, dealers, strategies, rules, and the game itself.
- **Strategy Implementation**: Easily implement different player strategies, including basic strategy, custom strategies, or user input.
- **Simulation Capabilities**: Run simulations to analyze strategies, calculate odds, or test different rule sets.
- **Extensibility**: Designed to be extended for additional features, such as side bets, insurance, or card counting.

---

## **Installation**

### **Prerequisites**

- Python 3.6 or higher

### **Clone the Repository**

```bash
git clone https://github.com/yourusername/blackjack-simulation-library.git
cd blackjack-simulation-library
```

### **Install Dependencies**

Currently, the library does not have external dependencies beyond the Python Standard Library. If future dependencies are added, install them using:

```bash
pip install -r requirements.txt
```

---

## **Getting Started**

To get started with the Blackjack Simulation Library, you can explore the provided examples or start building your own applications using the library's modules.

---

## **Library Structure**

The library is organized into the following modules:

- **`cards.py`**: Contains `Card`, `Deck`, and `Shoe` classes.
- **`hand.py`**: Contains the `Hand` class.
- **`players.py`**: Contains `Player` and `Dealer` classes.
- **`strategy.py`**: Contains the `Strategy` base class and strategy implementations.
- **`rules.py`**: Contains the `Rules` class to define game rules.
- **`game.py`**: Contains the `Game` class to manage game flow.
- **`main.py`**: Example script for a command-line Blackjack game.

---

## **Usage Examples**

### **1. Command-Line Blackjack Game**

**Description**: Run a simple command-line Blackjack game where you play against the dealer.

**Setup**:

- The `main.py` script demonstrates how to create a human player and start the game.

**Usage**:

```bash
python3 main.py
```

**Example Code** (`main.py`):

```python
# main.py

from game import Game
from players import Dealer
from rules import Rules
from strategy import Strategy

class HumanStrategy(Strategy):
    def decide_action(self, hand, dealer_up_card, rules):
        while True:
            print(f"\nYour hand: {[str(card) for card in hand.cards]}")
            print(f"Dealer's up card: {dealer_up_card}")
            print(f"Hand value(s): {sorted(hand.get_values())}")

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

        if player.bankroll < game.table_limits[0]:
            print("You don't have enough bankroll to continue.")
            break
        cont = input("Do you want to play another round? (y/n): ").lower()
        if cont != 'y':
            break

if __name__ == "__main__":
    main()
```

**Instructions**:

- Run `python3 main.py` to start the game.
- Follow the on-screen prompts to play.

---

### **2. UI Blackjack Game**

**Description**: Develop a graphical user interface (GUI) for the Blackjack game using frameworks like Tkinter, PyQt, or Pygame.

**Setup**:

- Choose a GUI framework and install any required packages.
- Create a new script (e.g., `game_ui.py`) and use the library's classes to build the game logic.
- Replace user inputs and outputs with GUI elements (buttons, labels, etc.).

**Example**:

Due to the variety of GUI frameworks, here's a high-level example using Tkinter:

```python
# game_ui.py

import tkinter as tk
from game import Game
from players import Dealer
from rules import Rules
from strategy import Strategy

class GUIPlayer(Player):
    # Implement methods to interact with GUI components
    pass

def main():
    root = tk.Tk()
    # Build GUI components
    # Set up the game using Game, GUIPlayer, and Dealer classes
    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
```

**Instructions**:

- Build the GUI components to display cards, handle user actions, and show game status.
- Use event handlers to connect GUI actions to game logic.

---

### **3. Strategy Simulation**

**Description**: Simulate Blackjack games using predefined strategies to analyze performance over many rounds.

**Setup**:

- Create a script (e.g., `simulation.py`) to run simulations.
- Use the `BasicStrategy` class or implement custom strategies.

**Example Code** (`simulation.py`):

```python
# simulation.py

from game import Game
from players import Dealer, Player
from rules import Rules
from strategy import BasicStrategy

def main():
    rules = Rules()
    strategy = BasicStrategy()
    player = Player(bankroll=10000, strategy=strategy, name="SimPlayer")
    dealer = Dealer()
    game = Game(players=[player], dealer=dealer, rules=rules)

    num_rounds = 10000
    for _ in range(num_rounds):
        game.start_round()
        # Optionally collect data for analysis

    print(f"Final bankroll after {num_rounds} rounds: {player.bankroll}")

if __name__ == "__main__":
    main()
```

**Instructions**:

- Run `python3 simulation.py` to start the simulation.
- Modify the strategy or rules to test different scenarios.
- Collect and analyze data to evaluate strategy performance.

---

### **4. Monte Carlo Simulation**

**Description**: Perform extensive simulations to compute odds, expected returns, or optimal strategies using Monte Carlo methods.

**Setup**:

- Create a script (e.g., `monte_carlo.py`) to run simulations with varying parameters.
- Utilize multiprocessing or threading for performance optimization if necessary.

**Example Code** (`monte_carlo.py`):

```python
# monte_carlo.py

import multiprocessing
from game import Game
from players import Dealer, Player
from rules import Rules
from strategy import BasicStrategy

def run_simulation(sim_id, num_rounds, results_queue):
    rules = Rules()
    strategy = BasicStrategy()
    player = Player(bankroll=10000, strategy=strategy, name=f"SimPlayer_{sim_id}")
    dealer = Dealer()
    game = Game(players=[player], dealer=dealer, rules=rules)

    for _ in range(num_rounds):
        game.start_round()
    results_queue.put(player.bankroll)

def main():
    num_simulations = 10
    num_rounds_per_sim = 100000
    processes = []
    results_queue = multiprocessing.Queue()

    for sim_id in range(num_simulations):
        p = multiprocessing.Process(target=run_simulation, args=(sim_id, num_rounds_per_sim, results_queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    results = [results_queue.get() for _ in processes]
    average_bankroll = sum(results) / num_simulations
    print(f"Average bankroll after simulations: {average_bankroll}")

if __name__ == "__main__":
    main()
```

**Instructions**:

- Run `python3 monte_carlo.py` to start the Monte Carlo simulation.
- Adjust `num_simulations` and `num_rounds_per_sim` for desired accuracy and performance.
- Analyze results to draw conclusions about strategy effectiveness.

---

## **Customization**

The library is designed to be customizable to suit different needs.

### **Custom Rules**

Modify game rules using the `Rules` class:

```python
rules = Rules(
    blackjack_payout=1.5,
    number_of_decks=6,
    dealer_hits_soft_17=False,
    double_down_allowed_on=[9, 10, 11],
    double_after_split_allowed=True,
    splitting_rules={
        'max_splits': 3,
        'can_split_aces': True,
        'resplit_aces_allowed': False,
        'can_split_unlike_tens': False,
    },
    surrender_allowed='late',
    insurance_offered=True,
    insurance_payout=2.0
)
```

### **Custom Strategies**

Implement your own strategies by subclassing the `Strategy` base class:

```python
from strategy import Strategy

class MyCustomStrategy(Strategy):
    def decide_action(self, hand, dealer_up_card, rules):
        # Implement custom decision logic
        pass
```

Use your strategy in the game:

```python
player = Player(bankroll=1000, strategy=MyCustomStrategy(), name="CustomPlayer")
```

### **Extending Functionality**

Add new features such as:

- **Side Bets**: Create classes to handle side bets and integrate them into the game flow.
- **Card Counting**: Implement card counting strategies by tracking the cards dealt from the shoe.
- **Advanced Analytics**: Collect detailed game data for statistical analysis or machine learning applications.

---

## **Contributing**

Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

1. **Fork the repository** on GitHub.
2. **Create a new branch** for your feature or bug fix.
3. **Commit your changes** with clear and descriptive messages.
4. **Submit a pull request** explaining your changes and their purpose.

---

## **License**

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

---

Feel free to explore, customize, and extend the Blackjack Simulation Library to suit your needs. Happy coding and good luck at the tables!