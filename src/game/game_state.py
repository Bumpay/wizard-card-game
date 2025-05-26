from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Mapping

from src.core.trick import Trick
from .wizard_card import WizardCard, CardSuit

if TYPE_CHECKING:
    from src.game.wizard_game import WizardGame
    from src.core.player import WizardBasePlayer


@dataclass(frozen=True)
class GameState:
    players: tuple[WizardBasePlayer]
    current_round_number: int
    current_scores: Mapping[WizardBasePlayer, int]
    current_bets: Mapping[WizardBasePlayer, int]
    trump_suit: CardSuit
    current_trick: Trick
    won_tricks: Mapping[WizardBasePlayer, int]
    hand: tuple[WizardCard]

    @classmethod
    def from_game(cls, game: WizardGame, player: WizardBasePlayer) -> GameState:
        return cls(
            players=game.players,
            current_round_number=game.current_round.round_number,
            current_scores=game.current_scores,
            current_bets=game.current_round.current_bets,
            trump_suit=game.current_round.trump_suit,
            current_trick=game.current_round.current_trick,
            won_tricks=game.current_round.won_tricks,
            hand=game.current_round.hands[player]
        )