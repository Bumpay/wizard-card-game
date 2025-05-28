from typing import List, Type
import matplotlib.pyplot as plt
import numpy as np

from src.ai.debug_agent import WizardDebugPlayer
from src.ai.simple_agent import WizardSimpleBot
from src.ai.wizard_environment import WizardEnvironment
from src.ai.adrian_agent import WizardAdrianPlayerV01

import logging

def setup_logging():
    logging.getLogger('src.game.wizard_game').setLevel(logging.WARNING)
    logging.getLogger('src.core.round').setLevel(logging.WARNING)
    logging.getLogger('src.core.trick').setLevel(logging.WARNING)

def run_evaluation(player_classes: List[Type], num_games: int):
    env = WizardEnvironment()
    results = env.evaluate_players(
        player_classes=player_classes,
        num_games=num_games
    )
    env.print_results()

    plot_bet_accuracy(results, 'bet_accuracy.png')
    env.plot_betting_patterns('betting_patterns.png')
    env.plot_score_distributions('score_distributions.png')
    return results


def plot_bet_accuracy(stats: dict, save_path: str = None):
    """
    Create a line plot showing bet accuracy per round for each player type.

    Args:
        stats: Dictionary containing player statistics
        save_path: Optional path to save the plot (e.g., 'bet_accuracy.png')
    """
    plt.figure(figsize=(12, 6))

    for player_name, player_stats in stats.items():
        rounds = []
        accuracies = []

        for round_num in range(1, 21):
            placed_bets = player_stats['bets_placed'][round_num]
            if placed_bets > 0:
                accuracy = player_stats['right_bets'][round_num] / placed_bets
                rounds.append(round_num)
                accuracies.append(accuracy)

        plt.plot(rounds, accuracies, marker='o', label=player_name)

    plt.xlabel('Round Number')
    plt.ylabel('Bet Accuracy')
    plt.title('Betting Accuracy by Round')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # Set y-axis to percentage format
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

    if save_path:
        plt.savefig(save_path)
    plt.show()

def main():
    setup_logging()

    # Run the evaluation
    run_evaluation(
        player_classes=[WizardAdrianPlayerV01, WizardDebugPlayer, WizardSimpleBot],
        num_games=10000
    )

if __name__ == '__main__':
    main()