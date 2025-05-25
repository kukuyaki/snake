import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 設定顏色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GREEN = (0, 150, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# 預設遊戲參數
DEFAULT_WINDOW_WIDTH = 800
DEFAULT_WINDOW_HEIGHT = 600
DEFAULT_CELL_SIZE = 20
DEFAULT_SNAKE_LENGTH = 3
DEFAULT_FOOD_COUNT = 1
DEFAULT_SPEED = 120

class GameSettings:
    def __init__(self):
        self.window_width = DEFAULT_WINDOW_WIDTH
        self.window_height = DEFAULT_WINDOW_HEIGHT
        self.cell_size = DEFAULT_CELL_SIZE
        self.snake_length = DEFAULT_SNAKE_LENGTH
        self.food_count = DEFAULT_FOOD_COUNT
        self.speed = DEFAULT_SPEED
        
    @property
    def cell_number_x(self):
        return self.window_width // self.cell_size
        
    @property
    def cell_number_y(self):
        return self.window_height // self.cell_size

class StartScreen:
    def __init__(self):
        self.settings = GameSettings()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
    def draw_slider(self, screen, x, y, width, min_val, max_val, current_val, label):
        # 繪製滑桿背景
        pygame.draw.rect(screen, GRAY, (x, y, width, 20))
        
        # 計算滑桿位置
        slider_pos = int(x + (current_val - min_val) / (max_val - min_val) * width)
        pygame.draw.circle(screen, WHITE, (slider_pos, y + 10), 12)
        pygame.draw.circle(screen, BLUE, (slider_pos, y + 10), 10)
        
        # 繪製標籤和數值
        label_text = self.font_small.render(f"{label}: {current_val}", True, WHITE)
        screen.blit(label_text, (x, y - 25))
        
        return pygame.Rect(x - 12, y - 2, width + 24, 24)
    
    def handle_slider_input(self, mouse_pos, slider_rect, x, width, min_val, max_val):
        if slider_rect.collidepoint(mouse_pos):
            relative_x = mouse_pos[0] - x
            relative_x = max(0, min(relative_x, width))
            return int(min_val + (relative_x / width) * (max_val - min_val))
        return None
    
    def draw_button(self, screen, x, y, width, height, text, color=BLUE):
        pygame.draw.rect(screen, color, (x, y, width, height))
        pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)
        
        text_surface = self.font_medium.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(x + width//2, y + height//2))
        screen.blit(text_surface, text_rect)
        
        return pygame.Rect(x, y, width, height)
    
    def show(self, screen):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            screen.fill(BLACK)
            
            # 標題
            title = self.font_large.render("snake game setting", True, GREEN)
            title_rect = title.get_rect(center=(screen.get_width()//2, 50))
            screen.blit(title, title_rect)
            
            # 設定區域起始位置
            start_y = 120
            spacing = 80
            slider_width = 300
            center_x = screen.get_width() // 2 - slider_width // 2
            
            # 畫面寬度滑桿
            width_rect = self.draw_slider(screen, center_x, start_y, slider_width, 
                                        600, 1200, self.settings.window_width, "width")
            
            # 畫面高度滑桿
            height_rect = self.draw_slider(screen, center_x, start_y + spacing, slider_width, 
                                         400, 800, self.settings.window_height, "height")
            
            # 格子大小滑桿
            cell_rect = self.draw_slider(screen, center_x, start_y + spacing*2, slider_width, 
                                       15, 30, self.settings.cell_size, "block size")
            
            # 初始蛇長度滑桿
            snake_rect = self.draw_slider(screen, center_x, start_y + spacing*3, slider_width, 
                                        2, 10, self.settings.snake_length, "snake length")
            
            # 食物數量滑桿
            food_rect = self.draw_slider(screen, center_x, start_y + spacing*4, slider_width, 
                                       1, 8, self.settings.food_count, "food number")
            
            # 遊戲速度滑桿
            speed_rect = self.draw_slider(screen, center_x, start_y + spacing*5, slider_width, 
                                        60, 200, self.settings.speed, "speed(ms)")
            
            # 預覽資訊
            preview_y = start_y + spacing*6 + 20
            preview_info = [
                f"gmae file: {self.settings.cell_number_x} x {self.settings.cell_number_y} blocks",
                f"total: {self.settings.cell_number_x * self.settings.cell_number_y}",
                f"recomand window size: {self.settings.cell_number_x * self.settings.cell_size} x {self.settings.cell_number_y * self.settings.cell_size}"
            ]
            
            for i, info in enumerate(preview_info):
                info_text = self.font_small.render(info, True, LIGHT_GRAY)
                info_rect = info_text.get_rect(center=(screen.get_width()//2, preview_y + i*25))
                screen.blit(info_text, info_rect)
            
            # 按鈕
            button_y = preview_y + 100
            start_button_rect = self.draw_button(screen, center_x, button_y, 140, 50, "start", GREEN)
            reset_button_rect = self.draw_button(screen, center_x + 160, button_y, 140, 50, "reset", GRAY)
            
            # 處理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # 檢查滑桿
                    new_width = self.handle_slider_input(mouse_pos, width_rect, center_x, slider_width, 600, 1200)
                    if new_width is not None:
                        self.settings.window_width = new_width
                    
                    new_height = self.handle_slider_input(mouse_pos, height_rect, center_x, slider_width, 400, 800)
                    if new_height is not None:
                        self.settings.window_height = new_height
                    
                    new_cell = self.handle_slider_input(mouse_pos, cell_rect, center_x, slider_width, 15, 30)
                    if new_cell is not None:
                        self.settings.cell_size = new_cell
                    
                    new_snake = self.handle_slider_input(mouse_pos, snake_rect, center_x, slider_width, 2, 10)
                    if new_snake is not None:
                        self.settings.snake_length = new_snake
                    
                    new_food = self.handle_slider_input(mouse_pos, food_rect, center_x, slider_width, 1, 8)
                    if new_food is not None:
                        self.settings.food_count = new_food
                    
                    new_speed = self.handle_slider_input(mouse_pos, speed_rect, center_x, slider_width, 60, 200)
                    if new_speed is not None:
                        self.settings.speed = new_speed
                    
                    # 檢查按鈕
                    if start_button_rect.collidepoint(mouse_pos):
                        return self.settings
                    
                    if reset_button_rect.collidepoint(mouse_pos):
                        self.settings = GameSettings()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return self.settings
            
            pygame.display.flip()
            clock.tick(60)

class Snake:
    def __init__(self, settings):
        self.settings = settings
        # 根據設定建立初始蛇身
        start_x = settings.cell_number_x // 2
        start_y = settings.cell_number_y // 2
        self.body = []
        for i in range(settings.snake_length):
            self.body.append(pygame.Vector2(start_x - i, start_y))
        
        self.direction = pygame.Vector2(1, 0)
        self.new_direction = pygame.Vector2(1, 0)
        self.new_block = False
        
    def draw_snake(self, screen):
        for i, block in enumerate(self.body):
            x_pos = int(block.x * self.settings.cell_size)
            y_pos = int(block.y * self.settings.cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, self.settings.cell_size, self.settings.cell_size)
            
            # 蛇頭用不同顏色
            if i == 0:
                pygame.draw.rect(screen, DARK_GREEN, block_rect)
            else:
                pygame.draw.rect(screen, GREEN, block_rect)
            
    def move_snake(self):
        self.direction = self.new_direction
        
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True
    
    def change_direction(self, direction):
        if direction == pygame.Vector2(0, -1) and self.direction.y != 1:
            self.new_direction = direction
        elif direction == pygame.Vector2(0, 1) and self.direction.y != -1:
            self.new_direction = direction
        elif direction == pygame.Vector2(1, 0) and self.direction.x != -1:
            self.new_direction = direction
        elif direction == pygame.Vector2(-1, 0) and self.direction.x != 1:
            self.new_direction = direction
    
    def check_collision(self):
        if not 0 <= self.body[0].x < self.settings.cell_number_x or not 0 <= self.body[0].y < self.settings.cell_number_y:
            return True
        
        for block in self.body[1:]:
            if block == self.body[0]:
                return True
        
        return False

class Food:
    def __init__(self, settings):
        self.settings = settings
        self.positions = []
        self.colors = [RED, ORANGE, PURPLE, CYAN]
        self.generate_food()
    
    def generate_food(self):
        self.positions = []
        for _ in range(self.settings.food_count):
            self.add_food()
    
    def add_food(self):
        x = random.randint(0, self.settings.cell_number_x - 1)
        y = random.randint(0, self.settings.cell_number_y - 1)
        pos = pygame.Vector2(x, y)
        
        # 確保不重疊
        while pos in self.positions:
            x = random.randint(0, self.settings.cell_number_x - 1)
            y = random.randint(0, self.settings.cell_number_y - 1)
            pos = pygame.Vector2(x, y)
        
        self.positions.append(pos)
    
    def draw_food(self, screen):
        for i, pos in enumerate(self.positions):
            food_rect = pygame.Rect(int(pos.x * self.settings.cell_size), 
                                  int(pos.y * self.settings.cell_size), 
                                  self.settings.cell_size, self.settings.cell_size)
            color = self.colors[i % len(self.colors)]
            pygame.draw.rect(screen, color, food_rect)
    
    def check_collision(self, snake_head):
        for pos in self.positions:
            if pos == snake_head:
                self.positions.remove(pos)
                self.add_food()
                return True
        return False

class Main:
    def __init__(self, settings):
        self.settings = settings
        self.snake = Snake(settings)
        self.food = Food(settings)
        self.score = 0
        self.font = pygame.font.Font(None, 36)
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self, screen):
        self.draw_grass(screen)
        self.food.draw_food(screen)
        self.snake.draw_snake(screen)
        self.draw_score(screen)
    
    def check_collision(self):
        if self.food.check_collision(self.snake.body[0]):
            self.snake.add_block()
            self.score += 10
    
    def check_fail(self):
        if self.snake.check_collision():
            self.game_over()
    
    def game_over(self):
        # 顯示遊戲結束畫面
        overlay = pygame.Surface((self.settings.window_width, self.settings.window_height))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        
        screen = pygame.display.get_surface()
        screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("game over!", True, WHITE)
        score_text = self.font.render(f"final score: {self.score}", True, WHITE)
        restart_text = self.font.render("press r or esc", True, WHITE)
        
        screen.blit(game_over_text, (self.settings.window_width//2 - 80, self.settings.window_height//2 - 60))
        screen.blit(score_text, (self.settings.window_width//2 - 90, self.settings.window_height//2 - 20))
        screen.blit(restart_text, (self.settings.window_width//2 - 150, self.settings.window_height//2 + 20))
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True  # 重新開始
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        
        return False
    
    def draw_grass(self, screen):
        grass_color = (167, 209, 61)
        for row in range(self.settings.cell_number_y):
            if row % 2 == 0:
                for col in range(self.settings.cell_number_x):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * self.settings.cell_size, 
                                               row * self.settings.cell_size, 
                                               self.settings.cell_size, self.settings.cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(self.settings.cell_number_x):
                    if col % 2 == 1:
                        grass_rect = pygame.Rect(col * self.settings.cell_size, 
                                               row * self.settings.cell_size, 
                                               self.settings.cell_size, self.settings.cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
    
    def draw_score(self, screen):
        score_text = f"分數: {self.score}"
        score_surface = self.font.render(score_text, True, (56, 74, 12))
        score_rect = score_surface.get_rect(topleft=(self.settings.cell_size, self.settings.cell_size))
        screen.blit(score_surface, score_rect)

def main():
    # 顯示開始畫面
    start_screen_surface = pygame.display.set_mode((800, 700))
    pygame.display.set_caption('貪吃蛇遊戲設定')
    
    start_screen = StartScreen()
    settings = start_screen.show(start_screen_surface)
    
    # 根據設定調整遊戲視窗
    screen = pygame.display.set_mode((settings.window_width, settings.window_height))
    pygame.display.set_caption('貪吃蛇遊戲')
    clock = pygame.time.Clock()
    
    while True:
        # 創建遊戲實例
        game = Main(settings)
        
        # 設定遊戲更新事件
        SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(SCREEN_UPDATE, settings.speed)
        
        # 遊戲主循環
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == SCREEN_UPDATE:
                    game.update()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.snake.change_direction(pygame.Vector2(0, -1))
                    elif event.key == pygame.K_DOWN:
                        game.snake.change_direction(pygame.Vector2(0, 1))
                    elif event.key == pygame.K_RIGHT:
                        game.snake.change_direction(pygame.Vector2(1, 0))
                    elif event.key == pygame.K_LEFT:
                        game.snake.change_direction(pygame.Vector2(-1, 0))
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            # 繪製遊戲畫面
            screen.fill((175, 215, 70))
            game.draw_elements(screen)
            pygame.display.flip()
            clock.tick(60)
        
        # 顯示設定畫面
        start_screen_surface = pygame.display.set_mode((800, 700))
        pygame.display.set_caption('貪吃蛇遊戲設定')
        settings = start_screen.show(start_screen_surface)
        screen = pygame.display.set_mode((settings.window_width, settings.window_height))
        pygame.display.set_caption('貪吃蛇遊戲')

if __name__ == "__main__":
    main()
