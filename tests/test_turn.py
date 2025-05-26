from unittest.mock import create_autospec, Mock

import pytest

from src.core.player import WizardBasePlayer
from src.core.turn import valid_cards, Turn
from src.game.game_state import GameState
from src.game.wizard_card import WizardCard, CardSuit, CardType

class TestTurn:
    @pytest.fixture
    def mock_player(self):
        player = create_autospec(WizardBasePlayer)
        player.name = 'TestPlayer'
        return player

    @pytest.fixture
    def mock_game_state_callback(self):
        def callback(player):
            return Mock(spec=GameState)
        return callback

    @pytest.fixture
    def base_hand(self):
        return [
            WizardCard(CardType.STANDARD, CardSuit.HEARTS, 10),
            WizardCard(CardType.STANDARD, CardSuit.SPADES, 7),
            WizardCard(CardType.WIZARD),
        ]

    def test_turn_initialization(self, mock_player, base_hand, mock_game_state_callback):
        """Test that Turn is properly initialized"""
        trick_cards = {}
        turn = Turn(mock_player, base_hand, trick_cards, None, mock_game_state_callback)

        assert turn._player == mock_player
        assert turn._hand == base_hand
        assert turn._trick_cards == trick_cards
        assert turn._trick_suit is None

    def test_play_valid_cards(self, mock_player, base_hand, mock_game_state_callback):
        """Test playing a valid card"""
        # Setup player to return a valid card
        valid_card = base_hand[0]  # Hearts 10
        mock_player.play_card.return_value = valid_card

        turn = Turn(mock_player, base_hand, {}, None, mock_game_state_callback)
        played_card = turn.play()

        assert played_card == valid_card
        mock_player.play_card.assert_called_once()

    def test_play_invalid_card_raises_error(self, mock_player, base_hand, mock_game_state_callback):
        """Test that playing an invalid card raises an error"""
        # Setup player to return a card not in hand
        invalid_card = WizardCard(CardType.STANDARD, CardSuit.DIAMONDS, 3)
        mock_player.play_card.return_value = invalid_card

        turn = Turn(mock_player, base_hand, {}, None, mock_game_state_callback)

        with pytest.raises(ValueError):
            turn.play()

    def test_play_special_card_always_valid(self, mock_player, mock_game_state_callback):
        """Test that special cards (Wizard/Jester) can always be played"""
        hand = [
            WizardCard(CardType.WIZARD),
            WizardCard(CardType.STANDARD, CardSuit.SPADES, 7),
        ]
        trick_cards = {
            Mock(): WizardCard(CardType.STANDARD, CardSuit.HEARTS, 5)
        }

        # Try to play Wizard when heart is required
        mock_player.play_card.return_value = hand[0]

        turn = Turn(mock_player, hand, trick_cards, CardSuit.HEARTS, mock_game_state_callback)
        played_card = turn.play()

        assert played_card.card_type == CardType.WIZARD

    def test_play_removes_card_from_hand(self, mock_player, base_hand, mock_game_state_callback):
        """Test that played card is removed from hand"""
        played_card = base_hand[0]
        mock_player.play_card.return_value = played_card

        turn = Turn(mock_player, base_hand.copy(), {}, None, mock_game_state_callback)
        turn.play()

        assert played_card not in turn._hand
        assert len(turn._hand) == len(base_hand) - 1

    def test_game_state_callback_called(self, mock_player, base_hand, mock_game_state_callback):
        """Test that game state callback is called when getting state"""
        mock_callback = Mock(return_value=Mock(spec=GameState))

        turn = Turn(mock_player, base_hand, {}, None, mock_callback)
        mock_player.play_card.return_value = base_hand[0]

        turn.play()

        mock_callback.assert_called_once_with(mock_player)
        mock_player.play_card.assert_called_once()

    def test_empty_hand_raises_error(self, mock_player, mock_game_state_callback):
        """Test that playing with empty hand raises error"""
        turn = Turn(mock_player, [], {}, None, mock_game_state_callback)

        with pytest.raises(ValueError):
            turn.play()

    def test_play_with_no_valid_moves(self, mock_player, mock_game_state_callback):
        """Test behavior when there are no valid moves available"""
        hand = [WizardCard(CardType.STANDARD, CardSuit.SPADES, 7)]
        trick_cards = {
            Mock(): WizardCard(CardType.STANDARD, CardSuit.HEARTS, 5)
        }

        turn = Turn(mock_player, hand, trick_cards, CardSuit.HEARTS, mock_game_state_callback)
        mock_player.play_card.return_value = hand[0]

        # Should be allowed to play any card when no valid moves
        played_card = turn.play()
        assert played_card == WizardCard(CardType.STANDARD, CardSuit.SPADES, 7)


