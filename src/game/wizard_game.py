import random

from src.core.deck import Deck
from src.core.player import WizardBasePlayer
from src.core.round import Round
from src.core.trick import Trick
from src.game.game_state import GameState
from src.game.wizard_card_factory import create_wizard_cards


class WizardGame:
    def __init__(self):
        self._current_scores: dict[WizardBasePlayer, int] = dict()
        self._deck: Deck = Deck(create_wizard_cards())
        self._players: list[WizardBasePlayer] = list()
        self._current_round: Round | None = None
        self._current_trick: Trick | None = None
        self._max_rounds: int = 0

    def add_player(self, player: WizardBasePlayer):
        if len(self._players) >= 6:
            raise Exception('Too many players')
        else:
            self._players.append(player)
            print(f"Player '{player.name}' added")

    def start_game(self):
        if not 3 <= len(self._players) <= 6:
            raise ValueError('Invalid number of players')

        random.shuffle(self._players)

        self._current_scores = {player: 0 for player in self._players}

        self._max_rounds = 60 // len(self._players)

        print(f'\nStart game with {len(self._players)} players. Playing {self._max_rounds} rounds.')

        for round_number in range(self._max_rounds):
            print(f'\nRound {round_number+1}')
            self._play_round(round_number+1)


        print(f'\nGame finished')
        self.end_game()

    def _play_round(self, round_number: int):

        self._current_round = Round(
            round_number,
            self._players,
            self.get_game_state_for_player
        )

        print(f'Round {round_number}: Start bidding')
        round_scores = self._current_round.play()
        print(f'Round {round_number}: End bidding')

        self._current_scores = {
            player: self._current_scores.get(player, 0) + round_scores.get(player, 0)
            for player in set(self._current_scores) | set(round_scores)
        }

    def end_game(self):

        for player, score in sorted(self._current_scores.items(), key=lambda x: x[1], reverse=True):
            print(f'{player}: {score}')

        max_score = max(self._current_scores.values())

        winners = [player.name for player, score in self._current_scores.items() if score == max_score]

        if len(winners) == 1:
            print(f'\nWinner: {winners[0]} with score: {max_score}')
        else:
            print(f'\nWinners: {", ".join(winners)} with score: {max_score}')

    def get_game_state_for_player(self, player: WizardBasePlayer):
        return GameState.from_game(self, player)

    @property
    def current_scores(self):
        return self._current_scores

    @property
    def current_round(self) -> Round:
        return self._current_round

    @property
    def players(self):
        return self._players
