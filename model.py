# model.py - Complete updated version

from common_types import Player
from typing import Protocol

class WinCondition(Protocol):
    def is_winner(self, grid: list[list[Player | None]]) -> Player | None:
        ...

    def check_both_winners(self, grid: list[list[Player | None]]) -> tuple[bool, bool]:
        """Returns (P1_wins, P2_wins) tuple for detecting simultaneous wins."""
        ...

class TokenPhysics(Protocol):
    def apply_physics(self, grid: list[list[Player | None]]) -> None:
        ...

    def is_animating(self) -> bool:
        ...

    def step_animation(self, grid: list[list[Player | None]]) -> None:
        ...

class TicTacToeWinCondition:
    def is_winner(self, grid: list[list[Player | None]]) -> Player | None:
        p1_wins, p2_wins = self.check_both_winners(grid)

        if p1_wins and p2_wins:
            return None  # Both won - handled as special case in model
        elif p1_wins:
            return Player.P1
        elif p2_wins:
            return Player.P2
        else:
            return None

    def check_both_winners(self, grid: list[list[Player | None]]) -> tuple[bool, bool]:
        """Returns (P1_wins, P2_wins) for detecting simultaneous wins."""
        p1_wins: bool = self._check_player_wins(grid, Player.P1)
        p2_wins: bool = self._check_player_wins(grid, Player.P2)
        return (p1_wins, p2_wins)

    def _check_player_wins(self, grid: list[list[Player | None]], player: Player) -> bool:
        """Check if a specific player has won."""
        # Check rows
        for row in range(6):
            count: int = 0
            for col in range(7):
                if grid[row][col] == player:
                    count += 1
            if count == 7:
                return True

        # Check columns
        for col in range(7):
            count: int = 0
            for row in range(6):
                if grid[row][col] == player:
                    count += 1
            if count == 6:
                return True

        return False

class NotConnectFourWinCondition:
    """Win when 4+ tokens form a connected group (edge-adjacent, no diagonals)."""
    def is_winner(self, grid: list[list[Player | None]]) -> Player | None:
        p1_wins, p2_wins = self.check_both_winners(grid)

        if p1_wins and p2_wins:
            return None  # Both won - handled as special case in model
        elif p1_wins:
            return Player.P1
        elif p2_wins:
            return Player.P2
        else:
            return None

    def check_both_winners(self, grid: list[list[Player | None]]) -> tuple[bool, bool]:
        """Returns (P1_wins, P2_wins) for detecting simultaneous wins."""
        p1_wins: bool = self._check_player_wins(grid, Player.P1)
        p2_wins: bool = self._check_player_wins(grid, Player.P2)
        return (p1_wins, p2_wins)

    def _check_player_wins(self, grid: list[list[Player | None]], player: Player) -> bool:
        """Check if a specific player has a winning configuration."""
        rows: int = len(grid)
        cols: int = len(grid[0])
        visited: list[list[bool]] = [[False for _ in range(cols)] for _ in range(rows)]

        for start_row in range(rows):
            for start_col in range(cols):
                if grid[start_row][start_col] == player and not visited[start_row][start_col]:
                    group_size: int = self._bfs_count(grid, visited, start_row, start_col, player, rows, cols)
                    if group_size >= 4:
                        return True

        return False

    def _bfs_count(self, grid: list[list[Player | None]], visited: list[list[bool]],
                   start_row: int, start_col: int, player: Player, rows: int, cols: int) -> int:
        """Count the size of connected component using BFS."""
        queue: list[tuple[int, int]] = [(start_row, start_col)]
        visited[start_row][start_col] = True
        count: int = 0

        # Directions: up, down, left, right (no diagonals)
        directions: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            row, col = queue.pop(0)
            count += 1

            # Check all four cardinal directions
            for dr, dc in directions:
                new_row: int = row + dr
                new_col: int = col + dc

                # Check bounds and if it's the same player and not visited
                if (0 <= new_row < rows and 0 <= new_col < cols and
                    not visited[new_row][new_col] and
                    grid[new_row][new_col] == player):

                    visited[new_row][new_col] = True
                    queue.append((new_row, new_col))

        return count

class FloatingTokenPhysics:
    """Tokens stay where they are placed - no movement."""
    def apply_physics(self, grid: list[list[Player | None]]) -> None:
        pass

    def is_animating(self) -> bool:
        return False

    def step_animation(self, grid: list[list[Player | None]]) -> None:
        pass

class StrongGravityTokenPhysics:
    """Tokens fall to the lowest available row in their column."""
    def __init__(self) -> None:
        self._animating: bool = False

    def apply_physics(self, grid: list[list[Player | None]]) -> None:
        rows: int = len(grid)
        cols: int = len(grid[0])

        can_fall: bool = False
        for col in range(cols):
            for row in range(rows - 1):
                if grid[row][col] is not None:
                    for check_row in range(row + 1, rows):
                        if grid[check_row][col] is None:
                            can_fall = True
                            break
                    if can_fall:
                        break
            if can_fall:
                break

        if can_fall:
            self._animating = True

    def is_animating(self) -> bool:
        return self._animating

    def step_animation(self, grid: list[list[Player | None]]) -> None:
        rows: int = len(grid)
        cols: int = len(grid[0])

        moved: bool = False

        for row in range(rows - 2, -1, -1):
            for col in range(cols):
                if grid[row][col] is not None and grid[row + 1][col] is None:
                    grid[row + 1][col] = grid[row][col]
                    grid[row][col] = None
                    moved = True

        if not moved:
            self._animating = False

