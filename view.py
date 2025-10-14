import pyxel
from common_types import Player
from typing import Callable

class ConnectTacToeView:
    def __init__(self) -> None:
        #screen settings
        self.screen_width: int = 200
        self.screen_height: int = 200

        #number of rows and columns of grid
        self.row: int = 6
        self.col: int = 7

        #size of cell in grid
        self.cell_size: int = 25

        #size of grid
        self.grid_height: int = self.cell_size * self.row
        self.grid_width: int = self.cell_size * self.col

        #position of grid (centered)
        self.grid_x: int = (200 - self.grid_width) // 2
        self.grid_y: int = (200 - self.grid_height) // 2 + 15

        #color of players
        self.player1_color: int = 7
        self.player2_color: int = 9

        pyxel.init(self.screen_width, self.screen_height)
        pyxel.mouse(True)
        pyxel.load('subconnectfour.pyxres')

    def start_game(self, update: Callable[[], None], draw: Callable[[], None]) -> None:
        pyxel.run(update, draw)

    def clear_screen(self) -> None:
        pyxel.cls(0)

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
        # choose which sprite to draw depending on player
        if player_token == Player.P1:
            # source coordinates and size in the .pyxres image bank
            u, v, w, h = 0, 0, 16, 16   # adjust based on your token’s position and size
            img_bank = 0                # usually 0 if you saved in the first image bank
        else:
            u, v, w, h = 24, 0, 16, 16  # second token image
            img_bank = 0

        # compute where to place it (centered in the grid cell)
        draw_x = x + (self.cell_size - w) // 2
        draw_y = y + (self.cell_size - h) // 2

        pyxel.blt(draw_x, draw_y, img_bank, u, v, w, h, colkey=0)

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

    def draw_turn_message(self, cur_player: Player, y_coord: int = 15) -> None:
        player_color: int = self._cur_player_color(cur_player)
        turn_message: str = f"Your turn, {str(cur_player)}!"
        x_coord: int = (self.screen_width // 2) - len(turn_message) * 2
        pyxel.text(x_coord, y_coord, turn_message, player_color)

    def draw_both_winner_message(self, y_coord: int = 15) -> None:
        message: str = "Both players won!"
        x_coord: int = (self.screen_width // 2) - len(message) * 2
        pyxel.text(x_coord, y_coord, message, 10)  # white color

    def draw_winner_message(self, winner: Player, y_coord: int = 15) -> None:
        winner_color: int = self._cur_player_color(winner)
        win_message: str = f"The winner is, {str(winner)}!"
        x_coord: int = (self.screen_width // 2) - len(win_message) * 2
        pyxel.text(x_coord, y_coord, win_message, winner_color)

    def draw_no_winner_message(self, y_coord: int = 15) -> None:
        message: str = "No winner!"
        x_coord: int = (self.screen_width // 2) - len(message) * 2
        pyxel.text(x_coord, y_coord, message, 8)  # red/pinkish
