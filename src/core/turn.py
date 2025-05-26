from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable

from src.game.wizard_card import CardSuit, WizardCard, CardType

if TYPE_CHECKING:
    from src.core.player import WizardBasePlayer
    from src.game.game_state import GameState


class Turn:
    def __init__(self,
                 player: WizardBasePlayer,
                 hand: list[WizardCard],
                 trick_cards: dict[WizardBasePlayer, WizardCard],
                 trick_suit: CardSuit | None,
                 get_game_state: Callable[[WizardBasePlayer], GameState],
    ):
        self.player = player
        self.hand = hand
        self.trick_cards = trick_cards
        self.trick_suit = trick_suit
        self.get_game_state = get_game_state
        self.played_card: WizardCard | None = None

    def play(self) -> WizardCard:
        playable_cards = valid_cards(self.hand, self.trick_cards, self.trick_suit)
        game_state = self.get_game_state(self.player)

        chosen_card = self.player.play_card(game_state)
        assert chosen_card in playable_cards, f'{self.player.name} played an invalid card'

        self.hand.remove(chosen_card)
        self.trick_cards[self.player] = chosen_card
        self.played_card = chosen_card

        if self.trick_suit is None and chosen_card.card_type == CardType.STANDARD:
            self.trick_suit = chosen_card.card_suit

        return chosen_card


def valid_cards(hand: list[WizardCard], current_trick: list[WizardCard], trick_suit: CardSuit) -> list[WizardCard]:
    special_cards = [card for card in hand if card.card_type != CardType.STANDARD]

    # If no cards have been played yet in this trick, player can play anything
    if not len(current_trick):
        return hand
    else:
        # Cards that match the trick suit
        matching_suit = [card for card in hand if card.card_suit == trick_suit]

        return special_cards + matching_suit if matching_suit else hand
