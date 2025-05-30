import pygame
import sys
from enum import Enum, auto
import os  # Add import for file existence check

# Import classes from new modules
from game_logic import DimensionalFoldingGame
from rendering import GameRenderer, TEXT_COLOR # Import TEXT_COLOR for menu

# Define Game States
class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    HOW_TO_PLAY = auto()

# 初始化
pygame.init()
mixer_initialized = False
try:
    pygame.mixer.init() # Initialize the mixer
    mixer_initialized = True
except pygame.error as e:
    print(f"Warning: pygame.mixer.init() failed: {e}. Sound will be disabled.")

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dimensional Folding Tic-Tac-Toe") # Window Title
clock = pygame.time.Clock()

# Sound Effects (Placeholders - files are not actually present)
sound_files = {
    "place_piece": "assets/sounds/place_piece.wav",
    "fold_toggle": "assets/sounds/fold_toggle.wav",
    "invalid_move": "assets/sounds/invalid_move.wav",
    "game_win": "assets/sounds/game_win.wav",
    "game_draw": "assets/sounds/game_draw.wav",
    "ui_click": "assets/sounds/ui_click.wav"
}
sounds = {}
for key, filepath in sound_files.items():
    try:
        # Check if file exists before attempting to load
        if os.path.exists(filepath):
            sounds[key] = pygame.mixer.Sound(filepath)
        else:
            print(f"Info: Sound file '{filepath}' not found, skipping...")
            sounds[key] = None
    except pygame.error as e:
        print(f"Warning: Could not load sound '{filepath}': {e}")
        sounds[key] = None # Store None if loading fails

sound_enabled = True # Global sound toggle

def play_sound(sound_name):
    if sound_enabled and mixer_initialized and sounds.get(sound_name): # Check mixer_initialized
        sounds[sound_name].play()

# Menu items
menu_items = ["Start Game", "How to Play", "Exit Game"] # Start Game, How to Play, Exit
selected_menu_item_idx = 0

# How to Play text (condensed from README)
how_to_play_content = [
    "Objective: Standard tic-tac-toe rules - first to connect three wins.",
    "Special Mechanic: Dimensional Folding - click left buttons to toggle effects.",
    "",
    "Dimensional Effects:",
    "1. Space Folding: Swap middle and right columns.",
    "2. Time Folding: (if placed simultaneously) undo current move.",
    "3. Rule Folding: Flip all pieces on board (red becomes blue, blue becomes red).",
    "4. Chaos Folding: Randomly rearrange all pieces on board.",
    "",
    "Special Victory: When three dimensions are active, player with more pieces wins.",
    "Draw: Board is full with no winner.",
    "Press 'R' to restart game anytime.",
    "Press ESC or M to return to main menu from rules."
]


# ===== 主游戏循环 =====
def main():
    global selected_menu_item_idx, sound_enabled # Allow modification

    game = DimensionalFoldingGame()
    renderer = GameRenderer(game, WIDTH, HEIGHT)
    
    current_game_state = GameState.MENU
    previous_game_over_state = game.game_over # To detect game over transition

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            renderer.clear_click_feedback() # Clear click visualization states at start of new event processing

            if event.type == pygame.KEYDOWN: # Global key presses
                if event.key == pygame.K_s: # Toggle sound
                    sound_enabled = not sound_enabled
                    print(f"Sound enabled: {sound_enabled}") # Feedback for toggle

            if current_game_state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset_game()
                        previous_game_over_state = False # Reset this as well
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_m: 
                        current_game_state = GameState.MENU
                        play_sound("ui_click")
                        game.reset_game() 
                        previous_game_over_state = False
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        actions = []
                        # Check fold buttons first
                        fold_button_clicked = False
                        for i, btn_rect in enumerate(renderer.fold_btns):
                            if btn_rect.collidepoint(event.pos):
                                renderer.set_clicked_fold_button(i)
                                actions = game.make_move(grid_index=-1, fold_index=i)
                                fold_button_clicked = True
                                break
                        
                        if not fold_button_clicked and not game.game_over:
                            for i, cell_rect in enumerate(renderer.grid_rects):
                                if cell_rect.collidepoint(event.pos):
                                    renderer.set_clicked_grid_cell(i)
                                    actions = game.make_move(grid_index=i)
                                    break 
                        elif game.game_over: 
                             if any(btn.collidepoint(event.pos) for btn in renderer.fold_btns) or \
                                any(rect.collidepoint(event.pos) for rect in renderer.grid_rects):
                                game.reset_game()
                                previous_game_over_state = False
                                play_sound("ui_click") # Or a specific "restart_game" sound
                        
                        # Process actions for sounds
                        if "INVALID_MOVE" in actions:
                            play_sound("invalid_move")
                        if "PIECE_PLACED" in actions:
                            play_sound("place_piece")
                        if "FOLD_TOGGLED" in actions:
                            play_sound("fold_toggle")
                        # Note: make_move now returns a list. If it's empty, no sound, no player switch.
                        # This shouldn't happen if clicks are on valid elements.
                
                # Check for game over state transition to play win/draw sounds
                if game.game_over and not previous_game_over_state:
                    if game.winner == 0: # Draw
                        play_sound("game_draw")
                    elif game.winner is not None: # Player won
                        play_sound("game_win")
                previous_game_over_state = game.game_over


            elif current_game_state == GameState.MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_menu_item_idx = (selected_menu_item_idx - 1) % len(menu_items)
                        play_sound("ui_click")
                    elif event.key == pygame.K_DOWN:
                        selected_menu_item_idx = (selected_menu_item_idx + 1) % len(menu_items)
                        play_sound("ui_click")
                    elif event.key == pygame.K_RETURN: # Enter key
                        play_sound("ui_click")
                        if selected_menu_item_idx == 0: 
                            current_game_state = GameState.PLAYING
                            game.reset_game() 
                            previous_game_over_state = False
                        elif selected_menu_item_idx == 1: 
                            current_game_state = GameState.HOW_TO_PLAY
                        elif selected_menu_item_idx == 2: 
                            running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if hasattr(renderer, 'menu_item_rects'):
                            for i, item_rect in enumerate(renderer.menu_item_rects):
                                if item_rect and item_rect.collidepoint(event.pos):
                                    selected_menu_item_idx = i 
                                    play_sound("ui_click")
                                    if selected_menu_item_idx == 0: current_game_state = GameState.PLAYING; game.reset_game(); previous_game_over_state = False
                                    elif selected_menu_item_idx == 1: current_game_state = GameState.HOW_TO_PLAY
                                    elif selected_menu_item_idx == 2: running = False
                                    break
            
            elif current_game_state == GameState.HOW_TO_PLAY:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                        current_game_state = GameState.MENU
                        play_sound("ui_click")
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                     current_game_state = GameState.MENU
                     play_sound("ui_click")


        # Rendering based on state
        if current_game_state == GameState.PLAYING:
            renderer.draw(screen)
        elif current_game_state == GameState.MENU:
            renderer.draw_menu(screen, menu_items, selected_menu_item_idx)
        elif current_game_state == GameState.HOW_TO_PLAY:
            renderer.draw_how_to_play(screen, how_to_play_content)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()