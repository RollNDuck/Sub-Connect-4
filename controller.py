from common_types import Player
from model import ConnectTacToeModel
from view import ConnectTacToeView

class ConnectTacToeController:
    def __init__(self, model: ConnectTacToeModel, view: ConnectTacToeView) -> None:
        self._model: ConnectTacToeModel = model
        self._view: ConnectTacToeView = view
        self._frame_count: int = 0
        self._animation_speed: int = 10  # Frames between physics steps (lower = faster)

    def start(self) -> None:
        view: ConnectTacToeView = self._view
        view.start_game(self.update, self.draw)

    def update(self) -> None:
        # Always step physics animation if active
        if self._model.is_animating:
            self._frame_count += 1
            if self._frame_count >= self._animation_speed:
                self._frame_count = 0
                self._model.step_physics()
            return  # Don't accept input during animation

        # Only accept input if game is not done and not animating
        if self._model.is_game_done:
            return

        clicked_cell: tuple[int, int] | None = self._view.get_mouse_click()

        if clicked_cell is not None:
            row: int = clicked_cell[0]
            col: int = clicked_cell[1]
            self._model.choose_cell(row, col)

    def draw(self) -> None:
        grid: list[list[Player | None]] = self._model.get_grid
        self._view.draw_game(
            grid,
            self._model.current_player,
            self._model.winner,
            self._model.is_game_done,
            self._model.both_players_won
        )
