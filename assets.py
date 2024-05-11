import pygame 
import os 

#from config import IMG_DIR, SND_DIR
from config import *
ANIMACAO_ASTRONA = "animacao_astrona"
BACKGROUND_IMG = 'fundo_jogo'

def load_assets():
    assets = {} # Cria dicionário

    assets[BACKGROUND_IMG] = pygame.image.load(path.join(IMG_DIR, 'fundo\\fundo_planeta_vermelho.png')).convert()


    animacao_astrona = []
    for i in range(8):
        # Os arquivos de animação são numerados de 00 a 40
        filename = os.path.join(IMG_DIR, 'astronauta_anda','tile{}.png'.format(i))
        img = pygame.image.load(filename).convert()
        img = pygame.transform.scale(img, (100, 100))
        animacao_astrona.append(img)

    assets[ANIMACAO_ASTRONA] = animacao_astrona
    return assets