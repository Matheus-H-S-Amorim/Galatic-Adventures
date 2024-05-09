import pygame 
import os 

from config import IMG_DIR, SND_DIR

ANIMACAO_ASTRONA = "animacao_astrona"

def load_assets():
    assets = {} # Cria dicionário

    animacao_astrona = []
    for i in range(3):
        # Os arquivos de animação são numerados de 00 a 40
        filename = os.path.join(IMG_DIR, 'astronauta','tile00{}.png'.format(i))
        img = pygame.image.load(filename).convert()
        img = pygame.transform.scale(img, (200, 200))
        animacao_astrona.append(img)

    assets[ANIMACAO_ASTRONA] = animacao_astrona
    return assets