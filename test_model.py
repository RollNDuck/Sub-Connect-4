from common_types import Player
from model import (TicTacToeWinCondition, NotConnectFourWinCondition, FloatingTokenPhysics,
    StrongGravityTokenPhysics, WeakGravityTokenPhysics, ConnectTacToeModel,
)

class TestTicTacToeWinCondition:
    def test_TicTacToeRow(self) -> None:
        win_condition = TicTacToeWinCondition()
        grid: list[list[None | Player]] = [[None for _ in range(3)] for _ in range (3)]
        grid[0] = [Player.P1, Player.P1, Player.P1]

        assert win_condition.is_winner(grid) == Player.P1
        assert win_condition.did_both_win(grid) == (True, False)
        assert win_condition._did_player_win(grid, Player.P1) #type: ignore

    def test_TicTacToeCol(self) -> None:
        win_condition = TicTacToeWinCondition()
        grid: list[list[None | Player]] = [[None for _ in range(3)] for _ in range (3)]
        grid[0][2] = Player.P2
        grid[1][2] = Player.P2
        grid[2][2] = Player.P2

        assert win_condition.is_winner(grid) == Player.P2
        assert win_condition.did_both_win(grid) == (False, True)
        assert not win_condition._did_player_win(grid, Player.P1) #type: ignore

    def test_TicTacToe_no_win(self) -> None:
        win_condition = TicTacToeWinCondition()
        grid: list[list[None | Player]] = [[None for _ in range(3)] for _ in range (3)]

        assert win_condition.is_winner(grid) is None

    def test_TicTacToe_both_win(self) -> None:
        win_condition = TicTacToeWinCondition()
        grid: list[list[None | Player]] = [[None for _ in range(3)] for _ in range (3)]
        grid[0][2] = Player.P2
        grid[1][2] = Player.P2
        grid[2][2] = Player.P2
        grid[0][1] = Player.P1
        grid[1][1] = Player.P1
        grid[2][1] = Player.P1

        assert win_condition.is_winner(grid) is None

class TestNotConnectFourWin:
    def test_notconnectfourow(self) -> None:
        win_condition = NotConnectFourWinCondition()
        grid: list[list[None | Player]] = [[None for _ in range(4)] for _ in range (4)]
        grid[0] = [Player.P1, Player.P1, Player.P1, Player.P1]

        assert win_condition.is_winner(grid) == Player.P1
        assert win_condition.did_both_win(grid) == (True, False)
        assert win_condition._did_player_win(grid, Player.P1) #type: ignore

    def test_notconnectfourcol(self) -> None:
        win_condition = NotConnectFourWinCondition()
        grid: list[list[None | Player]] = [[None for _ in range(4)] for _ in range (4)]
        grid[0][2] = Player.P2
        grid[1][2] = Player.P2
        grid[2][2] = Player.P2
        grid[3][2] = Player.P2

        assert win_condition.is_winner(grid) == Player.P2
        assert win_condition.did_both_win(grid) == (False, True)
        assert not win_condition._did_player_win(grid, Player.P1) #type: ignore

    def test_notconnectfour_no_winner(self) -> None:
        win_condition = NotConnectFourWinCondition()
        grid: list[list[None | Player]] = [[None for _ in range(4)] for _ in range (4)]

        assert win_condition.is_winner(grid) is None

    def test_notconnectfour_both_win(self) -> None:
        win_condition = NotConnectFourWinCondition()
        grid: list[list[None | Player]] = [[None for _ in range(4)] for _ in range (4)]
        grid[0][2] = Player.P2
        grid[1][2] = Player.P2
        grid[2][2] = Player.P2
        grid[3][2] = Player.P2

        grid[0][1] = Player.P1
        grid[1][1] = Player.P1
        grid[2][1] = Player.P1
        grid[3][1] = Player.P1

        assert win_condition.is_winner(grid) is None

class TestTokenPhysics:
    def test_floating_token_physics(self) -> None:
        token_physics = FloatingTokenPhysics()
        token_physics.apply_physics([])
        assert not token_physics.is_falling()
        token_physics.token_falling([])

    def test_strong_gravity_token_physics(self) -> None:
        token_physics = StrongGravityTokenPhysics()
        grid: list[list[None | Player]]= [[None for _ in range(2)] for _ in range(2)]
        grid[0][0] = Player.P1

        token_physics.apply_physics(grid)
        assert token_physics.is_falling()
        token_physics.token_falling(grid)
        assert grid[1][0] == Player.P1
        token_physics.token_falling(grid)
        assert not token_physics.is_falling()

    def test_weak_gravity_token_physics(self) -> None:
        token_physics = WeakGravityTokenPhysics()
        grid: list[list[None | Player]]= [[None for _ in range(3)] for _ in range(3)]
        grid[0][0] = Player.P1
        grid[2][0] = Player.P2

        token_physics.apply_physics(grid)
        assert token_physics.is_falling()
        token_physics.token_falling(grid)
        assert grid[1][0] == Player.P1
        assert grid[2][0] == Player.P2
        assert not token_physics.is_falling()

