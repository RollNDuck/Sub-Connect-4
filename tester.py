from model import ConnectTacToeModel, StrongGravityTokenPhysics, WeakGravityTokenPhysics, FloatingTokenPhysics, TicTacToeWinCondition, NotConnectFourWinCondition, WinCondition, TokenPhysics
from common_types import WinConditionType, TokenPhysicsType

def make(win_condition_type: WinConditionType, token_physics_type: TokenPhysicsType) -> ConnectTacToeModel:
    win_condition: WinCondition
    match win_condition_type:
        case WinConditionType.NOT_CONNECT_FOUR:
            win_condition = NotConnectFourWinCondition()
        case WinConditionType.TIC_TAC_TOE:
            win_condition = TicTacToeWinCondition()
        case _:
            raise ValueError("Invalid Win Condition Type")

    token_physics: TokenPhysics
    match token_physics_type:
        case TokenPhysicsType.WEAK_GRAVITY:
            token_physics = WeakGravityTokenPhysics()
        case TokenPhysicsType.STRONG_GRAVITY:
            token_physics = StrongGravityTokenPhysics()
        case TokenPhysicsType.FLOATING:
            token_physics = FloatingTokenPhysics()
        case _:
            raise ValueError("Invalid Token Physics Type")

    return ConnectTacToeModel(win_condition, token_physics)
