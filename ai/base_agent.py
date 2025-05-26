import random

from core.player import WizardBasePlayer
from core.turn import valid_cards
from game.wizard_card import CardSuit, WizardCard

class WizardDebugPlayer(WizardBasePlayer):
    def make_bid(self, state) -> int:
        return 0

    def play_card(self, state) -> "WizardCard":
        card = valid_cards(state.hand, state.current_trick.trick_cards, state.current_trick.trick_suit)[0]
        return card

    def pick_trump_suit(self, state) -> "CardSuit":
        suit = random.choice(list(CardSuit))
        return suit