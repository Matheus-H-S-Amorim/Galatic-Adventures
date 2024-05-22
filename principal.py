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
import numpy as np 

#Tela do Jogo 
WIDTH = 1300                                                  # Largura 
HEIGHT = 650                                                  # Altura 
window = pygame.display.set_mode((WIDTH, HEIGHT))             # Cria Janela com Largura e Altura 
pygame.display.set_caption('Jogo do Astronauta!')             # Título da Janela 

world_speed = -10

#Inicia assests
assets = load_assets() 
player_WIDTH= 100
player_HEIGHT = 100
meteoro_WIDTH = 80         
meteoro_HEIGHT = 80
star_WIDTH = 50
star_HEIGHT = 50 

# Cenario
# background = pygame.image.load('assets/img/fundo/fundo_planeta_vermelho.png').convert()
# background_small= pygame.transform.scale(background, (WIDTH,HEIGHT))
# Personagem 
player_img = pygame.image.load('assets/img/astronauta_anda/tile0.png').convert_alpha()
player_img_small= pygame.transform.scale(player_img, (player_WIDTH, player_HEIGHT))
# Strela 
star_img = pygame.image.load('assets/img/estrela.webp').convert_alpha()
star_img_small= pygame.transform.scale(star_img, (star_WIDTH, star_HEIGHT))
# Meteoro 
meteoro_img = pygame.image.load('assets/img/Meteoro.png').convert_alpha()
meteoro_img_small= pygame.transform.scale(meteoro_img, (meteoro_WIDTH, meteoro_HEIGHT))


################################################## CONFIGURAÇÕES #######################################################################

TAM_PULO = 14
# Atura do chão
CHAO = HEIGHT - 70

# POSSIVEIS ESTADOS DO PLAYER
PARADO = 0                     # Parado 
PULANDO = 1                    # Pulando 
CAINDO = 2                     # Caindo 
ANDANDO = 3 

# Controlador de velocidade do jogo 
FPS = 30

# #Adicionando o placar: 
# score_font = pygame.font.Font(None, 50)
# #Adicionando o placar: 
score_font = pygame.font.Font('assets/font/PressStart2P.ttf', 28)  #Fonte de jogo 


# Inicia jogo 
game = True 

################################################## CLASSES #######################################################################


#Classe do Jogador 
class Player(pygame.sprite.Sprite):
    def __init__(self, img,assets):

        pygame.sprite.Sprite.__init__(self)
        self.gravidade = 2

        self.state = ANDANDO
        
        # Animar player 
        self.indo_direita = False 
        self.indo_esquerda = False  

        self.images = assets[ANIMACAO_ASTRONA]      # Pega lista de frames 
        self.index = 0 
        self.image = self.images[self.index]  
        
        self.rect = self.image.get_rect()           # Área de contato do Player 
        self.rect.centerx = WIDTH/8                 # Centro 
        self.bottom = CHAO                          # Base = GRWOND (para ficar no chao)
        self.rect.top = HEIGHT- player_HEIGHT -500  # Topo 
        self.speedy = 0                             # Velocidade zerada 
        self.speedx = 0 


    def update(self,assets):        

        self.speedy += self.gravidade #GRAVIDADE    # Velocidade de queda é a Gravidade 
        self.rect.y += self.speedy                  # Área de contato do player recebe velocidade e se move 
        self.rect.x += self.speedx

        # Animação a partir de indice de lista de imagens 
        self.index +=1
        if self.index >=len(self.images):
            self.index = 0 
        self.image = self.images[self.index] 
        
        img_n_invertida = self.image

        # Inverte imagem em X 
        if self.indo_esquerda == True: 
            img_invetida_x = pygame.transform.flip (self.image, True, False)
            self.image = img_invetida_x
            # Inverte imagem em Y 
            if self.gravidade<0: 
                img_invetida_y = pygame.transform.flip (self.image, False, True)
                self.image = img_invetida_y
        
        if self.indo_direita == True: 
            self.image = img_n_invertida
            # Inverte imagem em Y 
            if self.gravidade<0: 
                img_invetida_y = pygame.transform.flip (self.image, False, True)
                self.image = img_invetida_y
        # Inverte imagem em Y se liga gravidade parado 
        if self.indo_direita==False and self.indo_esquerda==False and self.gravidade<0: 
            img_invetida_y = pygame.transform.flip (self.image, False, True)
            self.image = img_invetida_y

            
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

        # nao ultrpassa teto e laterais  
        if self.rect.top<0:
            self.speedy = 0
            self.rect.top = -0

        if self.rect.centerx>WIDTH:
            self.rect.centerx = WIDTH
        
        if self.rect.centerx<0: 
            self.rect.centerx = 0
        
    def vira(self): 
        x = 100
        y = 100
        window.blit(pygame.transform.flip (self.image, False, True), (x, y))

    # Método para PULAR 
    def jump(self):
        if self.state == PARADO or self.state == ANDANDO:      
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
        self.area_nascer = np.arange(star_WIDTH, WIDTH+100,50)


        self.state = PARADO 
        self.image = img  
        self.rect = self.image.get_rect() 
        self.rect.centerx = random.choice(self.area_nascer)
        self.bottom = random.randint(0,CHAO)         
        self.rect.top = self.bottom - star_HEIGHT  # Topo 
        self.speedx = -5                           # Velocidade zerada 
        self.speedy = 5                            #Estrela fica parada 

    #ATUALIZANDO A POSIÇÃO DA ESTRELA: 

    def update(self,assets):
        self.rect.centerx += self.speedx
        self.rect.y += self.speedy
        if self.bottom > CHAO or self.rect.right < 0:   #or self.rect.left > WIDTH:
            self.rect.centerx = random.choice(self.area_nascer)
            self.bottom =  random.randint(0,CHAO)       # Base = GRWOND (para ficar no chao)
            self.rect.top = self.bottom - star_HEIGHT   # Topo 
            self.speedx = -5                            # Velocidade zerada 
            self.speedy = 5

        
