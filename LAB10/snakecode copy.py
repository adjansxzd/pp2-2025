import pygame
import time
import random
import psycopg2
from psycopg2 import sql
from color_palette import * 

def init_game_tables():
    """Инициализация таблиц для игры в существующей базе"""
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='BBJN1227',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()
    
    # Таблица пользователей игры
    cur.execute("""
    CREATE TABLE IF NOT EXISTS snake_users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        current_level INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # Таблица уровней
    cur.execute("""
    CREATE TABLE IF NOT EXISTS snake_levels (
        level_id SERIAL PRIMARY KEY,
        level_name VARCHAR(50) NOT NULL,
        speed INTEGER NOT NULL,
        walls TEXT,
        required_score INTEGER NOT NULL
    )""")
    
    # Таблица результатов
    cur.execute("""
    CREATE TABLE IF NOT EXISTS snake_scores (
        score_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES snake_users(user_id),
        score INTEGER NOT NULL,
        level INTEGER NOT NULL,
        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # Проверяем есть ли уровни, если нет - добавляем
    cur.execute("SELECT COUNT(*) FROM snake_levels")
    if cur.fetchone()[0] == 0:
        cur.execute("""
        INSERT INTO snake_levels (level_name, speed, walls, required_score) VALUES
            ('Новичок', 10, '[]', 0),
            ('Любитель', 15, '[[100,100,200,20],[400,300,200,20]]', 10),
            ('Эксперт', 20, '[[50,50,20,300],[300,150,300,20],[200,350,200,20]]', 30)
        """)
    
    conn.commit()
    cur.close()
    conn.close()

def get_db_connection():
    """Подключение к существующей базе"""
    return psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='BBJN1227',
        host='localhost',
        port='5432'
    )

def get_or_create_user(username):
    """Получение или создание пользователя"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
    SELECT user_id, current_level FROM snake_users 
    WHERE username = %s
    """, (username,))
    user = cur.fetchone()
    
    if user:
        user_id, level = user
        print(f"Добро пожаловать, {username}! Текущий уровень: {level}")
    else:
        cur.execute("""
        INSERT INTO snake_users (username) 
        VALUES (%s) 
        RETURNING user_id, current_level
        """, (username,))
        user_id, level = cur.fetchone()
        print(f"Новый игрок {username}! Начинаем с уровня {level}")
    
    conn.commit()
    cur.close()
    conn.close()
    return user_id, level

def get_level_info(level_id):
    """Получение информации об уровне"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT level_name, speed, walls, required_score 
    FROM snake_levels 
    WHERE level_id = %s
    """, (level_id,))
    level = cur.fetchone()
    cur.close()
    conn.close()
    
    if level:
        return {
            'name': level[0],
            'speed': level[1],
            'walls': eval(level[2]),  # Преобразуем строку JSON в список
            'required_score': level[3]
        }
    return None

def save_game_state(user_id, score, level):
    """Сохранение результатов игры"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO snake_scores (user_id, score, level) 
    VALUES (%s, %s, %s)
    """, (user_id, score, level))
    
    # Обновляем уровень пользователя если нужно
    cur.execute("""
    UPDATE snake_users 
    SET current_level = %s 
    WHERE user_id = %s AND current_level < %s
    """, (level, user_id, level))
    
    conn.commit()
    cur.close()
    conn.close()

# Инициализация таблиц при запуске
init_game_tables()

# Пример использования
username = input("Введите ваш игровой ник: ")
user_id, current_level = get_or_create_user(username)
level_info = get_level_info(current_level)

print(f"\nТекущий уровень: {level_info['name']}")
print(f"Скорость: {level_info['speed']}")
print(f"Требуется очков для перехода: {level_info['required_score']}")
print(f"Препятствия: {level_info['walls']}")

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
            self.score += food.weight
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
        self.weight = random.randint(1, 3) # Случайный вес от 1 до 3
        self.timer = random.randint(100, 200) # Случайный таймер
        self.color = self.get_color_by_weight()
    def get_color_by_weight(self):
        if self.weight == 1:
            return colorGREEN # Легкая еда - зеленая
        elif self.weight == 2:
            return colorBLUE # Средняя еда - синяя
        else:
            return colorPURPLE # Тяжелая еда - фиолетовая 
    def update(self):
        # Уменьшение таймера каждый кадр
        self.timer -= 1
        if self.timer <= 0:
            return True # Еда исчезла
        return False      
    # random position
    
    def generate(self, snake):
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)
            # Проверка чтобы еда не появлялась на змее
            if all(segment.x != x or segment.y != y for segment in snake.body):
                self.pos = Point(x, y)
                self.weight = random.randint(1, 3)
                self.timer = random.randint(100, 200)
                self.color = self.get_color_by_weight()
                break

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        timer_text = font.render(str(self.timer // 10), True, colorBLACK)
        screen.blit(timer_text, (self.pos.x * CELL + 5, self.pos.y * CELL + 5))

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
        if food.update():
            food.generate(snake)
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