class TestValidCards:
    @pytest.fixture
    def standard_cards(self):
        """Create a set of standard cards from different suits"""
        return [
            WizardCard(CardType.STANDARD, CardSuit.HEARTS, 10),
            WizardCard(CardType.STANDARD, CardSuit.HEARTS, 5),
            WizardCard(CardType.STANDARD, CardSuit.SPADES, 7),
            WizardCard(CardType.STANDARD, CardSuit.DIAMONDS, 8),
            WizardCard(CardType.STANDARD, CardSuit.CLUBS, 9),
        ]

    @pytest.fixture
    def special_cards(self):
        """Create wizard and jester cards"""
        return [
            WizardCard(CardType.WIZARD),
            WizardCard(CardType.JESTER)
        ]

    def test_empty_trick_allows_any_card(self, standard_cards, special_cards):
        """When no cards have been played, a player can play any card"""
        hand = standard_cards + special_cards
        valid = valid_cards(hand, [], None)
        assert set(valid) == set(hand)

    def test_must_follow_suit_if_possible(self):
        """Player must play cards of the same suit if they have them"""
        hand = [
            WizardCard(CardType.STANDARD, CardSuit.HEARTS, 10),
            WizardCard(CardType.STANDARD, CardSuit.HEARTS, 5),
            WizardCard(CardType.STANDARD, CardSuit.SPADES, 7),
        ]
        trick = [WizardCard(CardType.STANDARD, CardSuit.HEARTS, 8)]
        valid = valid_cards(hand, trick, CardSuit.HEARTS)

        # Only heart cards should be valid
        assert len(valid) == 2
        assert all(card.card_suit == CardSuit.HEARTS for card in valid)

    def test_can_play_any_card_if_cant_follow_suit(self):
        """If a player can't follow suit, they can play any card"""
        hand = [
            WizardCard(CardType.STANDARD, CardSuit.SPADES, 7),
            WizardCard(CardType.STANDARD, CardSuit.DIAMONDS, 8),
        ]
        trick = [WizardCard(CardType.STANDARD, CardSuit.HEARTS, 8)]
        valid = valid_cards(hand, trick, CardSuit.HEARTS)

        assert set(valid) == set(hand)

    def test_special_cards_always_valid(self):
        """Wizard and Jester cards can always be played"""
        hand = [
            WizardCard(CardType.STANDARD, CardSuit.SPADES, 7),
            WizardCard(CardType.WIZARD),
            WizardCard(CardType.JESTER),
        ]
        trick = [WizardCard(CardType.STANDARD, CardSuit.HEARTS, 8)]
        valid = valid_cards(hand, trick, CardSuit.HEARTS)

        # Should include both special cards
        special_cards = [card for card in valid if card.card_type != CardType.STANDARD]
        assert len(special_cards) == 2

    def test_special_cards_only_hand(self, special_cards):
        """Test when the hand only contains special cards"""
        hand = special_cards
        trick = [WizardCard(CardType.STANDARD, CardSuit.HEARTS, 8)]
        valid = valid_cards(hand, trick, CardSuit.HEARTS)

        assert set(valid) == set(hand)

    def test_mixed_valid_cards(self):
        """Test with a mix of matching suit and special cards"""
        hand = [
            WizardCard(CardType.STANDARD, CardSuit.HEARTS, 10),
            WizardCard(CardType.WIZARD),
            WizardCard(CardType.STANDARD, CardSuit.SPADES, 7),
            WizardCard(CardType.JESTER),
        ]
        trick = [WizardCard(CardType.STANDARD, CardSuit.HEARTS, 8)]
        valid = valid_cards(hand, trick, CardSuit.HEARTS)

        # Should include a heart card and both special cards
        assert len(valid) == 3
        assert any(card.card_type == CardType.STANDARD and card.card_suit == CardSuit.HEARTS for card in valid)
        assert any(card.card_type == CardType.WIZARD for card in valid)
        assert any(card.card_type == CardType.JESTER for card in valid)

    def test_trick_with_multiple_cards(self):
        """Test that only the first card in a trick determines the required suit"""
        hand = [
            WizardCard(CardType.STANDARD, CardSuit.HEARTS, 10),
            WizardCard(CardType.STANDARD, CardSuit.SPADES, 7),
        ]
        trick = [
            WizardCard(CardType.STANDARD, CardSuit.HEARTS, 8),
            WizardCard(CardType.STANDARD, CardSuit.SPADES, 9),
        ]
        valid = valid_cards(hand, trick, CardSuit.HEARTS)

        assert len(valid) == 1
        assert valid[0].card_suit == CardSuit.HEARTS

    def test_empty_hand(self):
        """Test with an empty hand"""
        trick = [WizardCard(CardType.STANDARD, CardSuit.HEARTS, 8)]
        valid = valid_cards([], trick, CardSuit.HEARTS)

        assert valid == []

    def test_null_trick_suit(self):
        """Test behavior when trick suit is None"""
        hand = [
            WizardCard(CardType.STANDARD, CardSuit.HEARTS, 10),
            WizardCard(CardType.STANDARD, CardSuit.SPADES, 7),
        ]
        trick = [WizardCard(CardType.STANDARD, CardSuit.HEARTS, 8)]
        valid = valid_cards(hand, trick, None)

        # Should be able to play any card
        assert set(valid) == set(hand)


