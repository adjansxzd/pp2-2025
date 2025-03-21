import pygame
import datetime
import sys

pygame.init()

# Настройки экрана
size = (800, 600)
screen = pygame.display.set_mode(size)
clock_center = (400, 300)

# Загружаю файлики
background_img = pygame.image.load(r"C:\Users\Adilzhan\Documents\pp2\LAB7\clock\mickeyclock.png")
seconds = pygame.image.load(r"C:\Users\Adilzhan\Documents\pp2\LAB7\clock\sec_hand.png")
minutes = pygame.image.load(r"C:\Users\Adilzhan\Documents\pp2\LAB7\clock\min_hand.png")

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(background_img, (0, 0))
    # Вычисляем углы и время
    now = datetime.datetime.now()
    minute_angle = -(now.minute * 6) + 90 - 144 
    second_angle = -(now.second * 6) + 90 - 36 

    min_rotated = pygame.transform.rotate(minutes, minute_angle)
    sec_rotated = pygame.transform.rotate(seconds, second_angle)
    min_rect = min_rotated.get_rect(center = clock_center)
    sec_rect = sec_rotated.get_rect(center = clock_center)

    screen.blit(min_rotated, min_rect.topleft)
    screen.blit(sec_rotated, sec_rect.topleft)
    pygame.display.flip() 

pygame.quit()
sys.exit()