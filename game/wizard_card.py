from enum import Enum

from core.card import Card


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


class WizardCard(Card):
    def __init__(self, card_type: CardType, card_suit: CardSuit|None=None, card_value:int|None=None):
        self.card_type: CardType = card_type
        self.card_suit: CardSuit | None = card_suit
        self.card_value: int | None = card_value

    def __str__(self):
        if self.card_type == CardType.STANDARD:
            return f'{self.card_suit} {self.card_value}'
        elif self.card_type == CardType.WIZARD:
            return 'Wizard'
        elif self.card_type == CardType.JESTER:
            return 'Jester'
        return 'Unknown Card'
