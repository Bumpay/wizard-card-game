from core.player import WizardBasePlayer
from core.deck import Deck
from core.trick import Trick
from game.wizard_card import WizardCard
from game.wizard_card_factory import create_wizard_cards


class Round:

    def __init__(
            self,
            round_number: int,
            players: list[WizardBasePlayer],
            game_state_callback
    ):
        self._players: list[WizardBasePlayer] = players
        self._round_number: int = round_number
        self._game_state_callback = game_state_callback

        self._current_trick: Trick | None = None
        self._deck: Deck = Deck(create_wizard_cards()).shuffle()
        self._hands: dict[WizardBasePlayer, list[WizardCard]] = self._deck.deal(self._players, self._round_number)
        self._trump_card: WizardCard | None = self._deck.draw_one() if self._deck.remaining() > 0 else None
        self._current_bets: dict[WizardBasePlayer, int] = {}
        self._won_tricks: dict[WizardBasePlayer, int] = {player: 0 for player in players}
        self._trick_starting_player: WizardBasePlayer = self._players[0]

    def play(self) -> dict[WizardBasePlayer, int]:

        print(f'\nTrump suit: {self.trump_suit}')
        self.run_bidding_phase()

        for i in range(self._round_number):
            print(f'\nTrick {i + 1} of {self._round_number}')
            winner = self.play_trick()

            self._won_tricks[winner] += 1
            self._trick_starting_player = winner

        round_scores = self.calculate_scores()

        return round_scores


    def run_bidding_phase(self):
        for player in self._players:
            decision = player.make_bid(self._game_state_callback(player))
            print(f'{player.name}: I bet {decision}')
            self._current_bets[player] = decision

    def play_trick(self) -> WizardBasePlayer:
        self._current_trick = Trick(
            self._players.copy(),
            self._hands,
            self.trump_suit,
            self._game_state_callback
        )
        winner = self.current_trick.play()

        return winner

    def calculate_scores(self) -> dict[WizardBasePlayer, int]:
        scores: dict[WizardBasePlayer, int] = {player: 0 for player in self._players}
        for player in self._players:
            scores[player] += (20 + self._current_bets[player] * 10) \
                if self._current_bets[player] == self._won_tricks[player] \
                else -10 * (abs(self._current_bets[player] - self._won_tricks[player]))

        return scores

    @property
    def current_bets(self):
        return self._current_bets

    @property
    def won_tricks(self):
        return self._won_tricks

    @property
    def hands(self):
        return self._hands

    @property
    def trump_suit(self):
        return self._trump_card.card_suit if self._trump_card else None

    @property
    def current_trick(self):
        return self._current_trick

    @property
    def round_number(self):
        return self._round_number