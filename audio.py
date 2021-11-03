import pygame.mixer
def ON():
    pygame.mixer.pre_init(48000, -16, channels=4)
    pygame.mixer.init()

Load = pygame.mixer.music.load

   