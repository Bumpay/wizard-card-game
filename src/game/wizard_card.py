from dataclasses import dataclass
from enum import Enum

from src.core.card import Card


class CardSuit(Enum):
    HEARTS = 'hearts'
    SPADES = 'spades'
    CLUBS = 'clubs'
    DIAMONDS = 'diamonds'

    def __str__(self):
        display_names = {
            CardSuit.HEARTS: '♥',
            CardSuit.SPADES: '♠',
            CardSuit.CLUBS: '♣',
            CardSuit.DIAMONDS: '♦'
        }
        return display_names[self]


class CardType(Enum):
    STANDARD = 'standard'
    JESTER = 'jester'
    WIZARD = 'wizard'

    def __str__(self):
        display_names = {
            CardType.STANDARD: 'Standard',
            CardType.JESTER: 'Jester',
            CardType.WIZARD: 'Wizard'
        }
        return display_names[self]


@dataclass(frozen=True)
class WizardCard(Card):
    card_type: CardType
    card_suit: CardSuit | None = None
    card_value: int | None = None

    def __post_init__(self):
        if self.card_type == CardType.STANDARD:
            if self.card_suit is None or self.card_value is None:
                raise ValueError('CardType.STANDARD requires card_suit and card_value')
        else:
            if self.card_suit is not None or self.card_value is not None:
                raise ValueError('Special cards must not have suit or value')

    def __str__(self):
        if self.card_type == CardType.STANDARD:
            return f'{self.card_suit} {self.card_value}'
        elif self.card_type == CardType.WIZARD:
            return 'Wizard'
        elif self.card_type == CardType.JESTER:
            return 'Jester'
        return 'Unknown Card'
