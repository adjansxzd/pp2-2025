import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Moving Ball")
background = (255, 255, 255)
ball_color = (255, 0, 0)
ball_size = 50
ball_radius = ball_size // 2
ball_x = (800 - ball_size) // 2
ball_y = (600 - ball_size) // 2
ball_speed = 20

def draw_ball(ball_x, ball_y):
    pygame.draw.circle(screen, ball_color, (ball_x , ball_y), 25)  # pygame.draw.circle(surface, color, center, radius, width=0)


done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball_y -= ball_speed
            elif event.key == pygame.K_DOWN:
                ball_y += ball_speed    
            elif event.key == pygame.K_LEFT:
                ball_x -= ball_speed
            elif event.key == pygame.K_RIGHT:
                ball_x += ball_speed
    # Boundaries
    if ball_x < 25:
        ball_x = 25
    elif ball_x > 800 - 25:
        ball_x = 800 - 25
    if ball_y < 25:
        ball_y = 25
    elif ball_y > 600 - 25:
        ball_y = 600 - 25
    screen.fill(background)
    draw_ball(ball_x, ball_y)
    pygame.display.update()
                        
pygame.quit()
