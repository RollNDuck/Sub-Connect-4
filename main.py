from argparse import ArgumentParser

from common_types import WinConditionType, TokenPhysicsType
from view import ConnectTacToeView
from controller import ConnectTacToeController
from tester import make

if __name__ == "__main__":
    parser = ArgumentParser(description="Connect-Tac-Toe Game")
    parser.add_argument(
        "-w",
        choices=["notconnectfour", "tictactoe"],
        required=True,
        help="Win condition: 'notconnectfour' or 'tictactoe'"
    )
    parser.add_argument(
        "-p",
        choices=["floating", "strong", "weak"],
        required=True,
        help="Token physics: 'floating', 'strong', or 'weak'"
    )
    args = parser.parse_args()

    win_condition_type: WinConditionType
    match args.w:
        case "notconnectfour":
            win_condition_type = WinConditionType.NOT_CONNECT_FOUR
        case "tictactoe":
            win_condition_type = WinConditionType.TIC_TAC_TOE
        case _:
            raise ValueError(f"Invalid win condition: {args.w}")

    token_physics_type: TokenPhysicsType
    match args.p:
        case "floating":
            token_physics_type = TokenPhysicsType.FLOATING
        case "strong":
            token_physics_type = TokenPhysicsType.STRONG_GRAVITY
        case "weak":
            token_physics_type = TokenPhysicsType.WEAK_GRAVITY
        case _:
            raise ValueError(f"Invalid physics type: {args.p}")

    model = make(win_condition_type, token_physics_type)
    view = ConnectTacToeView()
    controller = ConnectTacToeController(model, view)

    controller.start()
