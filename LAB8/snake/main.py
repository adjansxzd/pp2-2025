import pygame
import random
from color_palette import * # import готовых цветов

pygame.init()
# Screen settings
WIDTH = 600
HEIGHT = 600
CELL = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

# Game Over screen
image_game_over = font.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))
# Draw grid like chess
def draw_grid_chess():
    colors = [colorWHITE, colorGRAY]
    for i in range(WIDTH // CELL):
        for j in range(HEIGHT // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))
# Class to represent grip position
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
# Class snake
class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)] # body 
        self.dx = 1
        self.dy = 0
        self.score = 0 # track points
        self.level = 1 # track levels

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy
    # Рисует голову красной а тело желтым
    def draw(self):
        for i, segment in enumerate(self.body):
            color = colorRED if i == 0 else colorYELLOW
            pygame.draw.rect(screen, color, (segment.x * CELL, segment.y * CELL, CELL, CELL))
    # Проверка на collision с едой
    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.body.append(Point(head.x, head.y))
            self.score += 1
            if self.score % 4 == 0:
                self.level += 1
            return True
        return False
    # Выводит если змея ударилась о стену
    def check_wall_collision(self):
        head = self.body[0]
        return head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL
    # Если об себя
    def check_self_collision(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False
# Food class
class Food:
    def __init__(self):
        self.pos = Point(9, 9)  
    # random position
    def generate(self, snake):
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)
            if all(segment.x != x or segment.y != y for segment in snake.body):
                self.pos = Point(x, y)
                break

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

# Game setup
snake = Snake()
food = Food()

food.generate(snake)
FPS = 7 # fps and speed
running = True
game_over = False
# movement
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx = 0
                snake.dy = -1

    if not game_over:
        snake.move()
    # If snake hits wall or yourself --> game over
        if snake.check_wall_collision() or snake.check_self_collision():
            game_over = True
            screen.fill("red")
            screen.blit(image_game_over, image_game_over_rect)
            pygame.display.flip()
            
            continue
        # Move
        if snake.check_collision(food):
            food.generate(snake)

        screen.fill(colorBLACK)
        draw_grid_chess()
        snake.draw()
        food.draw()
        # Render of indicators
        score_text = font.render(f"Score: {snake.score}", True, colorBLACK)
        level_text = font.render(f"Level: {snake.level}", True, colorBLACK)
        speed_text = font.render(f"Speed: {FPS + snake.level - 1}", True, colorBLACK)
        # Вывод на экран индикаторы
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))
        screen.blit(speed_text, (10, 70))

        pygame.display.flip() # Update
        clock.tick(FPS + snake.level - 1)

pygame.quit()
