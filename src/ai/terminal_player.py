from src.ai.human_player import HumanPlayer
from src.game.game_state import GameState
from src.game.wizard_card import WizardCard, CardSuit


class ConsoleHumanPlayer(HumanPlayer):

    def display_game_state(self, game_state: GameState) -> None:
        """Display comprehensive game state information"""
        print("\n" + "=" * 50)
        print("GAME STATE")
        print("=" * 50)

        # Round information
        print(f"Round: {game_state.current_round_number}")
        print(f"Starting player: {game_state.players[0].name}")

        # Trump suit
        if game_state.trump_card:
            print(f"Trump Card: {game_state.trump_card}")
        if game_state.trump_suit:
            print(f"Trump Suit: {game_state.trump_suit}")

        # Score information
        print("\nSCORES:")
        for player, score in game_state.current_scores.items():
            print(f"{player.name}: {score}")

        # Betting information
        print("\nBETS:")
        for player, bet in game_state.current_bets.items():
            tricks_won = game_state.won_tricks.get(player, 0)
            print(f"{player.name}: Bet {bet}, Won {tricks_won}")

        # Current trick
        if game_state.current_trick:
            print("\nCURRENT TRICK:")
            for player, card in game_state.current_trick.trick_cards.items():
                print(f"{player.name}: {card}")

        # Player's hand
        print("\nYOUR HAND:")
        for i, card in enumerate(game_state.hand):
            print(f"{i}: {card}")

        print("=" * 50)

    def display_hand(self, game_state) -> None:
        # You can remove this method since display_game_state now shows all necessary information
        self.display_game_state(game_state)


    def get_bid_from_player(self, valid_bets: list[int]) -> int:
        print("\nValid bets:", valid_bets)
        while True:
            try:
                bid = int(input(f"Enter your bid: "))
                if bid in valid_bets:
                    return bid
                print("Invalid bid value")
            except ValueError:
                print("Please enter a number")

    def get_card_from_player(self, valid_cards: list[WizardCard]) -> WizardCard:
        print("\nValid cards to play:")
        for i, card in enumerate(valid_cards):
            print(f"{i}: {card}")

        while True:
            try:
                choice = int(input("Choose a card (number): "))
                if 0 <= choice < len(valid_cards):
                    return valid_cards[choice]
                print("Invalid card number")
            except ValueError:
                print("Please enter a number")

    def get_trump_suit_from_player(self) -> CardSuit:
        print("\nChoose a trump suit:")
        for i, suit in enumerate(CardSuit):
            print(f"{i}: {suit}")

        while True:
            try:
                choice = int(input("Enter the number of your chosen suit: "))
                if 0 <= choice < len(CardSuit):
                    return CardSuit(choice)
                print("Invalid choice. Please choose a number from the list.")
            except ValueError:
                print("Please enter a number.")

    def display_new_hand(self, hand: list[WizardCard]) -> None:
        print("\nYour new hand:")
        for card in hand:
            print(f"  {card}")