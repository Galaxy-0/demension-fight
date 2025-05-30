import pygame

import pygame

# Constants for rendering - New Color Scheme
# Primary Palette: Dark Teal, Orange, Cyan, Silver
BACKGROUND = (20, 40, 50)    # Deep dark teal/charcoal
GRID_COLOR = (192, 192, 192)  # Silver for grid lines
TEXT_COLOR = (230, 230, 230)  # Very light gray for general text
PANEL_COLOR = (30, 50, 60)    # Slightly lighter than background for the control panel

PLAYER_COLORS = [
    (255, 160, 0),   # Player 1: Vibrant Orange
    (0, 200, 255)    # Player 2: Bright Cyan
]

# Fold Button and Indicator Dot Colors
# (Inactive Color, Active Color, Text Color for Button)
FOLD_INACTIVE_COLOR = (70, 90, 100)  # Muted dark cyan/gray
FOLD_ACTIVE_COLOR = (255, 80, 120) # Bright Pink/Magenta for active folds (stands out)
FOLD_BUTTON_TEXT_COLOR = (230, 230, 230) # Light text for fold buttons

# Specific colors for indicator dots next to fold buttons
# Index 0: Inactive, Index 1: Active
DOT_COLORS = [FOLD_INACTIVE_COLOR, FOLD_ACTIVE_COLOR]

# Click feedback colors (subtle darkening or lightening)
CLICK_OFFSET = -20 # Subtract from RGB to darken on click, or positive to lighten
HOVER_OFFSET = 20  # Add to RGB to lighten on hover (though full hover might be too complex for now)

