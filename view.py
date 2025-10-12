import pyxel
from common_types import Player
from typing import Callable

class ConnectTacToeView:
    """
    View component for Connect-Tac-Toe game using Pyxel.

    Handles all visual rendering, user input, and display logic.
    """
    def __init__(self) -> None:
        self.screen_width: int = 200
        self.screen_height: int = 200

        self.row: int = 6
        self.col: int = 7

        # Calculate optimal cell size for better visual appearance
        self.cell_size: int = 24  # Slightly smaller for better fit
        self.grid_height: int = self.cell_size * self.row
        self.grid_width: int = self.cell_size * self.col

        # Perfect centering calculations
        self.grid_x: int = (self.screen_width - self.grid_width) // 2
        self.grid_y: int = (self.screen_height - self.grid_height) // 2 + 20  # More space for text

        # High contrast colors for better visibility
        self.player1_color: int = 11  # Bright yellow - highly visible
        self.player2_color: int = 8   # Bright red - highly visible
        self.border_color: int = 7    # White borders for clarity
        self.background_color: int = 0 # Black background

        pyxel.init(self.screen_width, self.screen_height, title="Connect-Tac-Toe")
        pyxel.mouse(True)

    def start_game(self, update: Callable[[], None], draw: Callable[[], None]) -> None:
        """Start the Pyxel game loop with the provided update and draw functions."""
        pyxel.run(update, draw)

    def draw_game(self, grid: list[list[Player | None]], cur_player: Player, winner: Player | None, game_over: bool, both_won: bool) -> None:
        """Draw the complete game state including grid and messages."""
        pyxel.cls(self.background_color)
        self.draw_grid(grid)
        self.draw_messages(cur_player, winner, game_over, both_won)

    def draw_grid(self, grid: list[list[Player | None]]) -> None:
        """Draw the game grid with borders and tokens."""
        for row in range(self.row):
            for col in range(self.col):
                x: int = self.grid_x + (col * self.cell_size)
                y: int = self.grid_y + (row * self.cell_size)

                # Draw cell border with high contrast
                pyxel.rectb(x, y, self.cell_size, self.cell_size, self.border_color)

                # Draw token if present
                player_token: Player | None = grid[row][col]
                if player_token is not None:
                    self._draw_token(x, y, player_token)

    def _draw_token(self, x: int, y: int, player_token: Player) -> None:
        """Draw a player token in the specified cell."""
        middle_x: float = self.cell_size / 2 + x
        middle_y: float = self.cell_size / 2 + y
        radius: float = self.cell_size / 3
        player_color: int = self._cur_player_color(player_token)
        pyxel.circ(middle_x, middle_y, radius, player_color)

    def _cur_player_color(self, player: Player) -> int:
        """Get the color associated with a player."""
        if player == Player.P1:
            return self.player1_color
        else:
            return self.player2_color

    def get_mouse_click(self) -> tuple[int, int] | None:
        """Get mouse click coordinates if within the grid, None otherwise."""
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            clicked_x: int = pyxel.mouse_x
            clicked_y: int = pyxel.mouse_y

            if self._in_grid(clicked_x, clicked_y):
                row: int = (clicked_y - self.grid_y) // self.cell_size
                col: int = (clicked_x - self.grid_x) // self.cell_size
                # Validate bounds to prevent index errors
                if 0 <= row < self.row and 0 <= col < self.col:
                    return (row, col)

        return None

    def _in_grid(self, x: int, y: int) -> bool:
        """Check if coordinates are within the game grid boundaries."""
        return (self.grid_x <= x <= self.grid_x + self.grid_width and
                self.grid_y <= y <= self.grid_y + self.grid_height)

    def draw_messages(self, cur_player: Player, winner: Player | None, game_over: bool, both_won: bool) -> None:
        """Draw game status messages with proper centering and colors."""
        y_coord: int = 10  # Positioned above the grid

        if not game_over:  # Current player turn message
            player_color: int = self._cur_player_color(cur_player)
            turn_message: str = f"Player {cur_player.name}'s turn"
            turn_x_coord: int = self._center_text(turn_message)
            pyxel.text(turn_x_coord, y_coord, turn_message, player_color)

        elif both_won:  # Both players won simultaneously
            both_won_message: str = "Both players won!"
            both_won_x_coord: int = self._center_text(both_won_message)
            pyxel.text(both_won_x_coord, y_coord, both_won_message, 7)  # White color

        elif winner is not None:  # Single winner message
            winner_color: int = self._cur_player_color(winner)
            win_message: str = f"Player {winner.name} wins!"
            win_x_coord: int = self._center_text(win_message)
            pyxel.text(win_x_coord, y_coord, win_message, winner_color)

        else:  # Draw - no winner and grid full
            draw_message: str = "Draw - No winner!"
            draw_x_coord: int = self._center_text(draw_message)
            pyxel.text(draw_x_coord, y_coord, draw_message, 8)  # Red color

    def _center_text(self, text: str) -> int:
        """Calculate x-coordinate to center text on screen."""
        # Pyxel text is 4 pixels wide per character
        text_width: int = len(text) * 4
        return (self.screen_width - text_width) // 2
