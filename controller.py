from common_types import Player
from model import ConnectTacToeModel
from view import ConnectTacToeView

class ConnectTacToeController:
    """
    Controller component for Connect-Tac-Toe game.

    Handles user input, coordinates between model and view, and manages game flow.
    """
    def __init__(self, model: ConnectTacToeModel, view: ConnectTacToeView) -> None:
        """
        Initialize the controller.

        Args:
            model: The game model to control
            view: The view to update
        """
        if model is None:
            raise ValueError("Model cannot be None")
        if view is None:
            raise ValueError("View cannot be None")

        self._model: ConnectTacToeModel = model
        self._view: ConnectTacToeView = view
        self._frame_count: int = 0
        self._animation_speed: int = 8  # Frames between physics steps (lower = faster)
        self._last_click_time: int = 0  # Track click timing to prevent rapid clicks

    def start(self) -> None:
        """Start the game loop."""
        self._view.start_game(self.update, self.draw)

    def update(self) -> None:
        """Update game state - handle physics animation and user input."""
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

        # Handle mouse clicks with debouncing
        clicked_cell: tuple[int, int] | None = self._view.get_mouse_click()
        if clicked_cell is not None:
            # Simple debouncing to prevent rapid clicks
            import pyxel
            current_time = pyxel.frame_count
            if current_time - self._last_click_time > 5:  # 5 frame delay
                self._last_click_time = current_time
                row: int = clicked_cell[0]
                col: int = clicked_cell[1]
                success = self._model.choose_cell(row, col)
                # Could add visual feedback here for invalid moves

    def draw(self) -> None:
        """Draw the current game state."""
        grid: list[list[Player | None]] = self._model.get_grid
        self._view.draw_game(
            grid,
            self._model.current_player,
            self._model.winner,
            self._model.is_game_done,
            self._model.both_players_won
        )
