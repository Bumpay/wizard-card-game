import logging
import random
from types import MappingProxyType

from src.core.deck import Deck
from src.core.player import WizardBasePlayer
from src.core.round import Round
from src.core.trick import Trick
from src.game.game_state import GameState
from src.game.wizard_card_factory import create_wizard_cards


class WizardGame:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._current_scores: dict[WizardBasePlayer, int] = dict()
        self._round_scores = {}
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
            self.logger.info(f"Player '{player.name}' added")

    def start_game(self):
        if not 3 <= len(self._players) <= 6:
            raise ValueError('Invalid number of players')

        random.shuffle(self._players)

        self._current_scores = {player: 0 for player in self._players}

        self._max_rounds = 60 // len(self._players)

        self.logger.info(f'\nStart game with {len(self._players)} players. Playing {self._max_rounds} rounds.')

        for round_number in range(self._max_rounds):
            self.logger.info(f'\nRound {round_number+1}')
            self._play_round(round_number+1)


        self.logger.info(f'\nGame finished')
        self.end_game()

    def _play_round(self, round_number: int):

        self._current_round = Round(
            round_number,
            self._players,
            self.get_game_state_for_player
        )

        self.logger.info(f'Round {round_number}: Start bidding')
        round_scores = self._current_round.play()
        self.logger.info(f'Round {round_number}: End bidding')

        self._round_scores[round_number] = round_scores

        self._current_scores = {
            player: self._current_scores.get(player, 0) + round_scores.get(player, 0)
            for player in set(self._current_scores) | set(round_scores)
        }

    def end_game(self):

        for player, score in sorted(self._current_scores.items(), key=lambda x: x[1], reverse=True):
            self.logger.info(f'{player}: {score}')

        max_score = max(self._current_scores.values())

        winners = [player.name for player, score in self._current_scores.items() if score == max_score]

        if len(winners) == 1:
            self.logger.info(f'\nWinner: {winners[0]} with score: {max_score}')
        else:
            self.logger.info(f'\nWinners: {", ".join(winners)} with score: {max_score}')

    def get_game_state_for_player(self, player: WizardBasePlayer):
        return GameState.from_game(self, player)

    @property
    def current_scores(self) -> MappingProxyType[WizardBasePlayer, int]:
        return MappingProxyType(self._current_scores)

    @property
    def current_round(self) -> Round:
        return self._current_round

    @property
    def players(self) -> tuple[WizardBasePlayer, ...]:
        return tuple(self._players)

    @property
    def round_scores(self):
        return self._round_scores
