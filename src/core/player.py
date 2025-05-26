from src.game.game_state import GameState
from src.game.wizard_card import WizardCard, CardSuit


class WizardBasePlayer:
    def __init__(self, name: str):
        self.name: str = name

    def make_bid(self, state: GameState) -> int:
        raise NotImplementedError('This method should be implemented by subclasses.')

    def play_card(self, state: GameState) -> WizardCard:
        raise NotImplementedError('This method should be implemented by subclasses.')

    def pick_trump_suit(self, state: GameState) -> CardSuit:
        raise NotImplementedError('This method should be implemented by subclasses.')

    def __str__(self) -> str:
        return self.name

def rotate_players(players: list[WizardBasePlayer], start_player: WizardBasePlayer) -> list[WizardBasePlayer]:
    player_index = players.index(start_player)
    return players[player_index:] + players[:player_index]
