import pygame
import numpy as np
import sys

# 初始化
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 游戏核心参数
BACKGROUND = (10, 10, 30)
GRID_COLOR = (100, 100, 150)
PLAYER_COLORS = [(220, 60, 60), (60, 180, 220)]
DOT_COLORS = [(180, 230, 80), (230, 180, 80)]

# ===== 创新机制 =====
class DimensionalFoldingGame:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        # 双维度游戏状态：3x3网格（主维度） + 4个折叠状态（次维度）
        self.grid = np.zeros((3, 3), dtype=int)  # 0=空 1=玩家1 2=玩家2
        self.folded_dimension = [0, 0, 0, 0]  # 四个折叠维度的状态（0/1）
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.grid_positions = [(i*200+200, j*150+150) for i in range(3) for j in range(3)]
        
    def make_move(self, grid_index, fold_index=None):
        """玩家行动：选择网格位置 + 可选折叠维度"""
        if self.game_over or self.grid.flat[grid_index] != 0:
            return False
        
        # 放置棋子
        self.grid.flat[grid_index] = self.current_player
        
        # 折叠维度操作（改变物理规则）
        if fold_index is not None:
            self.folded_dimension[fold_index] = 1 - self.folded_dimension[fold_index]
            
            # 维度折叠的特殊效果（核心创新点！）
            if fold_index == 0:  # 折叠空间：交换两列
                self.grid[:, [1, 2]] = self.grid[:, [2, 1]]
            elif fold_index == 1:  # 折叠时间：回退一步
                self.grid.flat[grid_index] = 0  # 撤销当前落子
            elif fold_index == 2:  # 折叠规则：反转所有棋子
                self.grid = 3 - self.grid
                self.grid[self.grid == 3] = 0
            elif fold_index == 3:  # 折叠胜利条件：随机移动所有棋子
                non_empty = np.argwhere(self.grid > 0)
                if len(non_empty) > 1:
                    np.random.shuffle(non_empty)
                    values = self.grid[tuple(non_empty.T)]
                    np.random.shuffle(values)
                    self.grid = np.zeros_like(self.grid)
                    self.grid[tuple(non_empty.T)] = values
        
        # 检查胜利条件（受折叠状态影响！）
        self.check_win_condition()
        
        # 切换玩家
        self.current_player = 3 - self.current_player
        return True
    
    def check_win_condition(self):
        """动态变化的胜利条件（受维度折叠影响）"""
        # 基础胜利条件：三连
        for i in range(3):
            if abs(sum(self.grid[i, :])) == 3:  # 行
                self.end_game(self.grid[i, 0])
            if abs(sum(self.grid[:, i])) == 3:  # 列
                self.end_game(self.grid[0, i])
        
        # 对角线
        if abs(self.grid[0,0] + self.grid[1,1] + self.grid[2,2]) == 3:
            self.end_game(self.grid[1,1])
        if abs(self.grid[0,2] + self.grid[1,1] + self.grid[2,0]) == 3:
            self.end_game(self.grid[1,1])
            
        # 折叠维度特殊胜利条件
        if sum(self.folded_dimension) >= 3:  # 激活三个折叠维度
            if np.sum(self.grid == 1) > np.sum(self.grid == 2):
                self.end_game(1)
            else:
                self.end_game(2)
                
        # 平局检测
        if 0 not in self.grid:
            self.end_game(0)
    
    def end_game(self, winner):
        self.game_over = True
        self.winner = winner

# ===== 游戏渲染 =====
class GameRenderer:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 28)
        self.fold_btns = [pygame.Rect(50, 100+i*60, 120, 40) for i in range(4)]
        self.grid_rects = [pygame.Rect(200+i%3*200, 150+i//3*150, 80, 80) for i in range(9)]
        self.fold_labels = ["空间折叠", "时间折叠", "规则折叠", "混沌折叠"]
        
    def draw(self, screen):
        # 绘制背景
        screen.fill(BACKGROUND)
        
        # 绘制维度折叠控制面板
        pygame.draw.rect(screen, (30, 30, 50), (20, 80, 180, 300), border_radius=10)
        for i, btn in enumerate(self.fold_btns):
            color = (70, 70, 100) if self.game.folded_dimension[i] == 0 else (180, 100, 200)
            pygame.draw.rect(screen, color, btn, border_radius=8)
            text = self.small_font.render(f"{self.fold_labels[i]}", True, (220, 220, 220))
            screen.blit(text, (btn.centerx - text.get_width()//2, btn.centery - text.get_height()//2))
        
        # 绘制网格
        for i, rect in enumerate(self.grid_rects):
            pygame.draw.rect(screen, GRID_COLOR, rect, width=3, border_radius=12)
            if self.game.grid.flat[i] > 0:
                pygame.draw.circle(screen, PLAYER_COLORS[self.game.grid.flat[i]-1], rect.center, 30)
        
        # 绘制状态信息
        status_text = f"玩家 {self.game.current_player} 回合"
        text = self.font.render(status_text, True, PLAYER_COLORS[self.game.current_player-1])
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 50))
        
        # 绘制折叠维度状态
        for i, state in enumerate(self.game.folded_dimension):
            pygame.draw.circle(screen, DOT_COLORS[state], (40, 110+i*60), 8)
        
        # 游戏结束显示
        if self.game.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            if self.game.winner == 0:
                text = self.font.render("平局！点击重新开始", True, (200, 200, 200))
            else:
                text = self.font.render(f"玩家 {self.game.winner} 获胜！", True, PLAYER_COLORS[self.game.winner-1])
            
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
            restart_text = self.small_font.render("按R键重新开始", True, (180, 180, 255))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

# ===== 主游戏循环 =====
def main():
    game = DimensionalFoldingGame()
    renderer = GameRenderer(game)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 重置游戏
                    game.reset_game()
                    
            if not game.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                # 检查维度折叠按钮
                for i, btn in enumerate(renderer.fold_btns):
                    if btn.collidepoint(event.pos):
                        game.make_move(-1, i)  # 仅折叠操作
                        
                # 检查网格点击
                for i, rect in enumerate(renderer.grid_rects):
                    if rect.collidepoint(event.pos):
                        game.make_move(i)
        
        # 渲染
        renderer.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()