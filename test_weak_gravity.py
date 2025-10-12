#!/usr/bin/env python3

from tester import make
from common_types import WinConditionType, TokenPhysicsType, Player

def test_weak_gravity():
    """Test weak gravity behavior step by step."""
    print("Testing Weak Gravity Token Physics")
    print("=" * 50)
    
    # Create a game with weak gravity
    game = make(WinConditionType.TIC_TAC_TOE, TokenPhysicsType.WEAK_GRAVITY)
    
    def print_grid():
        print("Current grid:")
        for row in range(game.row_count):
            row_str = ""
            for col in range(game.col_count):
                owner = game.get_owner(row, col)
                if owner == Player.P1:
                    row_str += "P1 "
                elif owner == Player.P2:
                    row_str += "P2 "
                else:
                    row_str += ".. "
            print(f"Row {row}: {row_str}")
        print()
    
    print("Initial state:")
    print_grid()
    
    # Place a token in row 0, col 0
    print("Placing P1 token at (0,0)...")
    result = game.choose_cell(0, 0)
    print(f"Placement result: {result}")
    print(f"Current player: {game.current_player}")
    print(f"Is animating: {game.is_animating}")
    print_grid()
    
    # Step through animation
    if game.is_animating:
        print("Stepping through animation...")
        step = 1
        while game.is_animating:
            print(f"Animation step {step}:")
            game.step_physics()
            print_grid()
            step += 1
            if step > 10:  # Safety break
                print("Animation took too long, breaking...")
                break
    
    print("Final state after animation:")
    print(f"Current player: {game.current_player}")
    print(f"Is game done: {game.is_game_done}")
    print(f"Winner: {game.winner}")
    print_grid()

if __name__ == "__main__":
    test_weak_gravity()
