import pygame.draw

ANIMACAO_ASTRONA = "animacao_astrona"
BACKGROUND_IMG = 'fundo_planeta_vermelho.png'
TELADEINICIO = 'tela_inicial'
SOM_FUNDO = 'som_suspense.mp3'
FUNDO_F2 = 'fundo_F2'

#Tela do Jogo (largura e altura)
WIDTH = 1300                                                   
HEIGHT = 650     
#Janela com largura e altura definidas:
window = pygame.display.set_mode((WIDTH, HEIGHT))             
pygame.display.set_caption('Jogo do Astronauta!')             # Título da Janela                                              

BLACK =(0,0,0)

# Frames por segundo:
FPS = 30

# Estados do JOGO 
JOGANDO = 0
ACABADO = 1

#velocidade do mundo:
world_speed = -10    

#medidas iniciais
player_WIDTH= 100
player_HEIGHT = 100
meteoro_WIDTH = 80        
meteoro_HEIGHT = 80
star_WIDTH = 50
star_HEIGHT = 50 

# POSSIVEIS ESTADOS DO PLAYER:
PARADO = 0                      
PULANDO = 1                      
CAINDO = 2                     
ANDANDO = 3 

# Velocidade inicial do pulo:
TAM_PULO = 14
# Atura do chão:
CHAO = HEIGHT - 70

#imagens:
# Cenario
background = pygame.image.load('assets/img/fundo/fundo_planeta_vermelho.png').convert()
background_small= pygame.transform.scale(background, (WIDTH,HEIGHT))
# Personagem 
player_img = pygame.image.load('assets/img/astronauta_anda/tile0.png').convert_alpha()
player_img_small= pygame.transform.scale(player_img, (player_WIDTH, player_HEIGHT))
# Strela 
star_img = pygame.image.load('assets/img/estrela.webp').convert_alpha()
star_img_small= pygame.transform.scale(star_img, (star_WIDTH, star_HEIGHT))
# Meteoro 
meteoro_img = pygame.image.load('assets/img/Meteoro.png').convert_alpha()
meteoro_img_small= pygame.transform.scale(meteoro_img, (meteoro_WIDTH, meteoro_HEIGHT))

#Cria grupo de Sprites 
all_sprites = pygame.sprite.Group()
all_meteoros = pygame.sprite.Group()
all_stars = pygame.sprite.Group()