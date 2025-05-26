from game.wizard_game import WizardGame
from ai.base_agent import WizardDebugPlayer
from ai.simple_agent import WizardSimpleBot
from ai.adrian_agent import WizardAdrianPlayerV01

def test():
#    game = WizardGame()
#    game.add_player(WizardSimpleBot('Albert'))
#    game.add_player(WizardSimpleBot('Bertha'))
#    game.add_player(WizardSimpleBot('Chris'))
#    game.add_player(WizardDebugPlayer('Dora'))
#    game.add_player(WizardDebugPlayer('Emil'))
#    game.add_player(WizardDebugPlayer('Francisca'))

    for i in range(1000):
        game = WizardGame()
        game.add_player(WizardAdrianPlayerV01('Adrian'))
        game.add_player(WizardDebugPlayer('Bertha'))
        game.add_player(WizardDebugPlayer('Chris'))
        game.start_game()


if __name__ == '__main__':
    test()