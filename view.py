import pyxel
from common_types import Player
from typing import Callable

class ConnectTacToeView:
    def __init__(self) -> None:
        self.screen_width: int = 200
        self.screen_height: int = 200

        self.row: int = 6
        self.col: int = 7

        self.cell_size: int = 25
        self.grid_height: int = self.cell_size * self.row
        self.grid_width: int = self.cell_size * self.col

        self.grid_x: int = (200 - self.grid_width) // 2
        self.grid_y: int = (200 - self.grid_height) // 2 + 15

        self.player1_color: int = 2
        self.player2_color: int = 5

        pyxel.init(self.screen_width, self.screen_height)
        pyxel.mouse(True)

    def start_game(self, update: Callable[[], None], draw: Callable[[], None]) -> None:
        pyxel.run(update, draw)

    def draw_game(self, grid: list[list[Player | None]], cur_player: Player, winner: Player | None, game_over: bool, both_won: bool) -> None:
        pyxel.cls(0)
        self.draw_grid(grid)
        self.draw_messages(cur_player, winner, game_over, both_won)

    def draw_grid(self, grid: list[list[Player | None]]) -> None:
        for row in range(self.row):
            for col in range(self.col):
                x: int = self.grid_x + (col * self.cell_size)
                y: int = self.grid_y + (row * self.cell_size)

                pyxel.rectb(x, y, self.cell_size, self.cell_size, 10)

                player_token: Player | None = grid[row][col]
                if player_token is not None:
                    self._draw_token(x, y, player_token)

    def _draw_token(self, x: int, y: int, player_token: Player) -> None:
        middle_x: float = self.cell_size / 2 + x
        middle_y: float = self.cell_size / 2 + y
        radius: float = self.cell_size / 3
        player_color: int = self._cur_player_color(player_token)
        pyxel.circ(middle_x, middle_y, radius, player_color)

    def _cur_player_color(self, player: Player) -> int:
        if player == Player.P1:
            return self.player1_color
        else:
            return self.player2_color

    def get_mouse_click(self) -> tuple[int, int] | None:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            clicked_x: int = pyxel.mouse_x
            clicked_y: int = pyxel.mouse_y

            if self._in_grid(clicked_x, clicked_y):
                row: int = (clicked_y - self.grid_y) // self.cell_size
                col: int = (clicked_x - self.grid_x) // self.cell_size
                return (row, col)

        return None

    def _in_grid(self, x: int, y: int) -> bool:
        return (self.grid_x <= x <= self.grid_x + self.grid_width and
                self.grid_y <= y <= self.grid_y + self.grid_height)

    def draw_messages(self, cur_player: Player, winner: Player | None, game_over: bool, both_won: bool) -> None:
        y_coord: int = 15

        if not game_over:  # current player turn message
            player_color: int = self._cur_player_color(cur_player)
            turn_message: str = f"Your turn, {str(cur_player)}!"
            x_coord: int = (self.screen_width // 2) - len(turn_message) * 2
            pyxel.text(x_coord, y_coord, turn_message, player_color)

        elif both_won:  # Both players won simultaneously
            message: str = "Both players won!"
            x_coord: int = (self.screen_width // 2) - len(message) * 2
            pyxel.text(x_coord, y_coord, message, 10)  # White color

        elif winner is not None:  # Single winner message
            winner_color: int = self._cur_player_color(winner)
            win_message: str = f"The winner is, {str(winner)}!"
            x_coord: int = (self.screen_width // 2) - len(win_message) * 2
            pyxel.text(x_coord, y_coord, win_message, winner_color)

        else:  # Draw - no winner and grid full
            message: str = "No winner!"
            x_coord: int = (self.screen_width // 2) - len(message) * 2
            pyxel.text(x_coord, y_coord, message, 8)  # red/pinkish
