from common_types import Player
from typing import Protocol

class WinCondition(Protocol):
    def is_winner(self, grid: list[list[Player | None]]) -> Player | None:
        ...

    def did_both_win(self, grid: list[list[Player | None]]) -> tuple[bool, bool]:
        ...

class TokenPhysics(Protocol):
    def apply_physics(self, grid: list[list[Player | None]]) -> None:
        ...

    def is_falling(self) -> bool:
        ...

    def token_falling(self, grid: list[list[Player | None]]) -> None:
        ...

class TicTacToeWinCondition:
    def is_winner(self, grid: list[list[Player | None]]) -> Player | None:
        p1_wins, p2_wins = self.did_both_win(grid)

        if p1_wins and p2_wins:
            return None
        elif p1_wins:
            return Player.P1
        elif p2_wins:
            return Player.P2
        else:
            return None

    def did_both_win(self, grid: list[list[Player | None]]) -> tuple[bool, bool]:
        p1_wins: bool = self._did_player_win(grid, Player.P1)
        p2_wins: bool = self._did_player_win(grid, Player.P2)
        return (p1_wins, p2_wins)

    def _did_player_win(self, grid: list[list[Player | None]], player: Player) -> bool:
        row_count: int = len(grid)
        col_count: int = len(grid[0])
        for row in range(row_count):
            count: int = 0
            for col in range(col_count):
                if grid[row][col] == player:
                    count += 1
            if count == col_count:
                return True

        for col in range(col_count):
            count: int = 0
            for row in range(row_count):
                if grid[row][col] == player:
                    count += 1
            if count == row_count:
                return True

        return False

class NotConnectFourWinCondition:
    def is_winner(self, grid: list[list[Player | None]]) -> Player | None:
        p1_wins, p2_wins = self.did_both_win(grid)

        if p1_wins and p2_wins:
            return None
        elif p1_wins:
            return Player.P1
        elif p2_wins:
            return Player.P2
        else:
            return None

    def did_both_win(self, grid: list[list[Player | None]]) -> tuple[bool, bool]:
        p1_wins: bool = self._did_player_win(grid, Player.P1)
        p2_wins: bool = self._did_player_win(grid, Player.P2)
        return (p1_wins, p2_wins)

    def _did_player_win(self, grid: list[list[Player | None]], player: Player) -> bool:
        rows: int = len(grid)
        cols: int = len(grid[0])
        visited: list[list[bool]] = [[False for _ in range(cols)] for _ in range(rows)]

        for start_row in range(rows):
            for start_col in range(cols):
                if grid[start_row][start_col] == player and not visited[start_row][start_col]:
                    group_size: int = self._breadthfs_count(grid, visited, start_row, start_col, player, rows, cols)
                    if group_size >= 4:
                        return True

        return False

    def _breadthfs_count(self, grid: list[list[Player | None]], visited: list[list[bool]], start_row: int, start_col: int, player: Player, rows: int, cols: int) -> int:
        queue: list[tuple[int, int]] = [(start_row, start_col)]
        visited[start_row][start_col] = True
        count: int = 0
        directions: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            row, col = queue.pop(0)
            count += 1
            for dr, dc in directions:
                new_row: int = row + dr
                new_col: int = col + dc
                if (0 <= new_row < rows and 0 <= new_col < cols and
                    not visited[new_row][new_col] and
                    grid[new_row][new_col] == player):

                    visited[new_row][new_col] = True
                    queue.append((new_row, new_col))

        return count

class FloatingTokenPhysics:
    def apply_physics(self, grid: list[list[Player | None]]) -> None:
        pass

    def is_falling(self) -> bool:
        return False

    def token_falling(self, grid: list[list[Player | None]]) -> None:
        pass

class StrongGravityTokenPhysics:
    def __init__(self) -> None:
        self._is_falling: bool = False

    def apply_physics(self, grid: list[list[Player | None]]) -> None:
        rows: int = len(grid)
        cols: int = len(grid[0])
        can_fall: bool = False

        for col in range(cols):
            for row in range(rows - 1):
                if grid[row][col] is not None and grid[row + 1][col] is None:
                    can_fall = True
                    break
            if can_fall:
                break
        if can_fall:
            self._is_falling = True

    def is_falling(self) -> bool:
        return self._is_falling

    def token_falling(self, grid: list[list[Player | None]]) -> None:
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
            self._is_falling = False

class WeakGravityTokenPhysics:
    def __init__(self) -> None:
        self._is_falling: bool = False

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
            self._is_falling = True

    def is_falling(self) -> bool:
        return self._is_falling

    def token_falling(self, grid: list[list[Player | None]]) -> None:
        rows: int = len(grid)
        cols: int = len(grid[0])
        moves: list[tuple[int, int, int, int]] = []

        for col in range(cols):
            occupied_after_move: set[int] = set()
            fixed_tokens: set[tuple[int, int]] = set()

            for row in range(rows - 1, -1, -1):
                if grid[row][col] is not None:
                    if row == rows - 1 or (row + 1, col) in fixed_tokens:
                        fixed_tokens.add((row, col))
                        occupied_after_move.add(row)

            for row in range(rows - 1):
                if grid[row][col] is not None and (row, col) not in fixed_tokens:
                    moves.append((row, col, row + 1, col))
                    occupied_after_move.add(row + 1)
        if moves:
            new_grid: list[list[Player | None]] = [[None for _ in range(cols)] for _ in range(rows)]
            for row in range(rows):
                for col in range(cols):
                    if grid[row][col] is not None:
                        is_moving: bool = False
                        for from_row, from_col, _, _ in moves:
                            if from_row == row and from_col == col:
                                is_moving = True
                                break
                        if not is_moving:
                            new_grid[row][col] = grid[row][col]

            for from_row, from_col, to_row, to_col in moves:
                new_grid[to_row][to_col] = grid[from_row][from_col]

            for row in range(rows):
                for col in range(cols):
                    grid[row][col] = new_grid[row][col]

        self._is_falling = False

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
        self._turn_end: bool = False
        self._did_both_win: bool = False

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
        return self._did_both_win

    @property
    def is_falling(self) -> bool:
        return self._token_physics.is_falling()

    def token_physics(self) -> None:
        if self._token_physics.is_falling():
            self._token_physics.token_falling(self._grid)

            if not self._token_physics.is_falling() and self._turn_end:
                self._turn_ended()

    def choose_cell(self, row: int, col: int) -> bool:
        if self.is_game_done or self.is_falling:
            return False
        if row < 0 or row >= self._row_count or col < 0 or col >= self._col_count:
            return False
        if self._grid[row][col] is not None:
            return False

        self._grid[row][col] = self._current_player

        self._token_physics.apply_physics(self._grid)

        if self._token_physics.is_falling():
            self._turn_end = True
        else:
            self._turn_ended()

        return True

    def _turn_ended(self) -> None:
        self._turn_end = False
        p1_wins, p2_wins = self._win_condition.did_both_win(self._grid)

        if p1_wins and p2_wins:
            self._did_both_win = True
            self._is_game_done = True
            self._winner = None
        elif p1_wins:
            self._winner = Player.P1
            self._is_game_done = True
        elif p2_wins:
            self._winner = Player.P2
            self._is_game_done = True
        elif self.is_grid_full(self._grid):
            self._is_game_done = True
        else:
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
