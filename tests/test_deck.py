import pytest

from core.deck import Deck
from core.player import WizardBasePlayer
from game.wizard_card import WizardCard, CardType, CardSuit


class DummyPlayer(WizardBasePlayer):
    def __init__(self, name: str):
        super().__init__(name)


def generate_test_cards(n):
    return [WizardCard(CardType.STANDARD, CardSuit.HEARTS, i) for i in range(n)]


def test_deck_initialization_and_shuffle():
    cards = generate_test_cards(10)
    deck = Deck(cards)

    assert deck.remaining() == 10
    assert cards != deck._cards  # shuffled, likely different order
    assert set(cards) == set(deck._cards)  # same content


def test_draw_cards_reduces_deck():
    deck = Deck(generate_test_cards(10))
    drawn = deck.draw(3)

    assert len(drawn) == 3
    assert deck.remaining() == 7


def test_draw_one_card():
    deck = Deck(generate_test_cards(5))
    card = deck.draw_one()

    assert isinstance(card, WizardCard)
    assert deck.remaining() == 4


def test_draw_too_many_raises():
    deck = Deck(generate_test_cards(2))
    with pytest.raises(ValueError):
        deck.draw(3)


def test_deal_cards_to_players():
    players = [DummyPlayer('P1'), DummyPlayer('P2')]
    deck = Deck(generate_test_cards(10))
    hands = deck.deal(players, 3)

    assert set(hands.keys()) == set(players)
    for hand in hands.values():
        assert len(hand) == 3

    total_dealt = sum(len(hand) for hand in hands.values())
    assert total_dealt == 6
    assert deck.remaining() == 4


def test_remaining_count():
    deck = Deck(generate_test_cards(5))
    assert deck.remaining() == 5
    deck.draw(2)
    assert deck.remaining() == 3