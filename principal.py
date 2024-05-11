################################################## INICIALIZAÇÃO #######################################################################

#Importa e inicia os pacotes 
import pygame
import pygame.draw    
pygame.init()
import random
import assets 
from assets import load_assets,ANIMACAO_ASTRONA

# import assets 
from assets import *
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
meteoro_WIDTH = 125         
meteoro_HEIGHT = 125
star_WIDTH = 50
star_HEIGHT = 50 

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


################# CONFIGURACOES 
# Gravidade
# GRAVIDADE = 2                     #Gravidade comentada virou ATRIBUTO DO PLAYER
# Velocidade inicial  pulo
TAM_PULO = 14
# Atura do chão
CHAO = HEIGHT - 70

# POSSIVEIS ESTADOS DO PLAYER
PARADO = 0                       # Parado 
PULANDO = 1                     # Pulando 
CAINDO = 2                     # Caindo 
ANDANDO = 3 

# Controlador de velocidade do jogo 
FPS = 30


# Inicia jogo 
game = True 

### <<<<<---- VE se ativa ou nao 
# ANIMACAO_ASTRONA = "animacao_astrona"
# BACKGROUND_IMG = 'fundo_jogo'

# def load_assets(IMG_DIR):
#     assets = {} # Cria dicionário
#         # Os arquivos de animação são numerados de 00 a 40
#     assets[ANIMACAO_ASTRONA] = pygame.image.load(path.join(IMG_DIR, 'astronauta_anda/tile0.png')).convert_alpha()    
#     assets[BACKGROUND_IMG] = pygame.image.load(path.join(IMG_DIR, 'fundo\\fundo_planeta_vermelho.png')).convert()
#     return assets
# ################ CLASSES

#Classe do Jogador 
class Player(pygame.sprite.Sprite):
    def __init__(self, img,assets):

        pygame.sprite.Sprite.__init__(self) # constói classe mAe (Sprite)
        self.gravidade = 1.5

        self.state = ANDANDO #PARADO                         # Estado do Player              # Player Parado 
        
        # Animar player 
        self.images = assets[ANIMACAO_ASTRONA]  # Pega lista de frames 
        self.index = 0 
        self.image = self.images[self.index]  
        
        self.rect = self.image.get_rect()           # Área de contato do Player 
        self.rect.centerx = WIDTH/8    #  WIDTH//2  # Centro 
        self.bottom = CHAO                   # Base = GRWOND (para ficar no chao)
        self.rect.top = HEIGHT- player_HEIGHT -500 # Topo 
        self.speedy = 0                             # Velocidade zerada 
        self.speedx = 0 #tirar dps pq n mexe em x

    # Atualiza Posição do Player     <------ SIMPLIFICAR
    def update(self,assets):
        # pygame.draw.rect(window,(0,0,0),self.rect) # ver rect

        self.speedy += self.gravidade #GRAVIDADE                      # Velocidade de queda é a Gravidade 
        self.rect.y += self.speedy                  # Área de contato do player recebe velocidade e se move 
        self.rect.x += self.speedx

        
        self.index +=1
        
        if self.index >=len(self.images):
            self.index = 0 

        self.image = self.images[self.index]

        # Nao faz animacao se tiver parado ou pulando 
        if self.state==PARADO or self.state==PULANDO or self.state==CAINDO: 
            self.index = 0 
                

        if self.speedy > 0:               # Muda estado: Player caindo 
            self.state = CAINDO  
            
        # Se bater no chão, para de cair
        if self.rect.bottom > CHAO:
            # Reposiciona para a posição do chão
            self.rect.bottom = CHAO
            # Para de cair
            self.speedy = 0
            # Atualiza o estado para parado
            self.state = ANDANDO
         
        # Se tiver andando, muda state para andandoo  <<<--- VER SE MANTEM OU N
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        #         self.state = ANDANDO    

        # nao ultrpassa teto e laterais  
        if self.rect.top<0:
            self.speedy = 0
            self.rect.top = -0

        if self.rect.centerx>WIDTH:
            self.rect.centerx = WIDTH
        
        if self.rect.centerx<0: 
            self.rect.centerx = 0

    # Método para PULAR 
    def jump(self):
        if self.state == PARADO or self.state == ANDANDO:                   # ATIVADO: pulo único            # Desativado: Pulo Múltiplo
            self.speedy -= TAM_PULO
            self.state = PULANDO
        if self.state == CAINDO:
            self.speedy -= 2*TAM_PULO - self.gravidade
            self.state = PULANDO
        if self.state == PULANDO:
            self.speedy -= TAM_PULO 
            self.state = PULANDO

