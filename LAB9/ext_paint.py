import pygame

pygame.init()
# Частота кадров 
FPS = 120
timer = pygame.time.Clock()
WIDTH = 800
HEIGHT = 600
active_shape = "circle"
active_color = "white"
size = 15 # Размер кисти 
# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint!")
painting = [] # Список для хранения нарисованныъ элементов

def draw_menu(shape, color):
    # Draw gray menu
    pygame.draw.rect(screen, "gray", [0, 0, WIDTH, 70])
    pygame.draw.line(screen, "black", (0, 70), (WIDTH, 70), 3)

    shape1 = pygame.draw.rect(screen, "black", [12, 20, 45, 30]) # Rectangle
    shape2 = pygame.draw.circle(screen, "black", (80, 35), radius=20) # Circle
    shape3 = pygame.draw.rect(screen, "black", [105, 20, 30, 30]) # Square
    shape4 = pygame.draw.polygon(screen, "black", [(140, 50), (160, 20), (180, 50)]) # Equilateral Triangle
    shape5 = pygame.draw.polygon(screen, "black", [(190, 40), (210, 20), (230, 40), (210, 60)]) # Rhombus

    # Draw indicator
    pygame.draw.circle(screen, color, (400, 35), 30)
    pygame.draw.circle(screen, "dark gray", (400, 35), 30, 3)
    # Кнопки цветов
    red = pygame.draw.rect(screen, "red", [WIDTH - 35, 10, 25, 25])
    blue  = pygame.draw.rect(screen, "blue", [WIDTH - 35, 35, 25, 25])
    teal = pygame.draw.rect(screen, "teal", [WIDTH - 60, 10, 25, 25])
    yellow = pygame.draw.rect(screen, "yellow", [WIDTH - 60, 35, 25, 25])
    green = pygame.draw.rect(screen, "green", [WIDTH - 85, 10, 25, 25])
    purple = pygame.draw.rect(screen, "purple", [WIDTH - 85, 35, 25, 25])
    black = pygame.draw.rect(screen, "black", [WIDTH - 110, 10, 25, 25])
    white = pygame.draw.rect(screen, "white", [WIDTH - 110, 35, 25, 25])
    # Кнопки изменения размера
    plus_button = pygame.draw.rect(screen, "black", [WIDTH - 160, 10, 30, 30])  # +
    minus_button = pygame.draw.rect(screen, "black", [WIDTH - 160, 40, 30, 30]) # -
    font = pygame.font.SysFont("Verdana", 18)
    plus_text = font.render("+", True, "white")
    minus_text = font.render("-", True, "white")
    screen.blit(plus_text, (WIDTH - 150, 15))
    screen.blit(minus_text, (WIDTH - 150, 45))

    shape_list = [shape1, shape2, shape3, shape4, shape5]
    color_rect = [red, blue, teal, yellow, green, purple, black, white]
    rgb_list = [(255, 0, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 255), (255, 255, 255), (0, 0, 0)]


    return shape_list, color_rect, rgb_list, plus_button, minus_button
# Рисовка фигур
def draw_painting(paints):
    for paint in paints:
        color, pos, shape, s = paint
        if shape == "circle":
            pygame.draw.circle(screen, color, pos, s)
        elif shape == "rect":
            pygame.draw.rect(screen, color, (pos[0] - s // 2, pos[1] - s, 50, 30)) 
        elif shape == "square":
            pygame.draw.rect(screen, color, (pos[0] - s // 2, pos[1] - s // 2, s, s))
        elif shape == "right_triangle":
            pygame.draw.polygon(screen, color, [(pos[0], pos[1] - s), (pos[0] - s, pos[1] + s), (pos[0] + s, pos[1] + s)])
        elif shape == "equilateral_triangle":
            pygame.draw.polygon(screen, color, [(pos[0], pos[1] - s), (pos[0] - s, pos[1] + s), (pos[0] + s, pos[1] + s)])
        elif shape == "rhombus":
            pygame.draw.polygon(screen, color, [(pos[0], pos[1] - s), (pos[0] + s, pos[1]), (pos[0], pos[1] + s), (pos[0] - s, pos[1])])       
    


# Main
run = True
while run:
    timer.tick(FPS) # Контроль фпс
    screen.fill("white") # заливка белым
    mouse = pygame.mouse.get_pos() # получение позиции мыши
    left_click = pygame.mouse.get_pressed()[0] # проверка нажатия ЛКМ
    # Добавление новой фигуры при клике
    if left_click and mouse[1] > 70:
        painting.append((active_color, mouse, active_shape, size))

    draw_painting(painting)
    # Предпросмотр фигуры под курсором
    if mouse[1] > 70:
        if active_shape == "circle":
            pygame.draw.circle(screen, active_color, mouse, size)
        elif active_shape == "rect":
            pygame.draw.rect(screen, active_color,(mouse[0] - size // 2, mouse[1] - size // 2, size, size))
        elif active_shape == "square":
            pygame.draw.rect(screen, active_color, (mouse[0] - size // 2, mouse[1] - size // 2, size, size))
        elif active_shape == "equilateral_triangle":
            pygame.draw.polygon(screen, active_color, [(mouse[0], mouse[1] - size), 
                                                   (mouse[0] - size, mouse[1] + size), 
                                                   (mouse[0] + size, mouse[1] + size)])
        elif active_shape == "rhombus":
            pygame.draw.polygon(screen, active_color, [(mouse[0], mouse[1] - size), 
                                                   (mouse[0] + size, mouse[1]), 
                                                   (mouse[0], mouse[1] + size), 
                                                   (mouse[0] - size, mouse[1])])    
            
    # Отрисовка меню и получение кнопок
    shapes, colors, rgbs, plus_btn, minus_btn = draw_menu(active_shape, active_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(shapes)):
                if shapes[i].collidepoint(event.pos):
                    if i == 0:
                        active_shape = "rect"
                    elif i == 1:
                        active_shape = "circle"
                    elif i == 2:
                        active_shape = "square"
                    elif i == 3:
                        active_shape = "equilateral_triangle"
                    elif i == 4:
                        active_shape = "rhombus"  
            # Выбор цвета              
            for i in range(len(colors)):
                if colors[i].collidepoint(event.pos):
                    active_color = rgbs[i]
            # Изменение размера        
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
    # Текущий размер                
    size_text = pygame.font.SysFont("Verdana", 18).render(f"Size: {size}", True, "black")
    screen.blit(size_text, (10, HEIGHT - 30))                        

    pygame.display.flip() # Обновление экрана
pygame.quit()  # и ВЫХОД          