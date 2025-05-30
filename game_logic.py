import numpy as np

class DimensionalFoldingGame:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        # Initialize or reset the game state.
        # self.grid: Represents the 3x3 game board. 0 for empty, 1 for Player 1, 2 for Player 2.
        self.grid = np.zeros((3, 3), dtype=int)
        # self.folded_dimension: Tracks the state of four dimensions (0 for normal, 1 for folded).
        # Indices correspond to: 0: Space, 1: Time, 2: Rule, 3: Chaos
        self.folded_dimension = [0, 0, 0, 0]
        self.current_player = 1  # Player 1 starts.
        self.game_over = False
        self.winner = None  # Can be 0 (draw), 1 (Player 1), or 2 (Player 2).
        # self.grid_positions: Screen coordinates for drawing, not used in core logic.
        self.grid_positions = [(i*200+200, j*150+150) for i in range(3) for j in range(3)] # Example positions
        
    def make_move(self, grid_index, fold_index=None):
        """
        Processes a player's move, which can be placing a piece, folding/unfolding a dimension, or both.

        Args:
            grid_index (int): The flattened index (0-8) of the grid cell for piece placement.
                              If -1, no piece is placed (only fold operation occurs).
            fold_index (int, optional): The index (0-3) of the dimension to toggle. Defaults to None.

        Returns:
            bool: True if the move was valid and processed, False otherwise.
        """
        # Prevent moves if the game is over or if the selected cell is already occupied.
        action_performed = [] # List to store types of actions

        if self.game_over or (grid_index != -1 and self.grid.flat[grid_index] != 0):
            return ["INVALID_MOVE"] # Move is invalid.
        
        # Place the current player's piece on the grid if a cell is selected.
        if grid_index != -1:
            self.grid.flat[grid_index] = self.current_player
            action_performed.append("PIECE_PLACED")
        
        # Process dimension folding if a fold_index is provided.
        if fold_index is not None:
            self.folded_dimension[fold_index] = 1 - self.folded_dimension[fold_index]  # Toggle the dimension's state (0 to 1 or 1 to 0).
            action_performed.append("FOLD_TOGGLED")
            
            # Apply the unique effect of the activated/deactivated dimensional fold.
            if fold_index == 0:  # Space Folding: Swaps the second and third columns of the grid.
                self.grid[:, [1, 2]] = self.grid[:, [2, 1]]
            elif fold_index == 1:  # Time Folding: If a piece was placed in this same turn, it's removed (undo).
                if grid_index != -1:  # Only effective if a piece placement was part of this move.
                    self.grid.flat[grid_index] = 0  # Revert the cell to empty.
            elif fold_index == 2:  # Rule Folding: Inverts all pieces on the board (Player 1 <-> Player 2).
                                    # Empty cells (0) remain empty.
                # Create a temporary copy to ensure correct swapping, e.g., 1s become 2s, original 2s become 1s.
                temp_grid = np.copy(self.grid)
                self.grid[temp_grid == 1] = 2 # All Player 1 pieces become Player 2 pieces.
                self.grid[temp_grid == 2] = 1 # All Player 2 pieces become Player 1 pieces.
            elif fold_index == 3:  # Chaos Folding: Randomly shuffles all existing pieces on the board.
                non_empty_indices = np.argwhere(self.grid > 0)  # Get coordinates of all cells with pieces.
                if len(non_empty_indices) > 1: # Only shuffle if there's more than one piece.
                    piece_values = self.grid[tuple(non_empty_indices.T)] # Extract the piece values (1s and 2s).
                    np.random.shuffle(piece_values) # Shuffle these extracted pieces.
                    
                    # Place the shuffled pieces back onto the original locations of non-empty cells.
                    self.grid[tuple(non_empty_indices.T)] = piece_values
        
        # After any action, check if a win or draw condition has been met.
        self.check_win_condition() # This might set self.game_over and self.winner
        
        # If the move was valid (a piece was placed or a dimension was folded), switch to the other player.
        if not action_performed: # If nothing was done (e.g. fold_index was None and grid_index was -1 with no piece placed prior)
             # This case should ideally not be reached if called with grid_index -1 and no fold_index.
             # However, if it's an invalid move not caught above (e.g. clicking outside valid areas, handled by UI)
             # we might return an empty list or a specific no_action flag.
             # For now, if action_performed is empty, it implies a logic flaw or an unhandled click type.
             # Let's assume valid calls always try to do *something*.
             pass


        if action_performed:
            self.current_player = 3 - self.current_player # Switches player (1 -> 2, 2 -> 1).
            return action_performed
        else:
            # This case implies an invalid call or an unhandled scenario.
            # For safety, treat as invalid if no specific action was logged.
            return ["INVALID_MOVE"] # Or an empty list if main.py handles no actions gracefully
    
    def check_win_condition(self):
        """
        Checks for win conditions (rows, columns, diagonals), the special fold-related win, or a draw.
        Sets self.game_over and self.winner if a condition is met.
        """
        if self.game_over: # If game already ended in a previous check (e.g. by a fold effect directly).
            return

        # Standard Tic-Tac-Toe win conditions: Three identical non-zero pieces in a line.
        for i in range(3):
            # Check row i
            if self.grid[i, 0] != 0 and self.grid[i, 0] == self.grid[i, 1] == self.grid[i, 2]:
                self.end_game(self.grid[i, 0]) # Winner is the player whose piece is in grid[i,0].
                return
            # Check column i
            if self.grid[0, i] != 0 and self.grid[0, i] == self.grid[1, i] == self.grid[2, i]:
                self.end_game(self.grid[0, i]) # Winner is the player whose piece is in grid[0,i].
                return
        
        # Check diagonals
        if self.grid[0, 0] != 0 and self.grid[0, 0] == self.grid[1, 1] == self.grid[2, 2]: # Main diagonal
            self.end_game(self.grid[0, 0]) # Winner is the player whose piece is in grid[0,0].
            return
        if self.grid[0, 2] != 0 and self.grid[0, 2] == self.grid[1, 1] == self.grid[2, 0]: # Anti-diagonal
            self.end_game(self.grid[0, 2]) # Winner is the player whose piece is in grid[0,2].
            return
            
        # Special win condition: Three or more dimensions are simultaneously folded.
        if sum(self.folded_dimension) >= 3:
            player1_pieces = np.sum(self.grid == 1)  # Count total pieces for Player 1.
            player2_pieces = np.sum(self.grid == 2)  # Count total pieces for Player 2.
            # The player with strictly more pieces on the board wins. If counts are equal, no one wins by this rule.
            if player1_pieces != player2_pieces:
                 self.end_game(1 if player1_pieces > player2_pieces else 2)
                 return
                
        # Draw condition: All cells are filled, and no player has won through other conditions.
        if 0 not in self.grid: # Check if there are any empty cells left.
            self.end_game(0)  # 0 signifies a draw.
            return
    
    def end_game(self, winner):
        self.game_over = True
        self.winner = winner
