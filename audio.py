import pygame.mixer
def ON():
    pygame.mixer.pre_init(48000, -16, channels=4)
    pygame.mixer.init()

load_music = pygame.mixer.music.load
get_busy = pygame.mixer.get_busy
play_music = pygame.mixer.music.play
stop_music = pygame.mixer.music.stop
unload = pygame.mixer.music.unload