from __future__ import annotations
from typing import Callable, TYPE_CHECKING

from src.core.turn import Turn
from src.game.wizard_card import WizardCard, CardSuit, CardType

if TYPE_CHECKING:
    from src.core.player import WizardBasePlayer
    from src.game.game_state import GameState


class Trick:
    def __init__(
            self,
            players: list[WizardBasePlayer],
            hands: dict[WizardBasePlayer, list[WizardCard]],
            trump_suit: CardSuit,
            get_game_state: Callable[[WizardBasePlayer], GameState],
    ):
        self._players = players
        self._hands = hands
        self._trump_suit = trump_suit
        self._get_game_state = get_game_state

        self._trick_cards: dict[WizardBasePlayer, WizardCard] = {}
        self._trick_suit: CardSuit | None = None

    def play(self) -> WizardBasePlayer:

        for player in self._players:
            turn = Turn(
                player,
                self._hands[player],
                self._trick_cards,
                self._trick_suit,
                self._get_game_state,
            )
            card = turn.play()
            self._trick_cards[player] = card
            if not self._trick_suit and card.card_type == CardType.STANDARD:
                self._trick_suit = card.card_suit
            print(f'{player.name}: I play a {card}')

        winner = self.determine_winner()
        print(f'\nTrick winner: {winner}')
        return winner

    def determine_winner(self) -> WizardBasePlayer:
        trick_suite = None
        for player, card in self._trick_cards.items():

            # First wizard card wins the round
            if card.card_type == CardType.WIZARD:
                return player

            # First standard card determines trick suite
            if not trick_suite and card.card_type == CardType.STANDARD:
                trick_suite = card.card_suit

        # If all played jester cards
        if all(card.card_type == CardType.JESTER for card in self._trick_cards.values()):
            return list(self._trick_cards.keys())[0]

        # If trump suited card is in play
        elif self._trump_suit and any(card.card_suit == self._trump_suit for card in self._trick_cards.values()):
            return max(
                ((player, card) for player, card in self._trick_cards.items()
                 if card.card_suit == self._trump_suit),
                key=lambda x: x[1].card_value
            )[0]

        # If no trump suited card is in play
        else:
            return max(
                ((player, card) for player, card in self._trick_cards.items()
                 if trick_suite and card.card_suit == trick_suite),
                key=lambda x: x[1].card_value
            )[0]

    @property
    def trick_suit(self):
        return self._trick_suit

    @property
    def trick_cards(self):
        return self._trick_cards