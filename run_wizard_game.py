import logging

from src.ai.debug_agent import WizardDebugPlayer
from src.ai.simple_agent import WizardSimpleBot
from src.ai.wizard_environment import WizardEnvironment
from src.ai.adrian_agent import WizardAdrianPlayerV01

logging.getLogger('src.game.wizard_game').setLevel(logging.WARNING)
logging.getLogger('src.core.round').setLevel(logging.WARNING)
logging.getLogger('src.core.trick').setLevel(logging.WARNING)

# Create and run the environment
env = WizardEnvironment()
results = env.evaluate_players(
    player_classes=[WizardSimpleBot, WizardDebugPlayer, WizardAdrianPlayerV01],
    num_games=1000,
    players_per_game=6
)

# Print the results
env.print_results()