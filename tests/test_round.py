import pytest
from unittest.mock import Mock, patch
from src.core.player import WizardBasePlayer
from src.core.trick import Trick
from src.game.wizard_card import WizardCard
from src.core.round import Round


class TestRound:
    @pytest.fixture
    def mock_players(self):
        # Create mock players
        player1 = Mock(spec=WizardBasePlayer)
        player2 = Mock(spec=WizardBasePlayer)
        player1.name = "Player1"
        player2.name = "Player2"
        return [player1, player2]

    @pytest.fixture
    def mock_game_state_callback(self):
        return Mock()

    @pytest.fixture
    def round_instance(self, mock_players, mock_game_state_callback):
        return Round(round_number=1, players=mock_players, game_state_callback=mock_game_state_callback)

    @pytest.fixture
    def mock_wizard_card(self):
        card = Mock(spec=WizardCard)
        card.card_suit = "Hearts"
        card.card_value = 7
        return card

    def test_round_initialization(self, round_instance, mock_players):
        """Test if Round is initialized correctly"""
        assert round_instance.round_number == 1
        assert len(round_instance.hands) == len(mock_players)
        # Each player should have cards equal to round number
        for player in mock_players:
            assert len(round_instance.hands[player]) == 1

    def test_bidding_phase(self, round_instance, mock_players):
        """Test if bidding phase works correctly"""
        # Setup mock bids
        mock_players[0].make_bid.return_value = 1
        mock_players[1].make_bid.return_value = 0

        round_instance.run_bidding_phase()

        assert round_instance.current_bets[mock_players[0]] == 1
        assert round_instance.current_bets[mock_players[1]] == 0

    def test_calculate_scores_correct_bet(self, round_instance, mock_players):
        """Test score calculation when players make correct bets"""
        # Setup test data
        round_instance._current_bets = {
            mock_players[0]: 1,
            mock_players[1]: 0
        }
        round_instance._won_tricks = {
            mock_players[0]: 1,  # Matches bet
            mock_players[1]: 0  # Matches bet
        }

        scores = round_instance.calculate_scores()

        # Both players should get 20 points + (bet * 10)
        assert scores[mock_players[0]] == 30  # 20 + (1 * 10)
        assert scores[mock_players[1]] == 20  # 20 + (0 * 10)

    def test_calculate_scores_incorrect_bet(self, round_instance, mock_players):
        """Test score calculation when players make incorrect bets"""
        # Setup test data
        round_instance._current_bets = {
            mock_players[0]: 1,
            mock_players[1]: 1
        }
        round_instance._won_tricks = {
            mock_players[0]: 0,  # Off by 1
            mock_players[1]: 0  # Off by 1
        }

        scores = round_instance.calculate_scores()

        # Players should lose 10 points per trick difference
        assert scores[mock_players[0]] == -10
        assert scores[mock_players[1]] == -10

    def test_play_trick(self, round_instance, mock_players, mock_wizard_card):
        """Test playing a single trick with valid cards"""
        # Set up valid hands for players
        round_instance._hands = {
            mock_players[0]: [mock_wizard_card],
            mock_players[1]: [mock_wizard_card]
        }

        # Mock players' play_card behavior to return valid cards
        mock_players[0].play_card = Mock(return_value=mock_wizard_card)
        mock_players[1].play_card = Mock(return_value=mock_wizard_card)

        # Patch Trick creation to control its behavior
        with patch('src.core.round.Trick') as MockTrick:
            mock_trick = MockTrick.return_value
            mock_trick.play.return_value = mock_players[0]

            winner = round_instance.play_trick(mock_players[0])

            # Verify Trick was created with the correct parameters
            MockTrick.assert_called_once_with(
                round_instance._players.copy(),
                round_instance._hands,
                round_instance.trump_suit,
                round_instance._game_state_callback
            )

            # Verify the trick was played
            assert mock_trick.play.called
            assert winner == mock_players[0]

            # Verify hands are valid before playing
            assert mock_wizard_card in round_instance._hands[mock_players[0]]
            assert mock_wizard_card in round_instance._hands[mock_players[1]]

    def test_trump_suit_with_no_trump_card(self, round_instance):
        """Test trump suit when no trump card is present"""
        round_instance._trump_card = None
        assert round_instance.trump_suit is None

    def test_trump_suit_with_trump_card(self, round_instance):
        """Test trump suit when trump card is present"""
        mock_trump_card = Mock(spec=WizardCard)
        mock_trump_card.card_suit = "Hearts"
        round_instance._trump_card = mock_trump_card

        assert round_instance.trump_suit == "Hearts"
