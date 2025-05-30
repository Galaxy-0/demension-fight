import unittest
import numpy as np
import sys
import os

# Adjust path to import DimensionalFoldingGame from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game_logic import DimensionalFoldingGame

class TestDimensionalFoldingGame(unittest.TestCase):

    def setUp(self):
        """Called before each test method."""
        self.game = DimensionalFoldingGame()

    def assertGridEqual(self, grid1, grid2_list, msg=None):
        """Helper to compare a NumPy grid with a list-of-lists."""
        self.assertEqual(grid1.tolist(), grid2_list, msg)

    def test_initial_state(self):
        self.assertGridEqual(self.game.grid, [[0,0,0],[0,0,0],[0,0,0]], "Grid should be empty initially.")
        self.assertEqual(self.game.current_player, 1, "Player 1 should start.")
        self.assertEqual(self.game.folded_dimension, [0,0,0,0], "No dimensions should be folded initially.")
        self.assertFalse(self.game.game_over, "Game should not be over initially.")
        self.assertIsNone(self.game.winner, "Winner should be None initially.")

    def test_place_piece_valid(self):
        actions = self.game.make_move(grid_index=0)
        self.assertGridEqual(self.game.grid, [[1,0,0],[0,0,0],[0,0,0]], "Piece for P1 should be at (0,0).")
        self.assertEqual(self.game.current_player, 2, "Should be Player 2's turn.")
        self.assertIn("PIECE_PLACED", actions)

    def test_place_piece_invalid_occupied(self):
        self.game.make_move(grid_index=0) # P1 places at 0
        actions = self.game.make_move(grid_index=0) # P2 tries to place at 0
        self.assertGridEqual(self.game.grid, [[1,0,0],[0,0,0],[0,0,0]], "Cell 0 should still contain P1's piece.")
        self.assertEqual(self.game.current_player, 2, "Should still be Player 2's turn as move was invalid.")
        self.assertIn("INVALID_MOVE", actions)

    def test_place_piece_invalid_game_over(self):
        # Setup a win for P1
        self.game.grid = np.array([[1,1,1],[0,0,0],[0,0,0]])
        self.game.check_win_condition() # This will set game_over
        self.assertTrue(self.game.game_over)
        
        actions = self.game.make_move(grid_index=3) # Try to place after game over
        self.assertGridEqual(self.game.grid, [[1,1,1],[0,0,0],[0,0,0]], "Grid should not change after game over.")
        self.assertIn("INVALID_MOVE", actions)

    def test_alternate_turns(self):
        self.game.make_move(0) # P1
        self.assertEqual(self.game.current_player, 2)
        self.game.make_move(1) # P2
        self.assertEqual(self.game.current_player, 1)
        self.game.make_move(2) # P1
        self.assertEqual(self.game.current_player, 2)

    # --- Standard Win Conditions ---
    def test_win_horizontal_player1(self):
        self.game.make_move(0) # P1
        self.game.make_move(3) # P2
        self.game.make_move(1) # P1
        self.game.make_move(4) # P2
        self.game.make_move(2) # P1 wins
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, 1)

    def test_win_vertical_player2(self):
        self.game.make_move(0) # P1
        self.game.make_move(1) # P2
        self.game.make_move(3) # P1
        self.game.make_move(4) # P2
        self.game.make_move(5) # P1
        self.game.make_move(7) # P2 wins (1, 4, 7)
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, 2)

    def test_win_diagonal_player1(self):
        self.game.make_move(0) # P1
        self.game.make_move(1) # P2
        self.game.make_move(4) # P1
        self.game.make_move(2) # P2
        self.game.make_move(8) # P1 wins (0, 4, 8)
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, 1)

    def test_draw_condition(self):
        # P1: 0, 2, 3, 7, 8
        # P2: 1, 4, 5, 6
        self.game.make_move(0); self.game.make_move(1)
        self.game.make_move(2); self.game.make_move(4)
        self.game.make_move(3); self.game.make_move(5)
        self.game.make_move(7); self.game.make_move(6)
        self.game.make_move(8) 
        self.assertTrue(self.game.game_over, "Game should be over due to draw.")
        self.assertEqual(self.game.winner, 0, "Winner should be 0 for a draw.")

    # --- Dimensional Fold Effects ---
    def test_space_fold_effect(self):
        self.game.grid = np.array([[1,2,0],[1,0,2],[0,1,2]])
        expected_grid_after_fold = [[1,0,2],[1,2,0],[0,2,1]]
        
        actions = self.game.make_move(grid_index=-1, fold_index=0) # Activate Space Fold
        self.assertIn("FOLD_TOGGLED", actions)
        self.assertEqual(self.game.folded_dimension[0], 1)
        self.assertGridEqual(self.game.grid, expected_grid_after_fold, "Columns 1 and 2 should swap.")

        actions = self.game.make_move(grid_index=-1, fold_index=0) # Deactivate Space Fold
        self.assertIn("FOLD_TOGGLED", actions)
        self.assertEqual(self.game.folded_dimension[0], 0)
        self.assertGridEqual(self.game.grid, [[1,2,0],[1,0,2],[0,1,2]], "Columns should swap back.")

    def test_time_fold_effect_with_piece(self):
        self.game.make_move(0) # P1 places at (0,0)
        self.assertGridEqual(self.game.grid, [[1,0,0],[0,0,0],[0,0,0]])
        
        # P2's turn, places at (1,1) and activates Time Fold
        actions = self.game.make_move(grid_index=4, fold_index=1) 
        self.assertIn("PIECE_PLACED", actions)
        self.assertIn("FOLD_TOGGLED", actions)
        self.assertGridEqual(self.game.grid, [[1,0,0],[0,0,0],[0,0,0]], "P2's piece at (1,1) should be reverted by Time Fold.")
        self.assertEqual(self.game.current_player, 1, "Should be P1's turn again as P2's piece placement was reverted but turn still passes.")
        self.assertEqual(self.game.folded_dimension[1], 1, "Time fold should be active.")

    def test_time_fold_effect_no_piece(self):
        self.game.make_move(grid_index=-1, fold_index=1) # P1 activates Time Fold without placing piece
        self.assertGridEqual(self.game.grid, [[0,0,0],[0,0,0],[0,0,0]], "Grid should remain empty.")
        self.assertEqual(self.game.folded_dimension[1], 1)
        self.assertEqual(self.game.current_player, 2, "Should be Player 2's turn.")

    def test_rule_fold_effect(self):
        self.game.grid = np.array([[1,2,0],[1,0,2],[0,0,0]]) # P1 at (0,0), (1,0); P2 at (0,1), (1,2)
        expected_grid_after_fold = [[2,1,0],[2,0,1],[0,0,0]]
        
        actions = self.game.make_move(grid_index=-1, fold_index=2) # Activate Rule Fold
        self.assertIn("FOLD_TOGGLED", actions)
        self.assertGridEqual(self.game.grid, expected_grid_after_fold, "Pieces should be inverted.")
        self.assertEqual(self.game.folded_dimension[2], 1)

    def test_chaos_fold_effect(self):
        self.game.grid = np.array([[1,2,0],[1,0,0],[0,0,0]])
        original_piece_count_p1 = np.sum(self.game.grid == 1)
        original_piece_count_p2 = np.sum(self.game.grid == 2)
        
        actions = self.game.make_move(grid_index=-1, fold_index=3) # Activate Chaos Fold
        self.assertIn("FOLD_TOGGLED", actions)
        self.assertEqual(np.sum(self.game.grid == 1), original_piece_count_p1, "P1 piece count should remain.")
        self.assertEqual(np.sum(self.game.grid == 2), original_piece_count_p2, "P2 piece count should remain.")
        # It's hard to test exact shuffle, but check if grid is different if it wasn't empty/full
        if original_piece_count_p1 > 0 or original_piece_count_p2 > 0:
             # This assertion might fail if the shuffle results in the exact same grid, which is statistically unlikely for non-trivial grids.
             # For a more robust test, one might need to check multiple shuffles or a fixed seed if the game used one.
             pass # For now, just checking piece counts is the most reliable.
        self.assertEqual(self.game.folded_dimension[3], 1)

    def test_fold_toggle(self):
        self.game.make_move(grid_index=-1, fold_index=0) # Activate
        self.assertEqual(self.game.folded_dimension[0], 1)
        self.game.make_move(grid_index=-1, fold_index=0) # Deactivate
        self.assertEqual(self.game.folded_dimension[0], 0)

    def test_make_move_with_fold_and_piece(self):
        actions = self.game.make_move(grid_index=0, fold_index=0) # P1 places at 0, activates Space Fold
        self.assertIn("PIECE_PLACED", actions)
        self.assertIn("FOLD_TOGGLED", actions)
        self.assertEqual(self.game.grid.flat[0], 1, "Piece should be placed.") # Note: Space fold might move it, check specific logic if needed
        self.assertEqual(self.game.folded_dimension[0], 1, "Space fold should be active.")
        self.assertEqual(self.game.current_player, 2)


    # --- Special Win Condition ---
    def test_dimensional_dominance_win_player1_rule_fold_is_third(self):
        # P1 makes the 3rd fold, and it's Rule Fold.
        # P2 must have more pieces *before* P1's move for P1 to win.
        self.game.grid = np.array([[2,2,0],[0,2,0],[1,0,0]]) # P2 has 3, P1 has 1
        
        # P1's turn (activates Space Fold)
        self.game.make_move(grid_index=-1, fold_index=0) # Folds: [1,0,0,0]. Grid: [[2,0,2],[0,2,0],[1,0,0]] -> P2 has 3, P1 has 1. Player: P2
        # P2's turn (activates Time Fold)
        self.game.make_move(grid_index=-1, fold_index=1) # Folds: [1,1,0,0]. Grid: (same). Player: P1
        # P1's turn (activates Rule Fold - this is the 3rd active fold)
        # Before Rule Fold by P1: Grid is [[2,0,2],[0,2,0],[1,0,0]] (P2:3, P1:1)
        # After Rule Fold by P1: Grid becomes [[1,0,1],[0,1,0],[2,0,0]] (P1:3, P2:1)
        self.game.make_move(grid_index=-1, fold_index=2) 
        
        self.assertTrue(self.game.game_over, "Game should be over by dimensional dominance.")
        self.assertEqual(self.game.winner, 1, "Player 1 should win by dimensional dominance after Rule Fold.")

    def test_dimensional_dominance_win_player1_non_rule_fold_is_third(self):
        # P1 makes the 3rd fold, and it's NOT Rule Fold.
        # P1 must have more pieces *before* P1's move.
        self.game.grid = np.array([[1,1,0],[0,1,0],[2,0,0]]) # P1 has 3, P2 has 1
        # P1's turn (activates Fold 0 - e.g. Space)
        self.game.make_move(grid_index=-1, fold_index=0) # Folds: [1,0,0,0]. Grid may change. P1:3, P2:1 still. Player: P2
        # P2's turn (activates Fold 1 - e.g. Time)
        self.game.make_move(grid_index=-1, fold_index=1) # Folds: [1,1,0,0]. Grid same. Player: P1
        # P1's turn (activates Fold 3 - e.g. Chaos, which doesn't change piece ownership)
        # Before Chaos Fold by P1: P1 has 3, P2 has 1.
        self.game.make_move(grid_index=-1, fold_index=3)
        
        self.assertTrue(self.game.game_over, "Game should be over by dimensional dominance.")
        self.assertEqual(self.game.winner, 1, "Player 1 should win by dimensional dominance with non-Rule Fold.")


    def test_dimensional_dominance_no_win_equal_pieces(self):
        self.game.grid = np.array([[1,1,0],[0,2,0],[0,0,2]]) # P1 has 2, P2 has 2
        self.game.make_move(grid_index=-1, fold_index=0) # P1
        self.game.make_move(grid_index=-1, fold_index=1)
        self.game.make_move(grid_index=-1, fold_index=2)
        self.assertFalse(self.game.game_over, "Game should not be over if pieces are equal on dimensional dominance.")

    def test_reset_game(self):
        self.game.make_move(0)
        self.game.make_move(grid_index=-1, fold_index=1)
        self.game.grid = np.array([[1,1,1],[0,0,0],[0,0,0]]) # Force a win
        self.game.check_win_condition()
        self.assertTrue(self.game.game_over)

        self.game.reset_game()
        self.test_initial_state() # Check if game is back to initial state

if __name__ == '__main__':
    unittest.main()
