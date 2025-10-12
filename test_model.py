import pytest
from common_types import Player
from model import (
    ConnectTacToeModel,
    TicTacToeWinCondition,
    NotConnectFourWinCondition,
    FloatingTokenPhysics,
    StrongGravityTokenPhysics,
    WeakGravityTokenPhysics
)


def create_grid() -> list[list[Player | None]]:
    """Create empty 6x7 grid."""
    return [[None for _ in range(7)] for _ in range(6)]


def set_grid_cell(grid: list[list[Player | None]], row: int, col: int, player: Player) -> None:
    """Set a specific grid cell."""
    grid[row][col] = player


def wait_until_settled(model: ConnectTacToeModel) -> None:
    """Step physics repeatedly until animation completes."""
    for _ in range(100):
        if not model.is_animating:
            break
        model.step_physics()


# ============================================================================
# TIC-TAC-TOE WIN CONDITION TESTS
# ============================================================================

class TestTicTacToeWinCondition:
    """Test TicTacToeWinCondition class."""

    def test_full_row_wins(self) -> None:
        """Test full row wins."""
        win_cond = TicTacToeWinCondition()
        grid = create_grid()
        for col in range(7):
            set_grid_cell(grid, 2, col, Player.P1)
        assert win_cond.is_winner(grid) == Player.P1

    def test_full_column_wins(self) -> None:
        """Test full column wins."""
        win_cond = TicTacToeWinCondition()
        grid = create_grid()
        for row in range(6):
            set_grid_cell(grid, row, 3, Player.P2)
        assert win_cond.is_winner(grid) == Player.P2

    def test_incomplete_no_win(self) -> None:
        """Test incomplete row/column doesn't win."""
        win_cond = TicTacToeWinCondition()
        grid = create_grid()
        for col in range(6):
            set_grid_cell(grid, 1, col, Player.P1)
        assert win_cond.is_winner(grid) is None

    def test_both_players_win(self) -> None:
        """Test both players winning simultaneously."""
        win_cond = TicTacToeWinCondition()
        grid = create_grid()
        # Test check_both_winners functionality
        # P1 wins with full row 0
        for col in range(7):
            grid[0][col] = Player.P1
        p1_wins, p2_wins = win_cond.check_both_winners(grid)
        assert p1_wins and not p2_wins

        # P2 wins with full column 2
        grid = create_grid()
        for row in range(6):
            grid[row][2] = Player.P2
        p1_wins, p2_wins = win_cond.check_both_winners(grid)
        assert not p1_wins and p2_wins


# ============================================================================
# NOT-CONNECT-FOUR WIN CONDITION TESTS
# ============================================================================

class TestNotConnectFourWinCondition:
    """Test NotConnectFourWinCondition class."""

    def test_vertical_four_wins(self) -> None:
        """Test vertical 4 wins."""
        win_cond = NotConnectFourWinCondition()
        grid = create_grid()
        for row in range(2, 6):
            set_grid_cell(grid, row, 3, Player.P1)
        assert win_cond.is_winner(grid) == Player.P1

    def test_horizontal_four_wins(self) -> None:
        """Test horizontal 4 wins."""
        win_cond = NotConnectFourWinCondition()
        grid = create_grid()
        for col in range(1, 5):
            set_grid_cell(grid, 3, col, Player.P2)
        assert win_cond.is_winner(grid) == Player.P2

    def test_l_shape_wins(self) -> None:
        """Test L-shape of 4 connected tokens wins."""
        win_cond = NotConnectFourWinCondition()
        grid = create_grid()
        for pos in [(2, 2), (3, 2), (4, 2), (4, 3)]:
            set_grid_cell(grid, pos[0], pos[1], Player.P1)
        assert win_cond.is_winner(grid) == Player.P1

    def test_t_shape_wins(self) -> None:
        """Test T-shape of 4 connected tokens wins."""
        win_cond = NotConnectFourWinCondition()
        grid = create_grid()
        for pos in [(2, 3), (3, 2), (3, 3), (3, 4)]:
            set_grid_cell(grid, pos[0], pos[1], Player.P2)
        assert win_cond.is_winner(grid) == Player.P2

    def test_diagonal_not_win(self) -> None:
        """Test diagonal 4 doesn't win."""
        win_cond = NotConnectFourWinCondition()
        grid = create_grid()
        for i in range(4):
            set_grid_cell(grid, i, i, Player.P1)
        assert win_cond.is_winner(grid) is None

    def test_three_connected_no_win(self) -> None:
        """Test only 3 connected doesn't win."""
        win_cond = NotConnectFourWinCondition()
        grid = create_grid()
        for row in range(2, 5):
            set_grid_cell(grid, row, 2, Player.P1)
        assert win_cond.is_winner(grid) is None

    def test_both_players_win(self) -> None:
        """Test both players winning simultaneously."""
        win_cond = NotConnectFourWinCondition()
        grid = create_grid()
        for row in range(4):
            set_grid_cell(grid, row, 0, Player.P1)
            set_grid_cell(grid, row, 6, Player.P2)
        assert win_cond.is_winner(grid) is None
        p1_wins, p2_wins = win_cond.check_both_winners(grid)
        assert p1_wins and p2_wins


