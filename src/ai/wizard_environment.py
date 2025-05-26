from typing import Type

import numpy as np

from src.core.player import WizardBasePlayer
from src.game.wizard_game import WizardGame


class WizardEnvironment:
    def __init__(self):
        self.stats: dict[str, dict] = {}

    def evaluate_players(
            self,
            player_classes: list[Type[WizardBasePlayer]],
            num_games: int = 100
    ) -> dict[str, dict]:
        """
        Evaluate multiple AI players over several games.

        :param player_classes: List of WizardBasePlayer classes to evaluate
        :param num_games: Number of games to play
        :param players_per_game: Number of players in each game
        """
        if not 3 <= len(player_classes) <= 6:
            raise ValueError('Number of players must be between 3 and 6')

        # Initialize statistics tracking
        self.stats = {
            player_class.__name__: {
                'total_games': 0,
                'wins': 0,
                'total_score': 0,
                'scores': [],
                'average_position': 0,
                'positions': [],
                'bets_placed': {i: 0 for i in range(1, 21)},  # Track wins for each round 1-20
                'right_bets': {i: 0 for i in range(1, 21)}  # Track how many times each round was played
            }
            for player_class in player_classes
        }

        # Run games
        for game_num in range(num_games):
            # Create new game instance
            game = WizardGame()

            # Create players for this game
            game_players = []
            for p_class in player_classes:
                # player_class = np.random.choice(player_classes)
                player = p_class(f'{p_class.__name__ }')
                game_players.append(player)
                game.add_player(player)

            # Play the game
            game.start_game()

            # Update statistics
            self._update_stats(game)

            if (game_num + 1) % 10 == 0:
                print(f'Completed {game_num + 1} games')

        # Calculate final statistics
        self._calculate_final_stats(num_games)

        return self.stats

    def _update_stats(self, game: WizardGame):
        """Update statistics after each game"""
        scores = game.current_scores
        round_scores = game.round_scores

        # Sort players by score to get positions
        sorted_players = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        max_score = sorted_players[0][1]

        for position, (player, score) in enumerate(sorted_players, 1):
            player_class_name = player.__class__.__name__
            stats = self.stats[player_class_name]

            stats['total_games'] += 1
            stats['total_score'] += score
            stats['scores'].append(score)
            stats['positions'].append(position)

            # Count wins (including ties)
            if score == max_score:
                stats['wins'] += 1

            for round_num, round_results in round_scores.items():
                stats['bets_placed'][round_num] += 1
                if round_results[player] > 0:
                    stats['right_bets'][round_num] += 1

    def _calculate_final_stats(self, num_games: int):
        """Calculate final statistics for all players"""
        for player_stats in self.stats.values():
            if player_stats['total_games'] > 0:
                player_stats['average_score'] = player_stats['total_score'] / player_stats['total_games']
                player_stats['win_rate'] = player_stats['wins'] / player_stats['total_games']
                player_stats['average_position'] = sum(player_stats['positions']) / len(player_stats['positions'])
                player_stats['score_std'] = np.std(player_stats['scores'])

                # Calculate position distribution
                position_counts = np.bincount(player_stats['positions'], minlength=7)[1:7]
                player_stats['position_distribution'] = position_counts / len(player_stats['positions'])

    def print_results(self):
        """Print formatted results of the evaluation"""
        print('\nEvaluation Results:')
        print('-' * 80)

        for player_name, stats in self.stats.items():
            print(f'\nPlayer: {player_name}')
            print(f"Games Played: {stats['total_games']}")
            print(f"Win Rate: {stats['win_rate']:.2%}")
            print(f"Average Score: {stats['average_score']:.2f} (±{stats['score_std']:.2f})")
            print(f"Average Position: {stats['average_position']:.2f}")
            print("Position Distribution:")
            for pos, freq in enumerate(stats['position_distribution'], 1):
                print(f"  {pos}th: {freq:.2%}")

            print('\nRound Correct Bets:')
            for round_num in range(1, 21):
                placed_bets = stats['bets_placed'][round_num]
                right_bets = stats['right_bets'][round_num]
                if placed_bets > 0:
                    correct_bet_percentage = right_bets / placed_bets
                    print(f"  Round {round_num}: {correct_bet_percentage:.2%} ({right_bets} / {placed_bets})")
                else:
                    print(f"Round {round_num}: No plays")

        print("-" * 80)
