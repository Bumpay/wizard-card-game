from src.game.wizard_game import WizardGame
from src.ai.base_agent import WizardDebugPlayer
from src.ai.adrian_agent import WizardAdrianPlayerV01

def main():

    for i in range(100000):
        game = WizardGame()
        game.add_player(WizardAdrianPlayerV01('Adrian'))
        game.add_player(WizardDebugPlayer('Bertha'))
        game.add_player(WizardDebugPlayer('Chris'))
        game.start_game()


if __name__ == '__main__':
    main()