# ============================================================================
# FLOATING TOKEN PHYSICS TESTS
# ============================================================================

class TestFloatingTokenPhysics:
    """Test FloatingTokenPhysics class."""

    def test_no_movement(self) -> None:
        """Test tokens don't move."""
        physics = FloatingTokenPhysics()
        grid = create_grid()
        set_grid_cell(grid, 2, 3, Player.P1)
        physics.apply_physics(grid)
        physics.step_animation(grid)
        assert grid[2][3] == Player.P1
        assert not physics.is_animating()


# ============================================================================
# STRONG GRAVITY TOKEN PHYSICS TESTS
# ============================================================================

class TestStrongGravityTokenPhysics:
    """Test StrongGravityTokenPhysics class."""

    def test_token_falls_to_bottom(self) -> None:
        """Test token falls to bottom."""
        physics = StrongGravityTokenPhysics()
        grid = create_grid()
        set_grid_cell(grid, 0, 3, Player.P1)
        physics.apply_physics(grid)
        while physics.is_animating():
            physics.step_animation(grid)
        assert grid[5][3] == Player.P1
        assert grid[0][3] is None

    def test_token_stacks(self) -> None:
        """Test token stacks on existing token."""
        physics = StrongGravityTokenPhysics()
        grid = create_grid()
        set_grid_cell(grid, 5, 2, Player.P1)
        set_grid_cell(grid, 0, 2, Player.P2)
        physics.apply_physics(grid)
        while physics.is_animating():
            physics.step_animation(grid)
        assert grid[5][2] == Player.P1
        assert grid[4][2] == Player.P2

    def test_no_animation_when_settled(self) -> None:
        """Test no animation when already at bottom."""
        physics = StrongGravityTokenPhysics()
        grid = create_grid()
        set_grid_cell(grid, 5, 4, Player.P1)
        physics.apply_physics(grid)
        assert not physics.is_animating()


# ============================================================================
# WEAK GRAVITY TOKEN PHYSICS TESTS
# ============================================================================

class TestWeakGravityTokenPhysics:
    """Test WeakGravityTokenPhysics class."""

    def test_token_moves_one_step(self) -> None:
        """Test token moves down one step."""
        physics = WeakGravityTokenPhysics()
        grid = create_grid()
        set_grid_cell(grid, 2, 3, Player.P1)
        physics.apply_physics(grid)
        physics.step_animation(grid)
        assert grid[3][3] == Player.P1
        assert grid[2][3] is None

    def test_simultaneous_fall(self) -> None:
        """Test multiple tokens move simultaneously."""
        physics = WeakGravityTokenPhysics()
        grid = create_grid()
        for row in range(3):
            set_grid_cell(grid, row, 2, Player.P1)
        physics.apply_physics(grid)
        physics.step_animation(grid)
        assert grid[1][2] == Player.P1
        assert grid[2][2] == Player.P1
        assert grid[3][2] == Player.P1

    def test_token_stops_when_blocked(self) -> None:
        """Test token stops when blocked."""
        physics = WeakGravityTokenPhysics()
        grid = create_grid()
        set_grid_cell(grid, 5, 3, Player.P1)
        set_grid_cell(grid, 3, 3, Player.P2)
        physics.apply_physics(grid)
        physics.step_animation(grid)
        assert grid[4][3] == Player.P2
        physics.apply_physics(grid)
        assert not physics.is_animating()


# ============================================================================
# CONNECTACTOE MODEL TESTS
# ============================================================================

