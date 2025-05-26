import random

from typing import Self
from core.player import WizardBasePlayer
from game.wizard_card import WizardCard

class Deck:
    def __init__(self, cards: list[WizardCard]):
        self._cards: list[WizardCard] = cards.copy()
        self.shuffle()

    def shuffle(self) -> Self:
        random.shuffle(self._cards)
        return self

    def draw(self, count: int = 1) -> list[WizardCard]:
        if len(self._cards) < count:
            raise ValueError(f'Not enough cards to draw {count}.')
        drawn = self._cards[:count]
        self._cards = self._cards[count:]
        return drawn

    def draw_one(self) -> WizardCard:
        return self.draw(1)[0]

    def deal(self, players: list[WizardBasePlayer], cards_per_player: int) -> dict[WizardBasePlayer, list[WizardCard]]:
        return {
            player: self.draw(cards_per_player)
            for player in players
        }

    def remaining(self) -> int:
        return len(self._cards)
