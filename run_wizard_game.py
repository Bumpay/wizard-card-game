from src.ai.debug_agent import WizardDebugPlayer
from src.ai.simple_agent import WizardSimpleBot
from src.ai.wizard_environment import WizardEnvironment

# Create and run the environment
env = WizardEnvironment()
results = env.evaluate_players(
    player_classes=[WizardSimpleBot, WizardDebugPlayer],
    num_games=1000,
    players_per_game=4
)

# Print the results
env.print_results()