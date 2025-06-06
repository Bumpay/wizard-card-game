import random

from src.core.player import WizardBasePlayer
from src.core.turn import valid_cards
from src.game.game_state import GameState
from src.game.wizard_card import CardSuit, WizardCard

class WizardDebugPlayer(WizardBasePlayer):
    def make_bid(self, state: GameState) -> int:
        return 0

    def play_card(self, state: GameState) -> "WizardCard":
        card = valid_cards(state.hand, state.current_trick.trick_cards, state.current_trick.trick_suit)[0]
        return card

    def pick_trump_suit(self, state: GameState) -> "CardSuit":
        suit = random.choice(list(CardSuit))
        return suit