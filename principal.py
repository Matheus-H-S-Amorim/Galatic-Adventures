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

#Adicionando o placar: 
score_font = pygame.font.Font(None, 50)  #Fonte de jogo 

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
        self.gravidade = 2

        self.state = ANDANDO #PARADO                         # Estado do Player              # Player Parado 
        
        # Animar player 
        self.indo_direita = False 
        self.indo_esquerda = False  

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

        # Animação a partir de indice de lista de imagens 
        self.index +=1
        if self.index >=len(self.images):
            self.index = 0 
        self.image = self.images[self.index] 
        
        img_n_invertida = self.image

        # Inverte imagem em Y 
        if self.gravidade<0: 
            x = 100
            y = 100
            img_invetida_y = pygame.transform.flip (self.image, False, True)
            self.image = img_invetida_y
        
        # Inverte imagem em X 
        if self.indo_esquerda == True: 
            img_invetida_x = pygame.transform.flip (self.image, True, False)
            self.image = img_invetida_x
        
        if self.indo_direita == True: 
            self.image = img_n_invertida
        
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
        
    def vira(self): 
        x = 100
        y = 100
        window.blit(pygame.transform.flip (self.image, False, True), (x, y))

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
        self.area_nascer = np.arange(star_WIDTH, WIDTH+100,50)


        self.state = PARADO 
        self.image = img  
        self.rect = self.image.get_rect() 
        self.rect.centerx = random.choice(self.area_nascer)
        self.bottom = random.randint(0,CHAO)                   # Base = GRWOND (para ficar no chao)
        self.rect.top = self.bottom - star_HEIGHT   # Topo 
        self.speedx = -5                            # Velocidade zerada 
        self.speedy = 5                           #Estrela fica parada 

    #ATUALIZANDO A POSIÇÃO DA ESTRELA: 

    def update(self,assets):
        self.rect.centerx += self.speedx
        self.rect.y += self.speedy
        # Se o estrela passar do final da tela, volta e sorteia novas posições e velocidades
        if self.bottom > CHAO or self.rect.right < 0: #or self.rect.left > WIDTH:
            self.rect.centerx = random.choice(self.area_nascer)
            self.bottom =  random.randint(0,CHAO)                # Base = GRWOND (para ficar no chao)
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
        self.bottom = random.randint(meteoro_HEIGHT, CHAO)                      #random.randint(0, HEIGHT-(500+meteoro_HEIGHT))    #HEIGHT -10    # Base = GRWOND (para ficar no chao)
        self.rect.top = self.bottom-meteoro_HEIGHT                                   #self.bottom -  meteoro_HEIGHT       # Topo 
        #self.rect.y = [self.bottom,self.rect.top ]         #Eixo y 
        self.speedx = random.choice(([-25,-15]))             # Velocidade em y 
        self.speedy = 1 #random.randint(2, 7)                  #Velocidade em x  

    #ATUALIZANDO A POSIÇÃO DO METEORO: 

    def update(self,assets):
         self.rect.centerx += self.speedx
         self.rect.y += self.speedy
         # Se o meteoro passar do final da tela, volta e sorteia novas posições e velocidades
         if self.rect.top > HEIGHT or self.rect.right < 0: # or self.rect.left > WIDTH:
            self.rect.centerx = WIDTH + meteoro_WIDTH #random.randint(0, WIDTH-meteoro_WIDTH)
            #self.rect.y = random.randint(-100, -meteoro_HEIGHT)
            self.bottom = random.randint(meteoro_HEIGHT, CHAO)                      #random.randint(0, HEIGHT-(500+meteoro_HEIGHT))    #HEIGHT -10    # Base = GRWOND (para ficar no chao)
            self.rect.top = self.bottom-meteoro_HEIGHT    
            self.speedx = random.choice([-25,-15,-10])
            self.speedy = 1 

#Cria grupo de Sprites 
all_sprites = pygame.sprite.Group()
all_meteoros = pygame.sprite.Group()
all_stars = pygame.sprite.Group() 

#Cria stars 
# Adicionando mais estrelas:
n_estrelas= 5 #7

for i in range(n_estrelas): 
    estrela = Stars(star_img_small,assets) 
    all_sprites.add(estrela)  
    all_stars.add(estrela) 

#Cria Meteoros 
# Adicionando mais meteoros: 
n_meteoros =  3 #5 

for i in range(n_meteoros): 
    meteoro = Meteoros(meteoro_img_small,assets) 
    all_sprites.add(meteoro)  
    all_meteoros.add(meteoro) 

# Estados do JOGO 
JOGANDO = 0
ACABADO = 1 

# Fases 
Fase1 = "F1"
Fase2 = "F2"

#################################  LOOP PRINCIPAL    ###############################################################################


# window.blit(background_small, (0, 0))          # Plota cenário como background     

def modo_jogo (window):

    #Score inicial 
    score = 0

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

    # Vidas 
    vidas = 3 

    modo = JOGANDO

    # Som de fundo 
    assets[SOM_FUNDO].play(-1) 

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
                    player.indo_esquerda = True
                    player.indo_direita = False 
                    #player.state = ANDANDO

                if event.key == pygame.K_RIGHT:
                    player.indo_direita = True 
                    player.indo_esquerda = False 
                    player.speedx += 13
                    #player.state = ANDANDO

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
        estrelas_tocadas = pygame.sprite.spritecollide(player,all_stars,True)  # lista de estrelas tocadas por player q saiem de all_stars
        if len(estrelas_tocadas)>0: 
            # Recria as estrelas
            for estrela_tocada in estrelas_tocadas: 
                nov_estrela = Stars(star_img_small,assets)   ############ criar nv estrela e por em grupos  E MSM COM METEORORS<----
                all_sprites.add(nov_estrela)
                all_stars.add(nov_estrela)
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

            # Player com 3 vidas 
            print(vidas)
            if vidas>0:
                all_sprites.add(player)

            elif vidas<=0: 
                player.kill()
                modo = ACABADO
        

            print(vidas)
            print(score)
            
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

        #Desenhando o placar 
        text_surface = score_font.render(str(score), True, (255, 255, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        window.blit(text_surface, text_rect)
        
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
