from common_types import Player
from model import ConnectTacToeModel
from view import ConnectTacToeView

class ConnectTacToeController:
    def __init__(self, model: ConnectTacToeModel, view: ConnectTacToeView) -> None:
        self._model: ConnectTacToeModel = model
        self._view: ConnectTacToeView = view
        self._frame_count: int = 0
        self._frames: int = 10

    def start(self) -> None:
        view: ConnectTacToeView = self._view
        view.start_game(self.update, self.draw)

    def update(self) -> None:
        if self._model.is_falling:
            self._frame_count += 1
            if self._frame_count >= self._frames:
                self._frame_count = 0
                self._model.token_physics()
            return

        if self._model.is_game_done:
            return

        clicked_cell: tuple[int, int] | None = self._view.get_mouse_click()

        if clicked_cell is not None:
            row: int = clicked_cell[0]
            col: int = clicked_cell[1]
            self._model.choose_cell(row, col)

    def draw(self) -> None:
        view: ConnectTacToeView = self._view
        model: ConnectTacToeModel = self._model
        grid: list[list[Player | None]] = self._model.get_grid
    
        view.clear_screen()
        view.draw_grid(grid)

        if not model.is_game_done:  # current player turn message
            view.draw_turn_message(model.current_player)

        elif model.both_players_won:  # both players win at the same time
            view.draw_both_winner_message()

        elif model.winner is not None:  # one single winner
            view.draw_winner_message(model.winner)

        else: # grid is full but no winner
            view.draw_no_winner_message()
