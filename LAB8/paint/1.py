import pygame

pygame.init()

FPS = 120
timer = pygame.time.Clock()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint!")

# Default settings
color = "black"
thickness = 5
tool = "circle"  # 'circle', 'rect', 'eraser'

# Colors and positions for color selection
colors = ["black", "red", "green", "blue", "yellow", "purple"]
color_rects = []

def draw_menu():
    pygame.draw.rect(screen, "gray", [0, 0, WIDTH, 70])
    pygame.draw.line(screen, "black", (0, 70), (WIDTH, 70), 3)

    # Tool buttons
    rect_button = pygame.draw.rect(screen, "white", [10, 10, 50, 50])
    pygame.draw.rect(screen, "black", [15, 15, 40, 40], 2)
    
    circle_button = pygame.draw.circle(screen, "white", (90, 35), 25)
    pygame.draw.circle(screen, "black", (90, 35), 20, 2)
    
    eraser_button = pygame.draw.rect(screen, "white", [150, 10, 50, 50])
    pygame.draw.line(screen, "black", (155, 15), (195, 55), 4)

    # Color selection buttons
    x = 220
    color_rects.clear()
    for col in colors:
        rect = pygame.draw.rect(screen, col, [x, 20, 30, 30])
        color_rects.append((rect, col))
        x += 40

    return rect_button, circle_button, eraser_button

run = True
drawing = False
last_pos = None

while run:
    timer.tick(FPS)
    screen.fill("white")
    rect_btn, circle_btn, eraser_btn = draw_menu()

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if rect_btn.collidepoint(mouse):
                tool = "rect"
            elif circle_btn.collidepoint(mouse):
                tool = "circle"
            elif eraser_btn.collidepoint(mouse):
                tool = "eraser"
            else:
                for rect, col in color_rects:
                    if rect.collidepoint(mouse):
                        color = col
                drawing = True
                last_pos = mouse

        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # + key
                if thickness < 20:
                    thickness += 1
            elif event.key == pygame.K_MINUS:
                if thickness > 1:
                    thickness -= 1

    # Drawing logic
    if drawing and last_pos:
        if tool == "rect":
            pygame.draw.rect(screen, color, (*mouse, thickness, thickness))
        elif tool == "circle":
            pygame.draw.circle(screen, color, mouse, thickness)
        elif tool == "eraser":
            pygame.draw.circle(screen, "white", mouse, thickness)

    # Display thickness
    thickness_text = pygame.font.SysFont("Verdana", 20).render(f"Thickness: {thickness}", True, "black")
    screen.blit(thickness_text, (WIDTH - 180, 20))

    pygame.display.flip()

pygame.quit()