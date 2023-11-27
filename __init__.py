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
from . import CONSTANTS, dynamics, audio, state, level_handler, files, graphics, gui, input, variables, events
github = "xxlarytfvwxx"
# set_state = files.set_state
# get_state = files.get_state
Hbtns = False
# state = get_state()
def ON():
    audio.ON()
    pygame.init()
    
def OFF():
    pygame.quit()

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
