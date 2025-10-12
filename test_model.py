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
        for col in range(7):
            set_grid_cell(grid, 0, col, Player.P1)
        for row in range(6):
            set_grid_cell(grid, row, 6, Player.P2)
        assert win_cond.is_winner(grid) is None
        p1_wins, p2_wins = win_cond.check_both_winners(grid)
        assert p1_wins and p2_wins


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
        for col in range(7):
            model._grid[3][col] = Player.P1
        model._finish_turn()
        assert model.winner == Player.P1
        assert model.is_game_done

    def test_win_notconnectfour(self) -> None:
        """Test Not-Connect-Four win."""
        model = ConnectTacToeModel(NotConnectFourWinCondition(), FloatingTokenPhysics())
        for row in range(4):
            model._grid[row][2] = Player.P1
        model._finish_turn()
        assert model.winner == Player.P1
        assert model.is_game_done

    def test_both_players_win(self) -> None:
        """Test both players winning simultaneously."""
        model = ConnectTacToeModel(NotConnectFourWinCondition(), FloatingTokenPhysics())
        for row in range(4):
            model._grid[row][0] = Player.P1
            model._grid[row][6] = Player.P2
        model._finish_turn()
        assert model.both_players_won
        assert model.winner is None
        assert model.is_game_done

    def test_draw_detection(self) -> None:
        """Test draw when grid full."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        for row in range(6):
            for col in range(7):
                model._grid[row][col] = Player.P1 if (row + col) % 2 == 0 else Player.P2
        model._finish_turn()
        assert model.winner is None
        assert model.is_game_done

    def test_no_moves_after_game_done(self) -> None:
        """Test moves rejected after game ends."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        model._is_game_done = True
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
        for i in range(7):
            if model.is_game_done:
                break
            model.choose_cell(0, 2 if i < 4 else 0)
            wait_until_settled(model)
        assert model.winner == Player.P1

    def test_weak_gravity_cascading(self) -> None:
        """Test cascading with weak gravity."""
        model = ConnectTacToeModel(TicTacToeWinCondition(), WeakGravityTokenPhysics())
        for col in range(7):
            model._grid[0][col] = Player.P1
        model._token_physics.apply_physics(model._grid)
        for _ in range(6):
            if model._token_physics.is_animating():
                model._token_physics.step_animation(model._grid)
                model._token_physics.apply_physics(model._grid)
        model._finish_turn()
        assert model.winner == Player.P1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])