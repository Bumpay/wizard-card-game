from typing import List, Type

from src.ai.debug_agent import WizardDebugPlayer
from src.ai.simple_agent import WizardSimpleBot
from src.ai.wizard_environment import WizardEnvironment
from src.ai.adrian_agent import WizardAdrianPlayerV01
import logging

def setup_logging():
    logging.getLogger('src.game.wizard_game').setLevel(logging.WARNING)
    logging.getLogger('src.core.round').setLevel(logging.WARNING)
    logging.getLogger('src.core.trick').setLevel(logging.WARNING)

def run_evaluation(player_classes: List[Type], num_games: int, players_per_game: int):
    env = WizardEnvironment()
    results = env.evaluate_players(
        player_classes=player_classes,
        num_games=num_games,
        players_per_game=players_per_game
    )
    env.print_results()
    return results

def main():
    setup_logging()
    
    # Run the evaluation
    results = run_evaluation(
        player_classes=[WizardSimpleBot, WizardDebugPlayer, WizardAdrianPlayerV01],
        num_games=1000,
        players_per_game=6
    )

if __name__ == '__main__':
    main()