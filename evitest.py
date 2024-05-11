################################################## INICIALIZAÇÃO #######################################################################

#Importa e inicia os pacotes 
import pygame    
pygame.init()
import random
import assets 
from assets import load_assets,ANIMACAO_ASTRONA
from config import *
from os import *

#Tela do Jogo 
WIDTH = 1300                                                  # Largura 
HEIGHT = 650                                                  # Altura 
window = pygame.display.set_mode((WIDTH, HEIGHT))             # Cria Janela com Largura e Altura 
pygame.display.set_caption('Jogo do Astronauta!')             # Título da Janela 

BLACK =(0,0,0)

IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')

world_speed = -10

#Inicia assests
assets = load_assets() 
player_WIDTH= 100
player_HEIGHT = 100
meteoro_WIDTH = 200            #POR IMGS METEORO E ESTRELA
meteoro_HEIGHT = 200
star_WIDTH = 50
star_HEIGHT = 50 

background = pygame.image.load('assets/img/fundo/fundo_planeta_vermelho.png').convert()
background_small= pygame.transform.scale(background, (WIDTH,HEIGHT))

player_img = pygame.image.load('assets/img/astronauta_anda/tile0.png').convert_alpha()
player_img_small= pygame.transform.scale(player_img, (player_WIDTH, player_HEIGHT))

star_img = pygame.image.load('assets/img/estrela.webp').convert_alpha()
star_img_small= pygame.transform.scale(star_img, (star_WIDTH, star_HEIGHT))

meteoro_img = pygame.image.load('assets/img/Meteoro.png').convert_alpha()
meteoro_img= pygame.transform.scale(meteoro_img, (meteoro_WIDTH, meteoro_HEIGHT))


################# CONFIGURACOES 
# Gravidade
GRAVIDADE = 0.7
# Velocidade inicial  pulo
TAM_PULO = 10
# Atura do chão
CHAO = HEIGHT - 70

# POSSIVEIS ESTADOS DO PLAYER
PARADO = 0                       # Parado 
PULANDO = 1                     # Pulando 
CAINDO = 2                     # Caindo 
ANDANDO = 3 

# Controlador de velocidade do jogo 
FPS = 20


# Inicia jogo 
game = True 


ANIMACAO_ASTRONA = "animacao_astrona"
BACKGROUND_IMG = 'fundo_jogo'

# for i in range(8):


def load_assets(IMG_DIR):
    assets = {} # Cria dicionário
        # Os arquivos de animação são numerados de 00 a 40
    assets[ANIMACAO_ASTRONA] = pygame.image.load(path.join(IMG_DIR, 'astronauta_anda/tile0.png')).convert_alpha()    
    assets[BACKGROUND_IMG] = pygame.image.load(path.join(IMG_DIR, 'fundo\\fundo_planeta_vermelho.png')).convert()
    return assets
################ CLASSES

#Classe do Jogador 
class Player(pygame.sprite.Sprite):
    def __init__(self, img_player):

        pygame.sprite.Sprite.__init__(self) # constói classe mAe (Sprite)

        self.state = PARADO                         # Estado do Player              # Player Parado 
        img_player = pygame.transform.scale(img_player, (100, 100))

        # Animar player 
        self.image = assets[ANIMACAO_ASTRONA] # Pega lista de frames 
        self.index = 0 
        self.image = self.image[self.index]  
        
        
        
        self.rect = self.image.get_rect()           # Área de contato do Player 
        self.rect.centerx = WIDTH/8    #  WIDTH//2  # Centro 
        self.bottom = CHAO                   # Base = GRWOND (para ficar no chao)
        self.rect.top = CHAO - player_HEIGHT  # Topo 
        self.speedy = 0                             # Velocidade zerada 
        self.speedx = 0 #tirar dps pq n mexe em x



    # Atualiza Posição do Player     <------ SIMPLIFICAR
    def update(self,assets):
        
        self.speedy += GRAVIDADE                      # Velocidade de queda é a Gravidade 
        self.rect.y += self.speedy                  # Área de contato do player recebe velocidade e se move 
        self.rect.x += self.speedx

        
        self.index +=1
        
        # if self.index >=len(self.images):
        #     self.index = 0 

        # self.images = self.images[self.index]

        # Nao faz animacao se tiver parado ou pulando 
        if self.state==PARADO or self.state==PULANDO: 
            self.index = 0 
                

        if self.rect.bottom > CHAO:               # Muda estado: Player caindo 
            self.state = CAINDO  
            
        # Se bater no chão, para de cair
        if self.rect.bottom > CHAO:
            # Reposiciona para a posição do chão
            self.rect.bottom = CHAO
            # Para de cair
            self.speedy = 0
            # Atualiza o estado para parado
            self.state = PARADO
        
        # Se tiver andando, muda state para andandoo
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.state = ANDANDO    

        # nao ultrpassa teto 
        if self.rect.top<0:
            self.speedy = 0
            self.rect.top = -0

    # Método para PULAR 
    def jump(self):
        # if self.state == PARADO:                   # ATIVADO: pulo único            # Desativado: Pulo Múltiplo
        self.speedy -= TAM_PULO
        self.state = PULANDO

