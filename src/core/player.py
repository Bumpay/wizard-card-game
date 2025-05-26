import signal
from functools import wraps

from src.game.game_state import GameState
from src.game.wizard_card import WizardCard, CardSuit

def timeout(seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def handler(signum, frame):
                raise TimeoutError(f'Function {func.__name__} timed out after {seconds} seconds')

            # Set the signal handler and a 5-second alarm
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)

            return result
        return wrapper
    return decorator


class WizardBasePlayer:
    def __init__(self, name: str):
        self.name: str = name

    @timeout(1)
    def make_bid(self, state: GameState) -> int:
        raise NotImplementedError('This method should be implemented by subclasses.')

    @timeout(1)
    def play_card(self, state: GameState) -> WizardCard:
        raise NotImplementedError('This method should be implemented by subclasses.')

    def pick_trump_suit(self, state: GameState) -> CardSuit:
        raise NotImplementedError('This method should be implemented by subclasses.')

    def __str__(self) -> str:
        return self.name

def rotate_players(players: list[WizardBasePlayer], start_player: WizardBasePlayer) -> list[WizardBasePlayer]:
    player_index = players.index(start_player)
    return players[player_index:] + players[:player_index]