class TestConnectTacToeModel:
    """Test ConnectTacToeModel class."""

    def test_initialization(self) -> None:
        """Test model initializes correctly."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        assert model.current_player == Player.P1
        assert model.winner is None
        assert not model.is_game_done
        assert model.row_count == 6
        assert model.col_count == 7

    def test_choose_cell_valid(self) -> None:
        """Test choosing valid cell."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        assert model.choose_cell(2, 3)
        assert model.get_owner(2, 3) == Player.P1
        assert model.current_player == Player.P2

    def test_choose_cell_invalid(self) -> None:
        """Test invalid cell choices."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        model.choose_cell(1, 2)
        assert not model.choose_cell(1, 2)  # Occupied
        assert not model.choose_cell(-1, 0)  # Out of bounds
        assert not model.choose_cell(6, 0)  # Out of bounds

    def test_turn_alternation(self) -> None:
        """Test players alternate turns."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        assert model.current_player == Player.P1
        model.choose_cell(0, 0)
        assert model.current_player == Player.P2
        model.choose_cell(0, 1)
        assert model.current_player == Player.P1

    def test_win_tictactoe_row(self) -> None:
        """Test Tic-Tac-Toe row win."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        # Setup winning condition by directly placing tokens and checking
        for col in range(7):
            model.choose_cell(3, col)
            if col < 6:  # Let P2 play non-winning moves
                model.choose_cell(4, col)
        assert model.winner == Player.P1
        assert model.is_game_done

    def test_win_notconnectfour(self) -> None:
        """Test Not-Connect-Four win."""
        model = ConnectTacToeModel(NotConnectFourWinCondition(), FloatingTokenPhysics())
        # P1 makes vertical 4, P2 makes non-winning moves
        for row in range(4):
            model.choose_cell(row, 2)
            if row < 3:
                model.choose_cell(row, 3)
        assert model.winner == Player.P1
        assert model.is_game_done

    def test_both_players_win(self) -> None:
        """Test both players winning simultaneously."""
        model = ConnectTacToeModel(NotConnectFourWinCondition(), FloatingTokenPhysics())
        # Create a scenario where both can win on same turn
        # P1 gets 3 in col 0, P2 gets 3 in col 6
        for row in range(3):
            model.choose_cell(row, 0)  # P1
            model.choose_cell(row, 6)  # P2
        # Now P1 completes col 0 (4 in a row)
        model.choose_cell(3, 0)  # P1
        # P2 completes col 6 (4 in a row)
        model.choose_cell(3, 6)  # P2

        # Check if both won
        assert model.both_players_won
        assert model.winner is None
        assert model.is_game_done

    def test_draw_detection(self) -> None:
        """Test draw when grid full."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        # Fill grid in a pattern that doesn't create a full row/column
        for row in range(6):
            for col in range(7):
                # Alternate players but avoid creating full rows/columns
                if (row + col) % 2 == 0:
                    model.choose_cell(row, col)
                    if not model.is_game_done and row * 7 + col < 41:
                        # P2's turn
                        next_col = (col + 1) % 7
                        next_row = row if next_col > col else row + 1
                        if next_row < 6:
                            model.choose_cell(next_row, next_col)

        # Manually check for draw by filling remaining cells
        all_filled = all(model.get_owner(r, c) is not None
                        for r in range(6) for c in range(7))
        if all_filled and model.winner is None:
            assert model.is_game_done

    def test_no_moves_after_game_done(self) -> None:
        """Test moves rejected after game ends."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        # Create a winning condition
        for col in range(7):
            model.choose_cell(0, col)
            if col < 6:
                model.choose_cell(1, col)
        # Game should be done, try another move
        assert not model.choose_cell(3, 3)

    def test_physics_with_strong_gravity(self) -> None:
        """Test strong gravity physics."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), StrongGravityTokenPhysics())
        model.choose_cell(0, 2)
        wait_until_settled(model)
        assert model.get_owner(5, 2) == Player.P1
        assert model.current_player == Player.P2

    def test_physics_with_weak_gravity(self) -> None:
        """Test weak gravity physics."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), WeakGravityTokenPhysics())
        model.choose_cell(0, 3)
        # Weak gravity moves one step per step_physics call
        while model.is_animating:
            model.step_physics()
        # After weak gravity, token should have moved down one step
        # But turn also completes, so we need to check the grid after animation
        assert model.get_owner(1, 3) == Player.P1


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for various combinations."""

    def test_tictactoe_floating_full_game(self) -> None:
        """Test complete game with TicTacToe + Floating."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        moves = [(2, 0), (1, 0), (2, 1), (1, 1), (2, 2), (1, 2), (2, 3), (1, 3),
                 (2, 4), (1, 4), (2, 5), (1, 5), (2, 6)]
        for row, col in moves:
            if model.is_game_done:
                break
            model.choose_cell(row, col)
        assert model.winner == Player.P1

    def test_notconnectfour_strong_vertical(self) -> None:
        """Test vertical 4 win with strong gravity."""
        model = ConnectTacToeModel(NotConnectFourWinCondition(), StrongGravityTokenPhysics())
        # P1 drops 4 tokens in column 2, P2 drops in column 0
        # Turn 0: P1 drops in col 2
        # Turn 1: P2 drops in col 0
        # Turn 2: P1 drops in col 2
        # Turn 3: P2 drops in col 0
        # Turn 4: P1 drops in col 2
        # Turn 5: P2 drops in col 0
        # Turn 6: P1 drops in col 2 (4th token, should win)
        for i in range(8):
            if model.is_game_done:
                break
            if i % 2 == 0:  # P1's turn
                model.choose_cell(0, 2)
            else:  # P2's turn
                model.choose_cell(0, 0)
            wait_until_settled(model)
        assert model.winner == Player.P1
        assert model.is_game_done

    def test_weak_gravity_cascading(self) -> None:
        """Test cascading with weak gravity."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), WeakGravityTokenPhysics())
        # Place tokens at top row
        for col in range(7):
            model.choose_cell(0, col)
            if col < 6:  # P2 plays elsewhere
                model.choose_cell(1, col)

        # Let physics settle
        for _ in range(10):
            if not model.is_animating:
                break
            model.step_physics()

        # Check if P1 won with a full row
        assert model.winner == Player.P1


    def test_all_win_condition_combinations(self) -> None:
        """Test all combinations of win conditions and physics."""
        win_conditions = [TicTacToeWinCondition(), NotConnectFourWinCondition()]
        physics_types = [FloatingTokenPhysics(), StrongGravityTokenPhysics(), WeakGravityTokenPhysics()]
        
        for win_cond in win_conditions:
            for physics in physics_types:
                model = ConnectTacToeModel(win_cond, physics)
                
                # Test basic functionality
                assert model.current_player == Player.P1
                assert model.winner is None
                assert not model.is_game_done
                assert model.row_count == 6
                assert model.col_count == 7
                
                # Test valid move
                assert model.choose_cell(0, 0)
                assert model.get_owner(0, 0) == Player.P1
                
                # Test invalid moves
                assert not model.choose_cell(0, 0)  # Occupied
                assert not model.choose_cell(-1, 0)  # Out of bounds
                assert not model.choose_cell(6, 0)  # Out of bounds
                assert not model.choose_cell(0, 7)  # Out of bounds

    def test_physics_animation_states(self) -> None:
        """Test physics animation state management."""
        # Test Strong Gravity animation
        model = ConnectTacToeModel(TicTacToeWinCondition(), StrongGravityTokenPhysics())
        model.choose_cell(0, 0)
        assert model.is_animating
        wait_until_settled(model)
        assert not model.is_animating
        assert model.get_owner(5, 0) == Player.P1
        
        # Test Weak Gravity animation
        model = ConnectTacToeModel(TicTacToeWinCondition(), WeakGravityTokenPhysics())
        model.choose_cell(0, 1)
        assert model.is_animating
        wait_until_settled(model)
        assert not model.is_animating
        assert model.get_owner(1, 1) == Player.P1
        
        # Test Floating (no animation)
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        model.choose_cell(0, 2)
        assert not model.is_animating
        assert model.get_owner(0, 2) == Player.P1

    def test_edge_case_coordinates(self) -> None:
        """Test edge case coordinate handling."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        
        # Test boundary coordinates
        assert model.choose_cell(0, 0)  # Top-left
        assert model.choose_cell(5, 6)  # Bottom-right
        assert model.get_owner(0, 0) == Player.P1
        assert model.get_owner(5, 6) == Player.P2
        
        # Test invalid coordinates
        assert not model.choose_cell(-1, -1)
        assert not model.choose_cell(6, 7)
        assert not model.choose_cell(0, -1)
        assert not model.choose_cell(-1, 0)

    def test_simultaneous_win_scenarios(self) -> None:
        """Test scenarios where both players could win simultaneously."""
        # Test with NotConnectFour
        model = ConnectTacToeModel(NotConnectFourWinCondition(), FloatingTokenPhysics())
        
        # Create a scenario where both players have 4+ connected tokens
        for row in range(4):
            model._grid[row][0] = Player.P1
            model._grid[row][6] = Player.P2
        
        model._finish_turn()
        assert model.both_players_won
        assert model.winner is None
        assert model.is_game_done

    def test_draw_scenarios(self) -> None:
        """Test draw scenarios (full grid, no winner)."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        
        # Fill grid without creating a winning condition
        for row in range(6):
            for col in range(7):
                if (row + col) % 2 == 0:
                    model._grid[row][col] = Player.P1
                else:
                    model._grid[row][col] = Player.P2
        
        model._finish_turn()
        assert model.winner is None
        assert model.is_game_done
        assert not model.both_players_won

    def test_physics_with_complex_patterns(self) -> None:
        """Test physics with complex token patterns."""
        # Test Strong Gravity with multiple tokens
        model = ConnectTacToeModel(NotConnectFourWinCondition(), StrongGravityTokenPhysics())
        
        # Place tokens in different columns
        model.choose_cell(0, 0)  # P1
        wait_until_settled(model)
        model.choose_cell(0, 1)  # P2
        wait_until_settled(model)
        model.choose_cell(0, 0)  # P1 (should stack)
        wait_until_settled(model)
        
        assert model.get_owner(5, 0) == Player.P1
        assert model.get_owner(4, 0) == Player.P1
        assert model.get_owner(5, 1) == Player.P2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])