##Classe dos meteoros: 
class Meteoros(pygame.sprite.Sprite):
    def __init__(self, img,assets):

        pygame.sprite.Sprite.__init__(self) 
        #self.state = PARADO 
        self.image = img  
        self.rect = self.image.get_rect() 
        self.rect.centerx = WIDTH + meteoro_WIDTH  
        self.bottom = random.randint(meteoro_HEIGHT, CHAO) 
        self.rect.top = self.bottom-meteoro_HEIGHT  
        self.speedx = random.choice(([-25,-15]))           # Velocidade em y 
        self.speedy = 1                                    #Velocidade em x  

    #ATUALIZANDO A POSIÇÃO DO METEORO: 

    def update(self,assets):
         self.rect.centerx += self.speedx
         self.rect.y += self.speedy
         if self.rect.top > HEIGHT or self.rect.right < 0:
            self.rect.centerx = WIDTH + meteoro_WIDTH 
            self.bottom = random.randint(meteoro_HEIGHT, CHAO)  
            self.rect.top = self.bottom-meteoro_HEIGHT    
            self.speedx = random.choice([-25,-15,-10])
            self.speedy = 1 

#Cria grupo de Sprites 
all_sprites = pygame.sprite.Group()
all_meteoros = pygame.sprite.Group()
all_stars = pygame.sprite.Group() 

#Cria stars 
# Adicionando mais estrelas:
n_estrelas= 5 

for i in range(n_estrelas): 
    estrela = Stars(star_img_small,assets) 
    all_sprites.add(estrela)  
    all_stars.add(estrela) 

#Cria Meteoros 
# Adicionando mais meteoros: 
n_meteoros =  3  

for i in range(n_meteoros): 
    meteoro = Meteoros(meteoro_img_small,assets) 
    all_sprites.add(meteoro)  
    all_meteoros.add(meteoro) 

# Estados do JOGO 
TELA_INICIAL = 0
JOGANDO = 1
ACABADO = 3 
GAMEOVER = 4
RODANDO = 5
# Fases 
Fase1 = "F1"
Fase2 = "F2"

#################################  LOOP PRINCIPAL    ###############################################################################

modo = TELA_INICIAL

