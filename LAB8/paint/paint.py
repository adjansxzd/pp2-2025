import pygame

pygame.init()

FPS = 120
timer = pygame.time.Clock()
WIDTH = 800
HEIGHT = 600
active_shape = "circle"
active_color = "white"
size = 15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint!")
painting = []

def draw_menu(shape, color):
    pygame.draw.rect(screen, "gray", [0, 0, WIDTH, 70])
    pygame.draw.line(screen, "black", (0, 70), (WIDTH, 70), 3)
    shape1 = pygame.draw.rect(screen, "black", [12, 20, 45, 30]) # Rectangle
    shape2 = pygame.draw.circle(screen, "black", (80, 35), radius=20) # Circle
    pygame.draw.circle(screen, color, (400, 35), 30)
    pygame.draw.circle(screen, "dark gray", (400, 35), 30, 3)

    red = pygame.draw.rect(screen, "red", [WIDTH - 35, 10, 25, 25])
    blue  = pygame.draw.rect(screen, "blue", [WIDTH - 35, 35, 25, 25])
    teal = pygame.draw.rect(screen, "teal", [WIDTH - 60, 10, 25, 25])
    yellow = pygame.draw.rect(screen, "yellow", [WIDTH - 60, 35, 25, 25])
    green = pygame.draw.rect(screen, "green", [WIDTH - 85, 10, 25, 25])
    purple = pygame.draw.rect(screen, "purple", [WIDTH - 85, 35, 25, 25])
    black = pygame.draw.rect(screen, "black", [WIDTH - 110, 10, 25, 25])
    white = pygame.draw.rect(screen, "white", [WIDTH - 110, 35, 25, 25])
    plus_button = pygame.draw.rect(screen, "black", [WIDTH - 160, 10, 30, 30])  # +
    minus_button = pygame.draw.rect(screen, "black", [WIDTH - 160, 40, 30, 30]) # -
    font = pygame.font.SysFont("Verdana", 18)
    plus_text = font.render("+", True, "white")
    minus_text = font.render("-", True, "white")
    screen.blit(plus_text, (WIDTH - 150, 15))
    screen.blit(minus_text, (WIDTH - 150, 45))

    shape_list = [shape1, shape2]
    color_rect = [red, blue, teal, yellow, green, purple, black, white]
    rgb_list = [(255, 0, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 255), (255, 255, 255), (0, 0, 0)]


    return shape_list, color_rect, rgb_list, plus_button, minus_button

def draw_painting(paints):
    for paint in paints:
        color, pos, shape, s = paint
        if shape == "circle":
            pygame.draw.circle(screen, color, pos, s)
        elif shape == "rect":
            pygame.draw.rect(screen, color, (pos[0] - s // 2, pos[1] - s, 50, 30))    
    



run = True
while run:
    timer.tick(FPS)
    screen.fill("white")
    mouse = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]

    if left_click and mouse[1] > 70:
        painting.append((active_color, mouse, active_shape, size))

    draw_painting(painting)

    if mouse[1] > 70:
        if active_shape == "circle":
            pygame.draw.circle(screen, active_color, mouse, size)
        elif active_shape == "rect":
            pygame.draw.rect(screen, active_color,(mouse[0] - size // 2, mouse[1] - size // 2, size, size))
    
    shapes, colors, rgbs, plus_btn, minus_btn = draw_menu(active_shape, active_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(shapes)):
                if shapes[i].collidepoint(event.pos):
                    active_shape = "rect" if i == 0 else "circle"
            for i in range(len(colors)):
                if colors[i].collidepoint(event.pos):
                    active_color = rgbs[i]
            if plus_btn.collidepoint(event.pos) and size < 25:
                size += 1
            if minus_btn.collidepoint(event.pos) and size > 1:
                size -= 1        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                if size < 25:
                    size += 1
            if event.key == pygame.K_MINUS:
                if size > 1:
                    size -= 1
    size_text = pygame.font.SysFont("Verdana", 18).render(f"Size: {size}", True, "black")
    screen.blit(size_text, (10, HEIGHT - 30))                        

    pygame.display.flip()
pygame.quit()            