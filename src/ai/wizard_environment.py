from typing import Type

import numpy as np
from matplotlib import pyplot as plt

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
                'right_bets': {i: 0 for i in range(1, 21)},  # Track how many times each round was played
                'bet_history': {i: {'bets': [], 'diffs': []} for i in range(1, 21)},
                'round_scores': {i: [] for i in range(1, 21)},  # New: scores per round
                'cumulative_scores': []  # New: final game scores
            }
            for player_class in player_classes
        }

        # Run games
        for game_num in range(num_games):
            # Create new game instance
            game = WizardGame()

            # Create players for this game
            game_players = []
            for i, p_class in enumerate(player_classes):
                # player_class = np.random.choice(player_classes)
                player = p_class(f'{p_class.__name__ }_{i}')
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
        bets_history = game.bets_history

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
            stats['cumulative_scores'].append(score)  # Store final game score

            # Count wins (including ties)
            if score == max_score:
                stats['wins'] += 1

            for round_num in bets_history:
                if player in bets_history[round_num]:
                    stats['round_scores'][round_num].append(round_scores[round_num][player])
                    bet_info = bets_history[round_num][player]
                    stats['bets_placed'][round_num] += 1
                    if bet_info['diff'] == 0:
                        stats['right_bets'][round_num] += 1

                    stats['bet_history'][round_num]['bets'].append(bet_info['bet'])
                    stats['bet_history'][round_num]['diffs'].append(bet_info['diff'])

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

            print("\nPosition Distribution:")
            for pos, freq in enumerate(stats['position_distribution'], 1):
                print(f"  {pos}th: {freq:.2%}")

            print('\nBetting Statistics by Round:')
            for round_num in range(1, 21):
                placed_bets = stats['bets_placed'][round_num]
                if placed_bets > 0:
                    bet_history = stats['bet_history'][round_num]
                    avg_bet = np.mean(bet_history['bets'])
                    avg_diff = np.mean(bet_history['diffs'])
                    right_bets = stats['right_bets'][round_num]
                    accuracy = right_bets / placed_bets

                    print(f'  Round {round_num}:')
                    print(f'    Accuracy: {accuracy:.2%} ({right_bets}/{placed_bets})')
                    print(f'    Avg Bet:  {avg_bet:.2}')
                    print(f'    Avg Diff: {avg_diff:.2}')

        print("-" * 80)

    def plot_betting_patterns(self, save_path: str = None):
        """
        Create plots showing betting patterns and differences, including distributions.

        Args:
            save_path: Optional path to save the plot
        """
        plt.figure(figsize=(20, 16))
        gs = plt.GridSpec(4, 1, height_ratios=[1, 2, 1, 2])

        # Create four subplots
        ax1 = plt.subplot(gs[0])  # Average bets line plot
        ax2 = plt.subplot(gs[1])  # Bet distributions
        ax3 = plt.subplot(gs[2])  # Average differences line plot
        ax4 = plt.subplot(gs[3])  # Difference distributions

        colors = plt.cm.tab10(np.linspace(0, 1, len(self.stats)))

        for (player_name, stats), color in zip(self.stats.items(), colors):
            rounds = []
            avg_bets = []
            avg_diffs = []
            all_bets_by_round = []
            all_diffs_by_round = []

            # Collect data for all plots
            for round_num in range(1, 21):
                if stats['bets_placed'][round_num] > 0:
                    rounds.append(round_num)
                    bet_history = stats['bet_history'][round_num]
                    avg_bets.append(np.mean(bet_history['bets']))
                    avg_diffs.append(np.mean(bet_history['diffs']))
                    all_bets_by_round.append(bet_history['bets'])
                    all_diffs_by_round.append(bet_history['diffs'])

            # Plot average lines
            ax1.plot(rounds, avg_bets, marker='o', label=player_name, color=color)
            ax3.plot(rounds, avg_diffs, marker='s', label=player_name, color=color)

            # Create violin plots and scatter for bets
            violin_positions_bets = []
            violin_data_bets = []
            for round_num, bets in zip(rounds, all_bets_by_round):
                if len(bets) > 0:
                    violin_positions_bets.extend([round_num] * len(bets))
                    violin_data_bets.extend(bets)

            parts_bets = ax2.violinplot([np.array(bets) for bets in all_bets_by_round],
                                        positions=rounds,
                                        showmeans=True,
                                        showextrema=True)

            # Create violin plots and scatter for differences
            violin_positions_diffs = []
            violin_data_diffs = []
            for round_num, diffs in zip(rounds, all_diffs_by_round):
                if len(diffs) > 0:
                    violin_positions_diffs.extend([round_num] * len(diffs))
                    violin_data_diffs.extend(diffs)

            parts_diffs = ax4.violinplot([np.array(diffs) for diffs in all_diffs_by_round],
                                         positions=rounds,
                                         showmeans=True,
                                         showextrema=True)

            # Customize violin plots colors
            for parts in [parts_bets, parts_diffs]:
                for pc in parts['bodies']:
                    pc.set_facecolor(color)
                    pc.set_alpha(0.3)
                parts['cmeans'].set_color(color)

            # Add scatter plots
            ax2.scatter(violin_positions_bets, violin_data_bets,
                        color=color, alpha=0.2, s=20,
                        label=f"{player_name} bets")
            ax4.scatter(violin_positions_diffs, violin_data_diffs,
                        color=color, alpha=0.2, s=20,
                        label=f"{player_name} diffs")

        # Customize average bets plot
        ax1.set_xlabel('')
        ax1.set_ylabel('Average Bet')
        ax1.set_title('Average Bets by Round')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Customize bets distribution plot
        ax2.set_xlabel('')
        ax2.set_ylabel('Bets')
        ax2.set_title('Bet Distribution by Round')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        # Customize average differences plot
        ax3.set_xlabel('')
        ax3.set_ylabel('Average Difference')
        ax3.set_title('Average Bet Difference by Round')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        # Customize differences distribution plot
        ax4.set_xlabel('Round Number')
        ax4.set_ylabel('Differences')
        ax4.set_title('Bet Difference Distribution by Round')
        ax4.grid(True, alpha=0.3)
        ax4.legend()

        # Adjust layout and display
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

    def plot_score_distributions(self, save_path: str = None):
        """
        Create plots showing round scores and final score distributions.
        """
        plt.figure(figsize=(20, 16))
        gs = plt.GridSpec(3, 1, height_ratios=[1, 2, 2])

        ax1 = plt.subplot(gs[0])  # Average round scores
        ax2 = plt.subplot(gs[1])  # Round score distributions
        ax3 = plt.subplot(gs[2])  # Final score distributions

        colors = plt.cm.tab10(np.linspace(0, 1, len(self.stats)))

        for (player_name, stats), color in zip(self.stats.items(), colors):
            rounds = []
            avg_scores = []
            all_round_scores = []

            # Collect round score data
            for round_num in range(1, 21):
                round_scores = stats['round_scores'][round_num]
                if round_scores:
                    rounds.append(round_num)
                    avg_scores.append(np.mean(round_scores))
                    all_round_scores.append(round_scores)

            # Plot average round scores
            ax1.plot(rounds, avg_scores, marker='o', label=player_name, color=color)

            # Create violin plot for round scores
            parts_scores = ax2.violinplot(all_round_scores,
                                          positions=rounds,
                                          showmeans=True,
                                          showextrema=True)

            # Customize violin plot colors
            for pc in parts_scores['bodies']:
                pc.set_facecolor(color)
                pc.set_alpha(0.3)
            parts_scores['cmeans'].set_color(color)

            # Add scatter for round scores
            for round_num, scores in zip(rounds, all_round_scores):
                ax2.scatter([round_num] * len(scores), scores,
                            color=color, alpha=0.2, s=20)

            # Plot final score distribution
            final_scores = stats['cumulative_scores']
            ax3.hist(final_scores, bins=30, alpha=0.3, label=player_name,
                     color=color, density=True)

            # Add KDE to final score distribution
            from scipy import stats as scipy_stats
            kernel = scipy_stats.gaussian_kde(final_scores)
            x_range = np.linspace(min(final_scores), max(final_scores), 200)
            ax3.plot(x_range, kernel(x_range), color=color, linewidth=2)

        # Customize average round scores plot
        ax1.set_xlabel('')
        ax1.set_ylabel('Average Round Score')
        ax1.set_title('Average Scores by Round')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Customize round score distribution plot
        ax2.set_xlabel('Round Number')
        ax2.set_ylabel('Round Score')
        ax2.set_title('Round Score Distribution')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        # Customize final score distribution plot
        ax3.set_xlabel('Final Score')
        ax3.set_ylabel('Density')
        ax3.set_title('Final Score Distribution')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