class GameRenderer:
    """Handles all drawing operations for the Dimensional Folding Game."""
    def __init__(self, game, width, height):
        """
        Initializes the GameRenderer.

        Args:
            game: An instance of the DimensionalFoldingGame class, providing game state.
            width (int): The width of the game screen in pixels.
            height (int): The height of the game screen in pixels.
        """
        self.game = game
        self.width = width
        self.height = height
        
        # Click/Hover states for buttons and grid cells
        self.clicked_fold_button_idx = None # Index of fold button being clicked
        self.clicked_grid_cell_idx = None # Index of grid cell being clicked
        # (Hover tracking would be added here if implemented)

        pygame.font.init() 
        self.font = pygame.font.SysFont(None, int(min(width, height) * 0.07)) 
        self.small_font = pygame.font.SysFont(None, int(min(width, height) * 0.04))
        self.smaller_font = pygame.font.SysFont(None, int(min(width, height) * 0.03)) # For fold active labels

        btn_width = self.width * 0.18
        btn_height = self.height * 0.07
        btn_x_pos = self.width * 0.05 
        self.fold_btns = [
            pygame.Rect(btn_x_pos, self.height * (0.15 + i*0.12), btn_width, btn_height) for i in range(4)
        ]
        
        grid_area_x_start = self.width * 0.30 
        grid_area_y_start = self.height * 0.20
        grid_area_width = self.width * 0.65
        grid_area_height = self.height * 0.7
        cell_spacing = min(grid_area_width, grid_area_height) * 0.05
        cell_width = (grid_area_width - 2 * cell_spacing) / 3
        cell_height = (grid_area_height - 2 * cell_spacing) / 3
        
        self.grid_rects = [
            pygame.Rect(
                grid_area_x_start + (i % 3 * (cell_width + cell_spacing)),
                grid_area_y_start + (i // 3 * (cell_height + cell_spacing)),
                cell_width,
                cell_height
            ) for i in range(9)
        ]
        self.fold_labels = ["空间折叠", "时间折叠", "规则折叠", "混沌折叠"]
        
    def _apply_click_effect(self, base_color, is_clicked):
        """ Helper function to apply a visual effect to a color when clicked. """
        if not is_clicked:
            return base_color
        # Darken the color
        return tuple(max(0, c + CLICK_OFFSET) for c in base_color)

    def draw(self, screen):
        """Renders the entire game state onto the provided Pygame screen."""
        screen.fill(BACKGROUND)
        
        panel_padding = self.height * 0.03
        first_btn_top = self.fold_btns[0].top
        last_btn_bottom = self.fold_btns[-1].bottom
        panel_height = (last_btn_bottom - first_btn_top) + 2 * panel_padding
        panel_rect = pygame.Rect(self.width * 0.025, first_btn_top - panel_padding, self.width * 0.25, panel_height)
        pygame.draw.rect(screen, PANEL_COLOR, panel_rect, border_radius=10)

        for i, btn in enumerate(self.fold_btns):
            is_active = self.game.folded_dimension[i] == 1
            is_clicked = self.clicked_fold_button_idx == i
            
            base_color = FOLD_ACTIVE_COLOR if is_active else FOLD_INACTIVE_COLOR
            draw_color = self._apply_click_effect(base_color, is_clicked)
            
            pygame.draw.rect(screen, draw_color, btn, border_radius=8)
            
            # Add "[ACTIVE]" text if dimension is folded
            label_text = self.fold_labels[i]
            if is_active:
                label_text += " [活动]" # "[ACTIVE]"
            
            text_surface = self.small_font.render(label_text, True, FOLD_BUTTON_TEXT_COLOR)
            text_rect = text_surface.get_rect(center=btn.center)
            screen.blit(text_surface, text_rect)
        
        for i, rect in enumerate(self.grid_rects):
            is_clicked = self.clicked_grid_cell_idx == i
            # For grid, maybe a border highlight on click or a temporary fill
            # For now, just draw the standard grid cell
            pygame.draw.rect(screen, GRID_COLOR, rect, width=3 if not is_clicked else 5, border_radius=12) 
            
            player_on_cell = self.game.grid.flat[i]
            if player_on_cell > 0:
                player_index = player_on_cell - 1
                if 0 <= player_index < len(PLAYER_COLORS):
                    piece_color = PLAYER_COLORS[player_index]
                    # Apply click effect if this piece was just placed (might be tricky to time this perfectly here)
                    # For simplicity, click effect on grid rect border is enough for now.
                    circle_radius = int(min(rect.width, rect.height) * 0.375)
                    pygame.draw.circle(screen, piece_color, rect.center, circle_radius)
        
        if not self.game.game_over:
            # Highlight current player: Make text larger or add an arrow
            status_text_str = f"玩家 {self.game.current_player} 回合"
            status_color = PLAYER_COLORS[self.game.current_player-1]
            
            # Render current player's turn with a slightly larger font or different style
            current_player_font = pygame.font.SysFont(None, int(min(self.width, self.height) * 0.075)) # Slightly larger
            text_surface = current_player_font.render(status_text_str, True, status_color)
        else:
            if self.game.winner == 0:
                status_text_str = "平局！"
                status_color = TEXT_COLOR
            elif self.game.winner is not None:
                status_text_str = f"玩家 {self.game.winner} 获胜！"
                status_color = PLAYER_COLORS[self.game.winner-1]
            else:
                status_text_str = "游戏结束！" 
                status_color = TEXT_COLOR
            text_surface = self.font.render(status_text_str, True, status_color)
        
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height * 0.08))
        screen.blit(text_surface, text_rect)
        
        dot_radius = int(self.height * 0.01)
        for i, state in enumerate(self.game.folded_dimension):
            dot_color = DOT_COLORS[1] if state == 1 else DOT_COLORS[0] 
            dot_pos_x = self.fold_btns[i].left - (self.width * 0.03) 
            dot_pos_y = self.fold_btns[i].centery
            pygame.draw.circle(screen, dot_color, (dot_pos_x, dot_pos_y), dot_radius)
        
        if self.game.game_over:
            overlay_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay_surface.fill((0, 0, 0, 180))
            screen.blit(overlay_surface, (0, 0))
            
            # Game over message (already prepared as text_surface, status_color)
            final_message_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(text_surface, final_message_rect)
            
            restart_prompt_text = "按R键重新开始"
            # Ensure restart prompt is prominent
            restart_font = pygame.font.SysFont(None, int(min(self.width, self.height) * 0.05))
            restart_text_surface = restart_font.render(restart_prompt_text, True, TEXT_COLOR)
            restart_text_rect = restart_text_surface.get_rect(center=(self.width // 2, final_message_rect.bottom + self.height * 0.07))
            screen.blit(restart_text_surface, restart_text_rect)

    # Methods for click feedback to be called from main.py
    def set_clicked_fold_button(self, index):
        self.clicked_fold_button_idx = index

    def set_clicked_grid_cell(self, index):
        self.clicked_grid_cell_idx = index

    def clear_click_feedback(self):
        self.clicked_fold_button_idx = None
        self.clicked_grid_cell_idx = None

    # Placeholder for draw_menu and draw_how_to_play
    def draw_menu(self, screen, menu_items, selected_item_idx):
        # TODO: Implement menu drawing
        screen.fill(BACKGROUND) # Or a different menu background
        title_font = pygame.font.SysFont(None, int(min(self.width, self.height) * 0.1))
        title_surface = title_font.render("维度折叠棋", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(self.width // 2, self.height * 0.2))
        screen.blit(title_surface, title_rect)

        item_font = pygame.font.SysFont(None, int(min(self.width, self.height) * 0.06))
        for i, item_text in enumerate(menu_items):
            color = PLAYER_COLORS[1] if i == selected_item_idx else TEXT_COLOR # Highlight selected item
            item_surface = item_font.render(item_text, True, color)
            item_rect = item_surface.get_rect(center=(self.width // 2, self.height * (0.4 + i * 0.15)))
            screen.blit(item_surface, item_rect)
            # Store rects for click detection in main.py
            if not hasattr(self, 'menu_item_rects'):
                 self.menu_item_rects = [None] * len(menu_items)
            self.menu_item_rects[i] = item_rect


    def draw_how_to_play(self, screen, rules_text_lines):
        # TODO: Implement how-to-play screen drawing
        screen.fill(BACKGROUND)
        title_font = pygame.font.SysFont(None, int(min(self.width, self.height) * 0.08))
        title_surface = title_font.render("游戏规则", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(self.width // 2, self.height * 0.1))
        screen.blit(title_surface, title_rect)

        line_font = pygame.font.SysFont(None, int(min(self.width, self.height) * 0.035))
        for i, line in enumerate(rules_text_lines):
            line_surface = line_font.render(line, True, TEXT_COLOR)
            line_rect = line_surface.get_rect(midleft=(self.width * 0.05, self.height * (0.2 + i * 0.05)))
            screen.blit(line_surface, line_rect)
        
        back_text = "按 ESC 或 M 返回主菜单"
        back_surface = self.small_font.render(back_text, True, TEXT_COLOR)
        back_rect = back_surface.get_rect(center=(self.width // 2, self.height * 0.9))
        screen.blit(back_surface, back_rect)
