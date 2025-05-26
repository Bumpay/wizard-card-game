import random
from collections import Counter

from src.core.turn import valid_cards
from src.game.game_state import GameState
from src.game.wizard_card import CardSuit, CardType, WizardCard
from src.core.player import WizardBasePlayer


class WizardAdrianPlayerV01(WizardBasePlayer):
    def make_bid(self, state) -> int:
        bid = 0
        hand = state.hand

        if state.current_round_number == 1 and self.expected_value(state) > 0:
            return 1


        bid += len([c for c in hand if c.card_type == CardType.WIZARD])
        bid += len([c for c in hand if state.trump_suit and c.card_suit == state.trump_suit])

        if state.current_round_number == 20:
            bid += len([c for c in hand if c.card_value and c.card_value >= 10])

        return min(bid, state.current_round_number)

    def play_card(self, state: GameState) -> WizardCard:
        trick = state.current_trick
        trick_goal = state.current_bets[self]
        tricks_won = state.won_tricks[self]
        hand = state.hand
        trump_suite = state.trump_suit

        if len(trick.trick_cards) == 0 and tricks_won < trick_goal:
            # Trick Winning strategy
            return self._pick_winning_card(hand, trump_suite)

        return valid_cards(list(hand), state.current_trick.trick_cards, state.current_trick.trick_suit)[0]

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

    def expected_value(self, state):
        card = state.hand[0]
        remaining_cards = 60 - 2
        players = len(state.players)
        prob_win = 1.0
        win_points = 30
        lose_points = -10

        if card.card_type == CardType.WIZARD:
            winning_cards = state.players.index(self) - 1  # Only previous player can win with a Wizard
        elif card.card_type == CardType.JESTER:
            # winning_cards = 56                          # Every card beats Jester except Jester
            return -1  # Chance too low
        elif card.card_suit == state.trump_suit:
            winning_cards = 4 + 13 - card.card_value    # Wizard and higher trump cards are better
        else:
            winning_cards = (4 + 13 - 1) # Wizards and Trump Cards - 1 that's been flipped
            if state.players.index(self) == 0:
                winning_cards += 13 - card.card_value
            else:
                return -1  # Chance too low

        safe_cards = remaining_cards - winning_cards

        for i in range(players-1):
            prob_win *= (safe_cards - i) / (remaining_cards - i)

        prob_lose = 1 - prob_win
        expected = prob_win * win_points + prob_lose * lose_points

        return expected