class WeakGravityTokenPhysics:
    """All tokens move down one cell simultaneously if possible."""
    def __init__(self) -> None:
        self._animating: bool = False

    def apply_physics(self, grid: list[list[Player | None]]) -> None:
        rows: int = len(grid)
        cols: int = len(grid[0])

        can_fall: bool = False
        for row in range(rows - 1):
            for col in range(cols):
                if grid[row][col] is not None and grid[row + 1][col] is None:
                    can_fall = True
                    break
            if can_fall:
                break

        if can_fall:
            self._animating = True

    def is_animating(self) -> bool:
        return self._animating

    def step_animation(self, grid: list[list[Player | None]]) -> None:
        rows: int = len(grid)
        cols: int = len(grid[0])

        new_grid: list[list[Player | None]] = [[None for _ in range(cols)] for _ in range(rows)]
        moved: bool = False

        for row in range(rows - 1, -1, -1):
            for col in range(cols):
                if grid[row][col] is not None:
                    if row < rows - 1 and grid[row + 1][col] is None:
                        new_grid[row + 1][col] = grid[row][col]
                        moved = True
                    else:
                        new_grid[row][col] = grid[row][col]

        for row in range(rows):
            for col in range(cols):
                grid[row][col] = new_grid[row][col]

        if not moved:
            self._animating = False

class ConnectTacToeModel:
    def __init__(self, win_condition: WinCondition, token_physics: TokenPhysics) -> None:
        self._row_count: int = 6
        self._col_count: int = 7
        self._current_player: Player = Player.P1
        self._winner: Player | None = None
        self._is_game_done: bool = False
        self._grid: list[list[Player | None]] = [[None for _ in range(self._col_count)] for _ in range(self._row_count)]
        self._win_condition: WinCondition = win_condition
        self._token_physics: TokenPhysics = token_physics
        self._pending_turn_end: bool = False
        self._both_players_won: bool = False

    @property
    def current_player(self) -> Player:
        return self._current_player

    @property
    def winner(self) -> Player | None:
        return self._winner

    @property
    def is_game_done(self) -> bool:
        return self._is_game_done

    @property
    def both_players_won(self) -> bool:
        """Returns True if both players won simultaneously."""
        return self._both_players_won

    @property
    def is_animating(self) -> bool:
        return self._token_physics.is_animating()

    def step_physics(self) -> None:
        """Step the physics animation forward one frame."""
        if self._token_physics.is_animating():
            self._token_physics.step_animation(self._grid)

            # When animation finishes, check win condition and end turn
            if not self._token_physics.is_animating() and self._pending_turn_end:
                self._finish_turn()

    def choose_cell(self, row: int, col: int) -> bool:
        if self.is_game_done or self.is_animating:
            return False
        if row < 0 or row >= self._row_count or col < 0 or col >= self._col_count:
            return False
        if self._grid[row][col] is not None:
            return False

        # Place token on grid
        self._grid[row][col] = self._current_player

        # Apply physics (may start animation)
        self._token_physics.apply_physics(self._grid)

        # IMPORTANT: Win condition is checked ONLY after physics complete
        # If animating, defer win check and turn end until animation finishes
        if self._token_physics.is_animating():
            self._pending_turn_end = True
        else:
            # No animation needed, check win condition immediately
            self._finish_turn()

        return True

    def _finish_turn(self) -> None:
        """Check win condition and switch players.

        This is ONLY called after token physics have been fully applied.
        """
        self._pending_turn_end = False

        # Check for simultaneous wins first
        p1_wins, p2_wins = self._win_condition.check_both_winners(self._grid)

        if p1_wins and p2_wins:
            # Both players won simultaneously
            self._both_players_won = True
            self._is_game_done = True
            self._winner = None  # No single winner
        elif p1_wins:
            self._winner = Player.P1
            self._is_game_done = True
        elif p2_wins:
            self._winner = Player.P2
            self._is_game_done = True
        elif self.is_grid_full(self._grid):
            # Draw - no winner and grid is full
            self._is_game_done = True
        else:
            # Switch to other player
            if self._current_player == Player.P1:
                self._current_player = Player.P2
            else:
                self._current_player = Player.P1

    def is_grid_full(self, grid: list[list[Player | None]]) -> bool:
        for row in range(self._row_count):
            for col in range(self._col_count):
                if grid[row][col] is None:
                    return False
        return True

    @property
    def row_count(self) -> int:
        return self._row_count

    @property
    def col_count(self) -> int:
        return self._col_count

    def get_owner(self, row: int, col: int) -> Player | None:
        return self._grid[row][col]

    @property
    def get_grid(self) -> list[list[Player | None]]:
        return self._grid