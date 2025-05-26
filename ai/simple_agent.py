import random
from collections import Counter

from game.wizard_card import CardSuit, CardType, WizardCard
from core.player import WizardBasePlayer


class WizardSimpleBot(WizardBasePlayer):
    def make_bid(self, state) -> int:
        bid = 0
        hand = state.hand

        bid += len([c for c in hand if c.card_type == CardType.WIZARD])
        bid += len([c for c in hand if c.card_suit == state._trump_suit])

        return min(bid, state.current_round_number)

    def play_card(self, state) -> WizardCard:
        trick = state.current_trick
        trick_goal = state._current_bets[self]
        tricks_won = state._won_tricks[self]
        hand = state.hand
        trump_suite = state._trump_suit

        if len(trick) == 0 and tricks_won < trick_goal:
            # Trick Winning strategy
            return self._pick_winning_card(hand, trump_suite)

        return hand[0]

    def pick_trump_suit(self, state) -> CardSuit:
        hand = state.hand

        most_suits = Counter(card.card_suit for card in hand).most_common(1)
        return most_suits[0][0] if most_suits else random.choice(list(CardSuit))

    def _pick_winning_card(self, hand, trump_suit):
        wizard_card = next((card for card in hand if card.card_type == CardType.WIZARD), None)
        highest_trump_card = max([card for card in hand if trump_suit and card.card_suit == trump_suit], key=lambda c: c.card_value, default=None)
        highest_non_trump_card = max([card for card in hand if card.card_type == CardType.STANDARD and card.card_suit != trump_suit], key=lambda c: c.card_value, default=None)

        if wizard_card:
            return wizard_card
        elif highest_trump_card:
            return highest_trump_card
        elif highest_non_trump_card:
            return highest_non_trump_card
        else:
            return hand[0]

