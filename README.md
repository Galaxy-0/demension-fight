# Dimensional Folding Tic-Tac-Toe

Welcome to Dimensional Folding Tic-Tac-Toe! This game takes the classic Tic-Tac-Toe and adds a strategic twist: players can fold and unfold dimensions to alter the rules of the game, leading to unique tactical possibilities.

## How to Play

The game is played on a 3x3 grid. Two players take turns placing their pieces (Player 1 is Red-ish, Player 2 is Blue-ish). The objective is to be the first to get three of your pieces in a row, column, or diagonal.

**Making a Move:**
1.  **Place a Piece:** Click on an empty square in the 3x3 grid to place your piece.
2.  **Fold a Dimension (Optional):** Before or after placing a piece (or instead of placing a piece), you can click on one of the four "Fold Buttons" on the left side of the screen. Each button corresponds to a different dimension:
    *   空间折叠 (Space Folding)
    *   时间折叠 (Time Folding)
    *   规则折叠 (Rule Folding)
    *   混沌折叠 (Chaos Folding)
    Clicking a button toggles the state of that dimension (folded or unfolded). Active folds are indicated by a brighter color on the button and its corresponding indicator dot.

## Dimensional Folds

Each dimensional fold has a unique impact on the game state:

*   **空间折叠 (Space Folding):**
    *   **Effect:** When activated, this fold swaps the second and third columns of the game grid. Deactivating it swaps them back.
*   **时间折叠 (Time Folding):**
    *   **Effect:** If you activate this fold *and* place a piece in the same turn, the piece you just placed is immediately removed (effectively undoing your piece placement for that turn). This allows for strategic "empty" moves or correcting a mistake if combined with a piece placement.
*   **规则折叠 (Rule Folding):**
    *   **Effect:** Activating this fold inverts all pieces currently on the board. Player 1's pieces become Player 2's, and Player 2's pieces become Player 1's. Empty cells remain empty. Deactivating it inverts them again.
*   **混沌折叠 (Chaos Folding):**
    *   **Effect:** When activated, all pieces currently on the grid are randomly shuffled to different occupied positions. The pattern of pieces changes unpredictably. This only happens if there is more than one piece on the board.

## Winning Conditions

There are two ways to win the game:

1.  **Standard Tic-Tac-Toe:**
    *   Get three of your pieces in a horizontal row.
    *   Get three of your pieces in a vertical column.
    *   Get three of your pieces in a diagonal line.
2.  **Dimensional Dominance (Special Condition):**
    *   If three or more dimensional folds are simultaneously active, the game checks the number of pieces on the board for each player.
    *   The player with strictly more pieces on the board immediately wins. If the piece counts are equal, this condition does not result in a win.

**Draw:**
*   If the grid becomes completely full and no player has met any winning condition, the game is a draw.

**Restarting the Game:**
*   Press the 'R' key at any time to reset the game to its initial state.

## Setup and Run

To play Dimensional Folding Tic-Tac-Toe, you need Python and the following libraries: Pygame and NumPy.

1.  **Prerequisites:**
    *   Ensure you have Python installed (version 3.7 or newer recommended).

2.  **Installation:**
    *   Open a terminal or command prompt.
    *   Install Pygame and NumPy using pip:
        ```bash
        pip install pygame numpy
        ```

3.  **Running the Game:**
    *   Navigate to the directory where the game files (`main.py`, `game_logic.py`, `rendering.py`) are located.
    *   Run the game using the following command:
        ```bash
        python main.py
        ```

Enjoy the mind-bending challenge!
