"""
            If you are reading this, you are a code digger.
            Now, I want to congratulate you,
            but I can't, not without telling you some things.

            If you are the player, please enjoy whatever game is using this engine,
            after all, that's the primary reason why I'm making this engine,
            so then people can have playing games or making their own if they want to.

            If you are the developer of a game, please keep the above in mind,
            make the game enjoyable for your players, but keep the game's premise in mind.
            Don't be afraid to step out of your comfort region, but you don't have to go too far to get things done.
            Listen to your playerbase, but don't add anything that will either subtract from nor distract the players from the game's premise.
            If you don't know what will subtract from the game's premise, don't be afraid to ask for help.
            If you ever feel burned out while making a game, take a break, 5 minutes, a nap, a day, a few days or even longer,
            just take that break and then don't be afraid to ask people for help.

            This has taken literal years of my starting, changing and giving up,
            I don't want to see my project ruined because someone made something wrong with this engine.
            So in other words I don't want to be held liable for anything you may do with this code.

            Yes, I am well aware of the possibility that you might be making your own modded version of the game.
            Please hear me out on this, go ahead and make your own game with this engine.

            If you find that something in this engine is overpowered or otherwise incorrect,
            please contact me via github, or maybe tumblr if I get one
            If you do make a game with this engine, please don't claim that I had a hand in making your game,
            I only supplied you with the engine.
            
            Official mods may be a possibility in the future, but that is going to be a long ways off.
            Mostly because I have no clue how I can make a way to import information to my game securely.
            I might have an idea or two, but I want this game to be the best game it can be before I release this into the wilds.



            I have been literally writing *just* this comment for over an hour, pouring my heart on this subject out to you.
            
"""
import os, sys, math, functools, pygame
from . import graphics
from . import dynamics
from . import files
from . import gui
from . import audio
from . import math
github = "xxlarytfvwxx"
set_state = files.set_state
get_state = files.get_state
Hbtns = False
state = get_state()

kdict = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "jump": pygame.K_j,
    "action": pygame.K_k,
    "boost": pygame.K_l,
    "esc": pygame.K_ESCAPE,
    "dbg": pygame.K_o,
    "rotate_left": pygame.K_LEFTBRACKET,
    "rotate_right": pygame.K_RIGHTBRACKET
}

def ON():
    audio.ON()
    pygame.init()
    files.set_state(0x00, 0x00)
    
def OFF():
    pygame.quit()

def key_pressed(k=""):
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit() #Failsafe for win7x64py3.3
            pygame.quit()
            sys.exit()
    if sum(keys) > 0:
        if k.lower() in kdict:
            return k == "" or bool(keys[kdict[k.lower()]])
def get_mouse_pos():
    return pygame.mouse.get_pos()


def load_Music(file):
    pygame.mixer_music.load(file)
def play_music(loop=0, t=0.0):
    pygame.mixer_music.play(loop)
def pause_music():
    pygame.mixer_music.pause()
def stop_music():
    pygame.mixer_music.stop()
def get_busy():
    return bool(pygame.mixer_music.get_busy())
def music_volume(vol):
    pygame.mixer_music.set_volume(vol)
def clock():
    return pygame.time.Clock()
