import pygame
import os

pygame.init()

screen_width = 550
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Music Player") # Название

# Загрузка фона
background_image = pygame.image.load(r"C:\Users\Adilzhan\Documents\pp2\LAB7\musica_player\background.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Загрузка изображения альбома
monkey_image = pygame.image.load(r"C:\Users\Adilzhan\Documents\pp2\LAB7\musica_player\jeskimonkey.jpeg")

monkey_width, monkey_height = 320, 320
monkey_image = pygame.transform.scale(monkey_image, (monkey_width, monkey_height)) # Меняю размер картинки
monkey_x = 120
monkey_y =  80
# Загрузка а.п
content = pygame.image.load(r"C:\Users\Adilzhan\Documents\pp2\LAB7\musica_player\expcon.jpg")
monkey_width, monkey_height = 50, 40
content = pygame.transform.scale(content, (monkey_width, monkey_height))
content_x = 420
content_y = 395

music_dir = r"C:\Users\Adilzhan\Documents\pp2\LAB7\musica_player\musica"
songs = [song for song in os.listdir(music_dir) if song.endswith(('.mp3'))]
curr_song_ind = 0

pygame.mixer.init()
pygame.mixer.music.load(os.path.join(music_dir, songs[curr_song_ind]))

def play_music():
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def next_song():
    global curr_song_ind
    curr_song_ind = (curr_song_ind + 1) % len(songs)
    pygame.mixer.music.load(os.path.join(music_dir, songs[curr_song_ind]))
    play_music()


def previous_song():
    global curr_song_ind
    curr_song_ind = (curr_song_ind - 1) % len(songs)
    pygame.mixer.music.load(os.path.join(music_dir, songs[curr_song_ind]))
    play_music()

run = True
while run:
    screen.blit(background_image, (0, 0))
    screen.blit(monkey_image, (monkey_x, monkey_y))
    screen.blit(content, (content_x, content_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: # Вверх чтобы воспроизвести
                play_music()
            elif event.key == pygame.K_DOWN: # Стрелка вниз чтобы остановить музыку
                stop_music()
            elif event.key == pygame.K_RIGHT: # Правая стрелка для след.песни
                next_song()
            elif event.key == pygame.K_LEFT: # ЛЕвая стрелка для пред
                previous_song()
            elif event.key == pygame.K_q: # Выход
                run = False

    pygame.display.flip()
