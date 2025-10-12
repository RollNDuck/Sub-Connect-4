from common_types import Player
from typing import Protocol

class WinCondition(Protocol):
    """Protocol defining the interface for win condition implementations."""
    
    def is_winner(self, grid: list[list[Player | None]]) -> Player | None:
        """Check if there is a winner on the current grid.
        
        Args:
            grid: 2D array representing the game board
            
        Returns:
            Winning player or None if no winner
        """
        ...

    def check_both_winners(self, grid: list[list[Player | None]]) -> tuple[bool, bool]:
        """Check if both players have winning conditions simultaneously.
        
        Args:
            grid: 2D array representing the game board
            
        Returns:
            Tuple of (P1_wins, P2_wins) for detecting simultaneous wins
        """
        ...

class TokenPhysics(Protocol):
    """Protocol defining the interface for token physics implementations."""
    
    def apply_physics(self, grid: list[list[Player | None]]) -> None:
        """Apply physics rules to the grid, potentially starting animation.
        
        Args:
            grid: 2D array representing the game board
        """
        ...

    def is_animating(self) -> bool:
        """Check if physics animation is currently running.
        
        Returns:
            True if animation is in progress, False otherwise
        """
        ...

    def step_animation(self, grid: list[list[Player | None]]) -> None:
        """Advance the physics animation by one step.
        
        Args:
            grid: 2D array representing the game board
        """
        ...

class TicTacToeWinCondition:
    """Win condition where a player wins by filling an entire row or column."""
    
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
            row_count: int = 0
            for col in range(7):
                if grid[row][col] == player:
                    row_count += 1
            if row_count == 7:
                return True

        # Check columns
        for col in range(7):
            col_count: int = 0
            for row in range(6):
                if grid[row][col] == player:
                    col_count += 1
            if col_count == 6:
                return True

        return False

class NotConnectFourWinCondition:
    """Win condition where a player wins by having 4+ tokens in a connected group.
    
    Tokens are connected if they share an edge (no diagonals). Uses BFS to find
    connected components and checks if any component has 4 or more tokens.
    """
    
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
    """Physics implementation where tokens stay exactly where they are placed.
    
    No movement or animation occurs - tokens remain in their original positions.
    """
    
    def apply_physics(self, grid: list[list[Player | None]]) -> None:
        pass

    def is_animating(self) -> bool:
        return False

    def step_animation(self, grid: list[list[Player | None]]) -> None:
        pass

class StrongGravityTokenPhysics:
    """Physics implementation where tokens fall to the lowest available row in their column.
    
    Tokens placed anywhere in a column will fall down to the bottom-most available
    position, similar to Connect Four. Animation occurs step by step until all
    tokens have settled.
    """
    
    def __init__(self) -> None:
        self._animating: bool = False

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
    """Physics implementation where all tokens move down one step simultaneously.
    
    Unlike Strong Gravity, tokens only move one cell down per turn, but all tokens
    move at the same time. This can create cascading effects where tokens continue
    to fall in subsequent turns. Only one step of movement occurs per turn.
    """
    
    def __init__(self) -> None:
        self._animating: bool = False

    def apply_physics(self, grid: list[list[Player | None]]) -> None:
        rows: int = len(grid)
        cols: int = len(grid[0])

        # Check if ANY token can fall
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
        """Move all tokens down one cell simultaneously with proper cascading."""
        rows: int = len(grid)
        cols: int = len(grid[0])

        # We'll use a more efficient approach:
        # For each column, we'll calculate which tokens should move
        moves: list[tuple[int, int, int, int]] = []

        # Process each column independently
        for col in range(cols):
            # For this column, we need to determine which tokens can move
            # We'll use a set to track which rows will have tokens after movement
            occupied_after_move: set[int] = set()

            # First, find all tokens that are fixed (can't move)
            # Tokens in the bottom row or with a token directly below them that can't move
            fixed_tokens: set[tuple[int, int]] = set()

            # Start from the bottom and work up
            for row in range(rows - 1, -1, -1):
                if grid[row][col] is not None:
                    # Check if this token is fixed
                    if row == rows - 1 or (row + 1, col) in fixed_tokens:
                        fixed_tokens.add((row, col))
                        occupied_after_move.add(row)

            # Now, all other tokens will move down one cell
            for row in range(rows - 1):
                if grid[row][col] is not None and (row, col) not in fixed_tokens:
                    # This token can move down
                    moves.append((row, col, row + 1, col))
                    occupied_after_move.add(row + 1)

        # Apply all moves simultaneously
        if moves:
            # Create a new grid state
            new_grid: list[list[Player | None]] = [[None for _ in range(cols)] for _ in range(rows)]

            # First, copy all tokens that aren't moving
            for row in range(rows):
                for col in range(cols):
                    if grid[row][col] is not None:
                        # Check if this token is moving
                        is_moving: bool = False
                        for from_row, from_col, _, _ in moves:
                            if from_row == row and from_col == col:
                                is_moving = True
                                break
                        if not is_moving:
                            new_grid[row][col] = grid[row][col]

            # Then place all moving tokens in their new positions
            for from_row, from_col, to_row, to_col in moves:
                new_grid[to_row][to_col] = grid[from_row][from_col]

            # Update the actual grid
            for row in range(rows):
                for col in range(cols):
                    grid[row][col] = new_grid[row][col]

        # For Weak Gravity, we only do one step of movement per turn
        # So we always stop animating after this step
        self._animating = False

