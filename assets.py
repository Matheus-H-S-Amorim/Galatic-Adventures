from os import *
import numpy as np
import random
import pygame

# ATALHOS para Pastas com Figuras e Sons 
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')
ANIMACAO_ASTRONA = "animacao_astrona"
BACKGROUND_IMG = 'fundo_jogo'
SOM_FUNDO = "som_fundo"

def load_assets():
    assets = {} # Cria dicionário

    assets[BACKGROUND_IMG] = pygame.image.load(path.join(IMG_DIR, 'fundo\\fundo_planeta_vermelho.png')).convert()
    assets[SOM_FUNDO] = pygame.mixer.Sound(path.join(SND_DIR, 'som_suspense.mp3'))

    animacao_astrona = []
    for i in range(8):
        # Os arquivos de animação são numerados de 00 a 40
        filename = path.join(IMG_DIR, 'astronauta_anda','tile{}.png'.format(i))
        img = pygame.image.load(filename).convert()
        img = pygame.transform.scale(img, (100, 100))
        animacao_astrona.append(img)

    assets[ANIMACAO_ASTRONA] = animacao_astrona
    return assets


### COLOCAR SOM 
#assets[SOM_FUNDO] = pygame.mixer.music.load(os.path.join(SND_DIR, 'som_suspense.mp3')) #pygame.mixer.Sound(os.path.join(SND_DIR, 'sound_suspense_galatic.mp3'))
#pygame.mixer.music.set_volume(0.4)