##Classe das estrelas: 
class Stars(pygame.sprite.Sprite):
    def __init__(self, img,assets):

        pygame.sprite.Sprite.__init__(self) 

        self.state = PARADO 
        self.image = img  
        self.rect = self.image.get_rect() 
        self.rect.centerx = random.randint(0,(WIDTH))  
        self.bottom = random.randint(0,(HEIGHT-15))                   # Base = GRWOND (para ficar no chao)
        self.rect.top = self.bottom - star_HEIGHT   # Topo 
        self.speedx = 0                             # Velocidade zerada 
        self.speedy = 0                             #Estrela fica parada 

    #ATUALIZANDO A POSIÇÃO DA ESTRELA: 

    def update(self,assets):
         self.rect.centerx += self.speedx
         self.rect.y += self.speedy
         # Se o estrela passar do final da tela, volta e sorteia novas posições e velocidades
         if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
             self.rect.centerx = random.randint(0, WIDTH-star_WIDTH)
             self.bottom = star_HEIGHT 
             self.rect.top = 0
             self.speedx = 0 #random.randint(-3, 3)
             self.speedy = 0 #random.randint(2, 7)  

##Classe dos meteoros: 
class Meteoros(pygame.sprite.Sprite):
    def __init__(self, img,assets):

        pygame.sprite.Sprite.__init__(self) 

        self.state = PARADO 
        self.image = img  
        self.rect = self.image.get_rect() 
        self.rect.centerx = WIDTH -200 
        self.bottom = meteoro_HEIGHT                        #random.randint(0, HEIGHT-(500+meteoro_HEIGHT))    #HEIGHT -10    # Base = GRWOND (para ficar no chao)
        self.rect.top = 0                                   #self.bottom -  meteoro_HEIGHT       # Topo 
        #self.rect.y = [self.bottom,self.rect.top ]         #Eixo y 
        self.speedx = random.randint(-3, -1)                 # Velocidade em y 
        self.speedy = random.randint(2, 7)                  #Velocidade em x  

    #ATUALIZANDO A POSIÇÃO DO METEORO: 

    def update(self,assets):
         self.rect.centerx += self.speedx
         self.rect.y += self.speedy
         # Se o meteoro passar do final da tela, volta e sorteia novas posições e velocidades
         if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
             self.rect.centerx = random.randint(0, WIDTH-meteoro_WIDTH)
             #self.rect.y = random.randint(-100, -meteoro_HEIGHT)
             self.bottom = meteoro_HEIGHT
             self.rect.top = 0
             self.speedx = random.randint(-3, -1)
             self.speedy = random.randint(2, 7)       



#Cria grupo de Sprites 
all_sprites = pygame.sprite.Group()
all_meteoros = pygame.sprite.Group()
all_stars = pygame.sprite.Group() 

#Cria stars 
# Adicionando mais estrelas:
n_estrelas= 7

for i in range(n_estrelas): 
    estrela = Stars(star_img_small,assets) 
    all_sprites.add(estrela)  
    all_stars.add(estrela) 

#Cria Meteoros 
# Adicionando mais meteoros: 
n_meteoros = 5 

for i in range(n_meteoros): 
    meteoro = Meteoros(meteoro_img_small,assets) 
    all_sprites.add(meteoro)  
    all_meteoros.add(meteoro) 

# Estados do JOGO 
JOGANDO = 0
ACABADO = 1

#################################  LOOP PRINCIPAL    ###############################################################################


# window.blit(background_small, (0, 0))          # Plota cenário como background     

def modo_jogo (window):

    clock = pygame.time.Clock()
    
    assets = load_assets()

    # Carrega o fundo do jogo
    background = pygame.image.load(path.join(IMG_DIR, 'fundo\\fundo_planeta_vermelho.png')).convert()#assets[BACKGROUND_IMG]
    # Redimensiona o fundo
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()

    #Cria player  
    player = Player(player_img_small,assets)#assets[ANIMACAO_ASTRONA])
    all_sprites.add(player)

    modo = JOGANDO


    while modo!= ACABADO:
        clock.tick(FPS)                 # Velocidade do Jogo 

        # Gravidade
        # GRAVIDADE = 0.7

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
                if event.key == pygame.K_LEFT:
                    player.speedx -= 13
                    #player.state = ANDANDO

                if event.key == pygame.K_RIGHT:
                    player.speedx += 13
                    #player.state = ANDANDO

            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    player.speedx += 13

                if event.key == pygame.K_RIGHT:
                    player.speedx -= 13
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    player.gravidade*=-1
        
        #COlisao 
        if  pygame.sprite.spritecollide(player,all_stars,True):
            estrela.kill()
        if  pygame.sprite.spritecollide(player,all_meteoros,False):
            player.kill()
            # mortes +=1
            # print(mortes)
            # if mortes>(3*FPS): 
            #     player.kill()
        



        #####################################################################
        #  MOVER FUNDO            
        window.fill((0,0,0))                           # Pinta fundo de preto 

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

        # all_sprites.draw(window)
        
        # Para cada loop:
        all_sprites.update(assets)                #Atualiza as ações de todos os sprites 
        all_sprites.draw(window)                  # Desenha todos os sprites 
        pygame.display.update()                   # Mostra novo frame com altereações # Dá para usar pygame.display.flip() também  
        # pygame.display.flip()

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