def modo_jogo (window):
    modo = TELA_INICIAL

    while modo != ACABADO:
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    modo = ACABADO

        modo = TELA_INICIAL
        score = 0

        clock = pygame.time.Clock()
        
        assets = load_assets()

        while modo != JOGANDO and modo != GAMEOVER and modo != RODANDO and modo != ACABADO:
            # Vidas 
            vidas = 3

            background = assets[TELADEINICIO]
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    modo = ACABADO

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        modo = JOGANDO
            window.blit(background, (0,0))
            pygame.display.update()

        background = pygame.image.load(path.join(IMG_DIR, 'fundo\\fundo_planeta_vermelho.png')).convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        background_rect = background.get_rect()

        #Cria player  
        player = Player(player_img_small,assets)
        all_sprites.add(player)


        # Som de fundo 
        assets[SOM_FUNDO].play(-1) 
        assets[SOM_FUNDO].set_volume(0.3)

        while modo!= GAMEOVER and modo != RODANDO and modo != TELA_INICIAL and modo != ACABADO:
            # Muda de fase 
            if score>20: 
                background = assets[FUNDO_F2]
                background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            
            if score>40: 
                background = assets[FUNDO_F3]
                background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            
            if score>60: 
                background = assets[FUNDO_F4]
                background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            
            clock.tick(FPS)                 # Velocidade do Jogo

            # Lê o teclado 
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
                        player.indo_esquerda = True
                        player.indo_direita = False 

                    if event.key == pygame.K_RIGHT:
                        player.indo_direita = True 
                        player.indo_esquerda = False 
                        player.speedx += 13

                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT:
                        player.speedx += 13
                        player.vira()

                    if event.key == pygame.K_RIGHT:
                        player.speedx -= 13
                        player.vira()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        player.gravidade*=-1
            
            #COlisao 
            # Estrelas
            estrelas_tocadas = pygame.sprite.spritecollide(player,all_stars,True) 
            if len(estrelas_tocadas)>0: 
                
                # Recria as estrelas
                for estrela_tocada in estrelas_tocadas: 
                    nov_estrela = Stars(star_img_small,assets)
                    all_sprites.add(nov_estrela)
                    all_stars.add(nov_estrela)
                    assets[SOM_STAR].play()
                    assets[SOM_STAR].set_volume(0.2)

                    score+=10 # Muda pontuação 

            # Meteoros 
            meteroros_tocados = pygame.sprite.spritecollide(player,all_meteoros,True)
            if len(meteroros_tocados)>0: 
                vidas -=1 

                # Recria meteoros 
                for meteoro_tocado in meteroros_tocados: 
                    nov_meteoro = Meteoros(meteoro_img_small,assets)
                    all_sprites.add(nov_meteoro)
                    all_meteoros.add(nov_meteoro)
                    assets[SOM_METEORO].play()
                    assets[SOM_METEORO].set_volume(0.2)

                # Player com 3 vidas 
                print(vidas)
                if vidas>0:
                    all_sprites.add(player)

                elif vidas<=0: 
                    player.kill()
                    assets[SOM_GAME_OVER].play()
                    assets[SOM_GAME_OVER].set_volume(1)
                    pygame.time.delay(1000)
                    modo = GAMEOVER
            
                print(vidas)
                print(score)
                
            while modo != TELA_INICIAL and modo != JOGANDO and modo != RODANDO and modo != ACABADO:

                background = assets[TELAFINAL]
                background = pygame.transform.scale(background, (WIDTH, HEIGHT))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        modo = ACABADO

                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                modo = RODANDO

                window.blit(background, (0,0))
                pygame.display.update()

            #####################################################################
            #  MOVER FUNDO            
            window.fill((0,0,0))    

            # Atualiza a posição da imagem de fundo.
            background_rect.x += world_speed

            # Se o fundo saiu da janela, faz ele voltar para dentro.
            if background_rect.right < 0:
                background_rect.x += background_rect.width
            window.blit(background, background_rect)

            # Desenhamos a imagem novamente, mas deslocada da largura da imagem em x.
            background_rect2 = background_rect.copy()
            background_rect2.x += background_rect2.width
            window.blit(background, background_rect2)

            #Desenhando o placar 
            text_surface = score_font.render(str(score), True, (255, 255, 0))
            text_rect = text_surface.get_rect()
            text_rect.midtop = (WIDTH / 2,  10)
            window.blit(text_surface, text_rect)

            # Desenhando as vidas
            text_surface = score_font.render(chr(9829) * vidas, True, (255, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.bottomleft = (10, HEIGHT - 10)
            window.blit(text_surface, text_rect) 
            
            # Para cada loop:
            all_sprites.update(assets)  
            all_sprites.draw(window)                  
            pygame.display.update()
                            

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