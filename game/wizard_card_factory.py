from game.wizard_card import WizardCard, CardType, CardSuit

def create_wizard_cards() -> list[WizardCard]:
    normal_cards = [
        WizardCard(CardType.STANDARD, suit, value)
        for suit in CardSuit
        for value in range(1, 14)
    ]

    special_cards = (
        [WizardCard(CardType.WIZARD)] * 4 +
        [WizardCard(CardType.JESTER)] * 4
    )

    return normal_cards + special_cards