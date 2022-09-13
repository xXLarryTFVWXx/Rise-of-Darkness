"""
            If you are reading this, you are a code digger.
            Now, I want to congratulate you,
            but I can't, not without letting you in on secrets.

            Please just go back to enjoying the game,
            This has taken literal years of my starting, changing and giving up,
            I don't want to see my project ruined
            because someone wanted to either see the code and reveal secrets
            or make their own modded version of this game.

            Yes, I am well aware of the possibility that you might be making your own modded version of the game.
            Please hear me out on this, go ahead and make your own version of the game,
            I only ask you to not change the core features, go ahead and add your own.
            Small tweaks to the core features are fine, but something that can end up being overpowered isn't.
            Keep things balanced, if you find that something in the core game is overpowered,
            please contact me via github, or maybe tumblr if I get one
            If you do end up making your own modded version of this game, you may show your friends,
            but please don't redistribute it to the general public,
            I don't want this to go crazy and become something different than my vision.
            I literally just want to share this with you.

            If you do show this to your friends, please tell them it is an unauthorized mod of this game.
            I really don't want someone to think that someone's morrally wrong game is attributed to this game.
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
