from abc import abstractmethod, ABC

from src.core.player import WizardBasePlayer
from src.core.turn import valid_cards
from src.game.game_state import GameState
from src.game.wizard_card import WizardCard, CardSuit


class HumanPlayer(WizardBasePlayer, ABC):


    def __init__(self, name: str):
        super().__init__(name)
        self._hand: list[WizardCard] = []

    def make_bid(self, game_state: GameState) -> int:
        self.display_game_state(game_state)
        valid_bets = list(range(0, game_state.current_round_number+1))
        return self.get_bid_from_player(valid_bets)

    def play_card(self, game_state: GameState) -> WizardCard:
        self.display_game_state(game_state)
        valids = valid_cards(game_state.hand, game_state.current_trick.trick_cards, game_state.current_trick.trick_suit)
        return self.get_card_from_player(valids)

    def pick_trump_suit(self) -> CardSuit:
        return self.get_trump_suit_from_player()

    def receive_hand(self, cards: list[WizardCard]) -> None:
        self._hand = cards.copy()
        self.display_new_hand(self._hand)

    @abstractmethod
    def display_game_state(self, game_state: GameState) -> None:
        """Display the current game state to the player"""
        pass

    @abstractmethod
    def get_bid_from_player(self, valid_bets: list[int]) -> int:
        """Get bid decision from the player"""
        pass

    @abstractmethod
    def get_card_from_player(self, valid_cards: list[WizardCard]) -> WizardCard:
        """Get card play decision from the player"""
        pass

    @abstractmethod
    def get_trump_suit_from_player(self) -> CardSuit:
        """Get trump suit choice from the player when a Wizard card is shown"""
        pass

    @abstractmethod
    def display_new_hand(self, hand: list[WizardCard]) -> None:
        """Display the new hand of cards to the player"""
        pass