##Classe das estrelas: 
class Stars(pygame.sprite.Sprite):
    def __init__(self, img,assets):

        pygame.sprite.Sprite.__init__(self) 

        self.state = PARADO 
        self.image = img  
        self.rect = self.image.get_rect() 
        self.rect.centerx = WIDTH-200 
        self.bottom = CHAO                   # Base = GRWOND (para ficar no chao)
        self.rect.top = CHAO - star_HEIGHT        # Topo 
        self.speedy = 0                             # Velocidade zerada 
        self.speedx = 0                             #Estrela fica parada 



#Cria grupo de Sprites 
all_sprites = pygame.sprite.Group()
all_meteoros = pygame.sprite.Group()
all_stars = pygame.sprite.Group() 



#Cria stars 
star = Stars(star_img_small,assets)
all_sprites.add(star)  
all_stars.add(star)

# Cria meteoros                                         <<----------------- FAZER METEOROS E ESTRELAS
#or i in range (8): criar meterorosss V12 linha 119

# Estados do JOGO 
JOGANDO = 0
ACABADO = 1

#################################  LOOP PRINCIPAL    ###############################################################################


# window.blit(background_small, (0, 0))          # Plota cenário como background     

def modo_jogo (window):
    GRAVIDADE = 0.7

    clock = pygame.time.Clock()
    
    assets = load_assets(IMG_DIR)

    # Carrega o fundo do jogo
    background = assets[BACKGROUND_IMG]
    # Redimensiona o fundo
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()



    #Cria grupo de Sprites 
    all_sprites = pygame.sprite.Group()
    all_stars = pygame.sprite.Group() 

    #Cria player  
    player = Player(assets[ANIMACAO_ASTRONA])
    all_sprites.add(player)

    #Cria stars 
    star = Stars(star_img_small,assets)
    all_sprites.add(star)  
    all_stars.add(star)

    modo = JOGANDO


    while modo!= ACABADO:
        clock.tick(FPS)                 # Velocidade do Jogo 

        # Processa todos os eventos que estão acontecendo (mouse, teclado, botão, etc).
        for event in pygame.event.get():

            # Se Fechou Jogo 
            if event.type == pygame.QUIT:
                modo = ACABADO        
                    # Se Apertou Tecla 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()

            ##########  MOVIMENTAÇÃO OPCIONAL NO EIXO X ########################
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_g:
                    GRAVIDADE*=-1
                if event.key == pygame.K_LEFT:
                    player.speedx -= 16
                if event.key == pygame.K_RIGHT:
                    player.speedx += 16

            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    player.speedx += 16
                if event.key == pygame.K_RIGHT:
                    player.speedx -= 16
                            
            #all_sprites.update(assets)                          #Atualiza as ações de todos os sprites 

        #COlisao 
        if  pygame.sprite.spritecollide(player,all_stars,True):
            star.kill()

        window.fill(BLACK)

        # background_rect = background.get_rect()

                # Atualiza a posição da imagem de fundo.
        background_rect.x += world_speed
        # Se o fundo saiu da janela, faz ele voltar para dentro.
        if background_rect.right < 0:
            background_rect.x += background_rect.width
        # Desenha o fundo e uma cópia para a direita.
        # Assumimos que a imagem selecionada ocupa pelo menos o tamanho da janela.
        # Além disso, ela deve ser cíclica, ou seja, o lado esquerdo deve ser continuação do direito.
        window.blit(background, background_rect)
        # Desenhamos a imagem novamente, mas deslocada da largura da imagem em x.
        background_rect2 = background_rect.copy()
        background_rect2.x += background_rect2.width
        window.blit(background, background_rect2)

        all_sprites.draw(window)
        all_sprites.update(assets)                   #Atualiza as ações de todos os sprites 

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()


        #####################################################################
    

    # Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
# pygame.display.set_caption(TITULO)

# Comando para evitar travamentos.
try:
    modo_jogo(window)
finally:
    pygame.quit()

    # # Para cada loop:
    # all_sprites.update(assets)                           #Atualiza as ações de todos os sprites 
    # pygame.display.update()   
    # window.fill((0,0,0))                           # Pinta fundo de preto 
    # window.blit(background_small, (0, 0))          # Plota cenário como background     
    # all_sprites.draw(window)                       # Desenha todos os sprites 
    # pygame.display.update()                        # Mostra novo frame com altereações # Dá para usar pygame.display.flip() também  
    # pygame.display.flip()
