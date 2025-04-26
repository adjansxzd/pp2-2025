import pygame
import random
import psycopg2
from color_palette import *

def init_db():
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='BBJN1227',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()
    
    cur.execute("DROP TABLE IF EXISTS snake_scores CASCADE")
    cur.execute("DROP TABLE IF EXISTS snake_users CASCADE")
    
    # Create users table 
    cur.execute("""
    CREATE TABLE snake_users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        high_score INTEGER DEFAULT 0,
        current_level INTEGER DEFAULT 1,
        last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # Create scores table
    cur.execute("""
    CREATE TABLE snake_scores (
        score_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES snake_users(user_id),
        score INTEGER NOT NULL,
        level INTEGER NOT NULL,
        game_data TEXT,
        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    conn.commit()
    cur.close()
    conn.close()

def get_db_connection():
    return psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='BBJN1227',
        host='localhost',
        port='5432'
    )


def get_or_create_user(username):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
        SELECT user_id, current_level, high_score 
        FROM snake_users 
        WHERE username = %s
        """, (username,))
        user = cur.fetchone()
        
        if user:
            user_id, level, high_score = user
            print(f"Welcome back, {username}! Level: {level}, High Score: {high_score}")
        else:
            cur.execute("""
            INSERT INTO snake_users (username) 
            VALUES (%s) 
            RETURNING user_id, current_level, high_score
            """, (username,))
            user_id, level, high_score = cur.fetchone()
            print(f"New user created! Starting at level {level}")
        
        cur.execute("""
        UPDATE snake_users 
        SET last_played = CURRENT_TIMESTAMP 
        WHERE user_id = %s
        """, (user_id,))
        
        conn.commit()
        return user_id, level
        
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
        return None, 1  
        
    finally:
        cur.close()
        conn.close()

def save_game_state(user_id, score, level, snake_body):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        game_data = f"{score},{level},{';'.join(f'{p.x},{p.y}' for p in snake_body)}"
        
        cur.execute("""
        INSERT INTO snake_scores (user_id, score, level, game_data) 
        VALUES (%s, %s, %s, %s)
        """, (user_id, score, level, game_data))
        
        cur.execute("""
        UPDATE snake_users 
        SET high_score = GREATEST(high_score, %s),
            current_level = %s
        WHERE user_id = %s
        """, (score, level, user_id))
        
        conn.commit()
    except Exception as e:
        print(f"Error saving game: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

# Initialize database with clean tables
init_db()


username = input("Enter your username: ")
user_id, current_level = get_or_create_user(username)


if user_id is None:
    print("Using default values due to error")
    current_level = 1

pygame.init()
WIDTH, HEIGHT = 600, 600
CELL = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)


LEVELS = {
    1: {'speed': 7, 'walls': []},
    2: {'speed': 10, 'walls': [[100,100,200,20], [400,300,200,20]]},
    3: {'speed': 13, 'walls': [[50,50,20,300], [300,150,300,20], [200,350,200,20]]}
}

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self):
        pygame.draw.rect(screen, colorBLUE, self.rect)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.score = 0
        self.level = current_level
    
    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy
    
    def draw(self):
        for i, segment in enumerate(self.body):
            color = colorRED if i == 0 else colorYELLOW
            pygame.draw.rect(screen, color, (segment.x * CELL, segment.y * CELL, CELL, CELL))
    
    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.body.append(Point(head.x, head.y))
            self.score += food.weight
            if self.score >= self.level * 10:  # Level up every 10 points
                self.level = min(self.level + 1, 3)
            return True
        return False
    
    def check_wall_collision(self, walls):
        head = self.body[0]
        # Screen boundaries
        if head.x < 0 or head.x >= WIDTH//CELL or head.y < 0 or head.y >= HEIGHT//CELL:
            return True
        
        # Wall collisions
        head_rect = pygame.Rect(head.x * CELL, head.y * CELL, CELL, CELL)
        for wall in walls:
            if head_rect.colliderect(wall.rect):
                return True
        
        # Self collision
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

class Food:
    def __init__(self):
        self.pos = Point(9, 9)
        self.weight = random.randint(1, 3)
        self.color = colorGREEN if self.weight == 1 else (colorBLUE if self.weight == 2 else colorPURPLE)
    
    def generate(self, snake, walls):
        while True:
            x = random.randint(0, WIDTH//CELL - 1)
            y = random.randint(0, HEIGHT//CELL - 1)
            
            # Check if position is free
            valid = True
            for segment in snake.body:
                if x == segment.x and y == segment.y:
                    valid = False
                    break
            
            if valid:
                # Check wall collisions
                food_rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
                for wall in walls:
                    if food_rect.colliderect(wall.rect):
                        valid = False
                        break
            
            if valid:
                self.pos = Point(x, y)
                self.weight = random.randint(1, 3)
                self.color = colorGREEN if self.weight == 1 else (colorBLUE if self.weight == 2 else colorPURPLE)
                break
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

def draw_grid():
    colors = [colorWHITE, colorGRAY]
    for i in range(WIDTH // CELL):
        for j in range(HEIGHT // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

# Game objects
snake = Snake()
food = Food()
walls = [Wall(*wall) for wall in LEVELS[snake.level]['walls']]
food.generate(snake, walls)

# Game state
running = True
game_over = False
paused = False
FPS = LEVELS[snake.level]['speed']

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Pause with P key
                paused = not paused
                if paused:
                    save_game_state(user_id, snake.score, snake.level, snake.body)
            
            if not paused and not game_over:
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
    
    if not game_over and not paused:
        snake.move()
        
        # Check collisions
        if snake.check_wall_collision(walls):
            game_over = True
            save_game_state(user_id, snake.score, snake.level, snake.body)
        
        if snake.check_collision(food):
            food.generate(snake, walls)
        
        # Update level if changed
        if snake.level != current_level:
            current_level = snake.level
            walls = [Wall(*wall) for wall in LEVELS[snake.level]['walls']]
            FPS = LEVELS[snake.level]['speed']
    
    # Drawing
    screen.fill(colorBLACK)
    draw_grid()
    
    # Draw walls
    for wall in walls:
        wall.draw()
    
    snake.draw()
    food.draw()
    
    
    score_text = font.render(f"Score: {snake.score}", True, colorBLACK)
    level_text = font.render(f"Level: {snake.level}", True, colorBLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    
    if paused:
        pause_text = font.render("PAUSED (Press P to resume)", True, colorRED)
        screen.blit(pause_text, (WIDTH//2 - 150, HEIGHT//2))
    
    if game_over:
        game_over_text = font.render("GAME OVER - Press R to restart", True, colorRED)
        screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            snake.reset()
            walls = [Wall(*wall) for wall in LEVELS[snake.level]['walls']]
            food.generate(snake, walls)
            game_over = False
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()