class TestConnectTacToeModel:
    def test_model_init(self) -> None:
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        assert model.row_count == 6
        assert model.col_count == 7
        assert model.current_player == Player.P1
        assert model.winner is None
        assert not model.is_game_done
        assert model.get_grid == [[None for _ in range(7)] for _ in range(6)]
        assert not model.both_players_won
        assert not model.is_grid_full(model.get_grid)

    def test_model_choose_cell(self) -> None:
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        assert model.choose_cell(0, 0)
        assert model.get_owner(0, 0) == Player.P1
        assert model.current_player == Player.P2
        assert not model.is_game_done

    def test_model_choose_occupied_cell(self) -> None:
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        assert model.choose_cell(0, 0)
        assert not model.choose_cell(0, 0)
    
    def test_model_grid_full(self) -> None:
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        grid: list[list[Player | None]] = [[Player.P1 for _ in range(7)] for _ in range(6)]
        assert model.is_grid_full(grid)

    def test_model_both_win(self) -> None:
        model = ConnectTacToeModel(TicTacToeWinCondition(), FloatingTokenPhysics())
        grid: list[list[None | Player]] = [[None for _ in range(7)] for _ in range(6)]
        grid[1] = [Player.P1 for _ in range(7)]
        grid[0] = [Player.P2 for _ in range(7)]
        
        model._grid = grid #type: ignore
        model._turn_ended() #type: ignore

        assert model.both_players_won
        assert model.winner is None

    def test_model_physics(self) -> None:
        win_condition = TicTacToeWinCondition()
        token_physics = StrongGravityTokenPhysics()
        model = ConnectTacToeModel(win_condition, token_physics)
        model._grid = [[None for _ in range(7)] for _ in range(6)] #type: ignore
        model._grid[0][0] = Player.P1 #type: ignore
        token_physics.apply_physics(model._grid) #type: ignore
        
        assert token_physics.is_falling()
        assert not model.choose_cell(0, 3)

        model._turn_end = True #type: ignore
        
        while model.is_falling:
            model.token_physics()

        assert not model.is_falling
        assert not model._turn_end #type: ignore

    def test_choose_cell_out_bounds(self) -> None:
        win_condition = TicTacToeWinCondition()
        token_physics = StrongGravityTokenPhysics()
        model = ConnectTacToeModel(win_condition, token_physics)
        assert not model.choose_cell(-1, -1)

    def test_choose_cell_falling(self) -> None:
        win_condition = TicTacToeWinCondition()
        token_physics = StrongGravityTokenPhysics()
        model = ConnectTacToeModel(win_condition, token_physics)
        model._grid = [[None for _ in range(7)] for _ in range(6)] #type: ignore
        model._grid[1][0] = None #type: ignore
        model.choose_cell(0, 0)

        assert model._turn_end #type: ignore
        assert token_physics.is_falling()

    def test_turn_ended_p1_wins(self) -> None:
        win_condition = TicTacToeWinCondition()
        token_physics = StrongGravityTokenPhysics()
        model = ConnectTacToeModel(win_condition, token_physics)
        model._grid = [[Player.P1 for _ in range(7)] for _ in range(6)] #type: ignore
        model._turn_ended() #type: ignore

        assert model.winner == Player.P1
        assert model.is_game_done

    def test_turn_ended_p2_wins(self) -> None:
        win_condition = TicTacToeWinCondition()
        token_physics = FloatingTokenPhysics()
        model = ConnectTacToeModel(win_condition, token_physics)
        model._grid = [[None for _ in range(7)] for _ in range(6)] #type: ignore
        model._grid[0] = [Player.P2 for _ in range(7)] #type: ignore
        model._turn_ended() #type: ignore

        assert model.winner == Player.P2
        assert model.is_game_done

    def test_turn_ended_grid_full(self) -> None:
        win_condition = TicTacToeWinCondition()
        token_physics = FloatingTokenPhysics()
        model = ConnectTacToeModel(win_condition, token_physics)
        model._grid = [["Hello" for _ in range(7)] for _ in range(6)] #type: ignore
        model._turn_ended() #type: ignore

        assert model.is_game_done

    def test_turn_ended_switch(self) -> None:
        win_condition = TicTacToeWinCondition()
        token_physics = FloatingTokenPhysics()
        model = ConnectTacToeModel(win_condition, token_physics)
        model._grid = [[None for _ in range(7)] for _ in range(6)] #type: ignore

        model._current_player = Player.P2 #type: ignore
        model._turn_ended() #type: ignore

        assert model.current_player == Player.P1