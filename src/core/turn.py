from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Sequence

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
        self._player = player
        self._hand = hand
        self._trick_cards = trick_cards
        self._trick_suit = trick_suit
        self._get_game_state = get_game_state
        self._played_card: WizardCard | None = None

    def play(self) -> WizardCard:
        playable_cards = valid_cards(self._hand, list(self._trick_cards.values()), self._trick_suit)
        game_state = self._get_game_state(self._player)

        try:
            chosen_card = self._player.play_card(game_state)
        except Exception as e:
            raise ValueError(f'Player {self._player.name} raised an exception: {e}')

        if not isinstance(chosen_card, WizardCard):
            raise ValueError(f'Player {self._player.name} returned invalid card type')

        if chosen_card not in playable_cards:
            raise ValueError(f'{self._player.name} played an invalid card')

        self._hand.remove(chosen_card)
        self._played_card = chosen_card

        if self._trick_suit is None and chosen_card.card_type == CardType.STANDARD:
            self._trick_suit = chosen_card.card_suit

        return chosen_card


def valid_cards(hand: Sequence[WizardCard], current_trick: list[WizardCard], trick_suit: CardSuit | None) -> list[WizardCard]:
    special_cards = [card for card in hand if card.card_type != CardType.STANDARD]

    # If no cards have been played yet in this trick, the player can play anything
    if not len(current_trick):
        return list(hand)
    else:
        # Cards that match the trick suit
        matching_suit = [card for card in hand if card.card_suit == trick_suit]

        return special_cards + matching_suit if matching_suit else hand