class ConnectTacToeModel:
    """Main model class for the Connect-Tac-Toe game.
    
    Manages game state, turn order, win conditions, and token physics.
    Follows the Open-Closed Principle by accepting win condition and physics
    implementations through dependency injection.
    """
    
    def __init__(self, win_condition: WinCondition, token_physics: TokenPhysics) -> None:
        """Initialize the game model with specified win condition and physics.
        
        Args:
            win_condition: Implementation of win condition rules
            token_physics: Implementation of token movement physics
        """
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
        """Get the current player whose turn it is.
        
        Returns:
            Current player (P1 or P2)
        """
        return self._current_player

    @property
    def winner(self) -> Player | None:
        """Get the winning player if the game has ended.
        
        Returns:
            Winning player or None if no winner (draw or game ongoing)
        """
        return self._winner

    @property
    def is_game_done(self) -> bool:
        """Check if the game has ended.
        
        Returns:
            True if game is over (winner, draw, or both players won)
        """
        return self._is_game_done

    @property
    def both_players_won(self) -> bool:
        """Check if both players won simultaneously.
        
        Returns:
            True if both players achieved winning conditions at the same time
        """
        return self._both_players_won

    @property
    def is_animating(self) -> bool:
        """Check if physics animation is currently running.
        
        Returns:
            True if tokens are currently animating
        """
        return self._token_physics.is_animating()

    def step_physics(self) -> None:
        """Advance the physics animation by one frame.
        
        This method should be called repeatedly during animation to update
        token positions. When animation completes, win conditions are checked
        and the turn ends.
        """
        if self._token_physics.is_animating():
            self._token_physics.step_animation(self._grid)

            # When animation finishes, check win condition and end turn
            if not self._token_physics.is_animating() and self._pending_turn_end:
                self._finish_turn()

    def choose_cell(self, row: int, col: int) -> bool:
        """Place a token in the specified cell if valid.
        
        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            
        Returns:
            True if token was placed successfully, False otherwise
        """
        # Validate game state
        if self.is_game_done:
            return False
        if self.is_animating:
            return False
            
        # Validate coordinates
        if not self._is_valid_coordinate(row, col):
            return False
            
        # Check if cell is occupied
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

    def _is_valid_coordinate(self, row: int, col: int) -> bool:
        """Check if coordinates are within valid bounds.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            True if coordinates are valid
        """
        return (0 <= row < self._row_count and 0 <= col < self._col_count)

    def _finish_turn(self) -> None:
        """Check win condition and switch players.

        This is ONLY called after token physics have been fully applied.
        Handles win detection, draw detection, and player switching.
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
        """Check if the grid is completely filled with tokens.
        
        Args:
            grid: 2D array representing the game board
            
        Returns:
            True if all cells are occupied
        """
        for row in range(self._row_count):
            for col in range(self._col_count):
                if grid[row][col] is None:
                    return False
        return True

    @property
    def row_count(self) -> int:
        """Get the number of rows in the grid.
        
        Returns:
            Number of rows (always 6)
        """
        return self._row_count

    @property
    def col_count(self) -> int:
        """Get the number of columns in the grid.
        
        Returns:
            Number of columns (always 7)
        """
        return self._col_count

    def get_owner(self, row: int, col: int) -> Player | None:
        """Get the owner of a specific cell.
        
        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            
        Returns:
            Player who owns the cell, or None if empty
        """
        return self._grid[row][col]

    @property
    def get_grid(self) -> list[list[Player | None]]:
        """Get a copy of the current game grid.
        
        Returns:
            2D array representing the current game state
        """
        return self._grid
