################################################## INICIALIZAÇÃO #######################################################################

#Importa e inicia os pacotes 
import pygame    
pygame.init()
import random

#Tela do Jogo 
WIDTH = 1300                                                  # Largura 
HEIGHT = 650                                                  # Altura 
window = pygame.display.set_mode((WIDTH, HEIGHT))             # Cria Janela com Largura e Altura 
pygame.display.set_caption('Jogo do Astronauta!')             # Título da Janela 

#Inicia assests
player_WIDTH= 100
player_HEIGHT = 100
meteoro_WIDTH = 150           #POR IMGS METEORO E ESTRELA
meteoro_HEIGHT = 150
star_WIDTH = 50
star_HEIGHT = 50 

background = pygame.image.load('assets/img/fundo_planeta_vermelho.png').convert()
background_small= pygame.transform.scale(background, (WIDTH,HEIGHT))

player_img = pygame.image.load('assets/img/astronauta/tile001.png').convert_alpha()
player_img_small= pygame.transform.scale(player_img, (player_WIDTH, player_HEIGHT))

star_img = pygame.image.load('assets/img/estrela.webp').convert_alpha()
star_img_small= pygame.transform.scale(star_img, (star_WIDTH, star_HEIGHT))

meteoro_img = pygame.image.load('assets/img/Meteoro.png').convert_alpha()
meteoro_img_small= pygame.transform.scale(meteoro_img, (meteoro_WIDTH, meteoro_HEIGHT))


################# CONFIGURACOES 
# Gravidade
GRAVIDADE = 0.7
# Velocidade inicial  pulo
TAM_PULO = 20
# Atura do chão
CHAO = HEIGHT - 70

# POSSIVEIS ESTADOS DO PLAYER
PARADO = 0                       # Parado 
PULANDO = 1                     # Pulando 
CAINDO = 2                     # Caindo 

# Controlador de velocidade do jogo 
clock = pygame.time.Clock()
FPS = 50


################ CLASSES

#Classe do Jogador 
class Player(pygame.sprite.Sprite):
    def __init__(self, img):

        pygame.sprite.Sprite.__init__(self) # constói classe mAe (Sprite)

        self.state = PARADO                         # Estado do Player              # Player Parado 
        self.image = img                            # Imagemn 
        self.rect = self.image.get_rect()           # Área de contato do Player 
        self.rect.centerx = WIDTH/8    #  WIDTH//2  # Centro 
        self.bottom = HEIGHT - 70                   # Base = GRWOND (para ficar no chao)
        self.rect.top = HEIGHT - player_HEIGHT      # Topo 
        self.speedy = 0                             # Velocidade zerada 
        self.speedx = 0 #tirar dps pq n mexe em x


    # Atualiza Posição do Player
    def update(self):
        self.speedy += GRAVIDADE                      # Velocidade de queda é a Gravidade 
        self.rect.y += self.speedy                  # Área de contato do player recebe velocidade e se move 

        self.rect.x += self.speedx

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
    
    # Método para PULAR 
    def jump(self):
        if self.state == PARADO:                   # ATIVADO: pulo único            # Desativado: Pulo Múltiplo
            self.speedy -= TAM_PULO
            self.state = PULANDO

##Classe das estrelas: 
class Stars(pygame.sprite.Sprite):
    def __init__(self, img):

        pygame.sprite.Sprite.__init__(self) 

        self.state = PARADO 
        self.image = img  
        self.rect = self.image.get_rect() 
        self.rect.centerx = WIDTH-200 
        self.bottom = HEIGHT - 60                   # Base = GRWOND (para ficar no chao)
        self.rect.top = HEIGHT - 120                # Topo 
        self.speedy = 0                             # Velocidade zerada 
        self.speedx = 0                             #Estrela fica parada 

##Classe dos meteoros: 
class Meteoros(pygame.sprite.Sprite):
    def __init__(self, img):

        pygame.sprite.Sprite.__init__(self) 

        self.state = PARADO 
        self.image = img  
        self.rect = self.image.get_rect() 
        self.rect.centerx = WIDTH-200 
        self.bottom = HEIGHT -10                # Base = GRWOND (para ficar no chao)
        self.rect.top = HEIGHT - 300            # Topo 
        self.speedy = 0                         # Velocidade zerada 
        self.speedx = 0                         #Estrela fica parada 

# Inicia jogo 
game = True 

#Cria grupo de Sprites 
all_sprites = pygame.sprite.Group()
all_meteoros = pygame.sprite.Group()
all_stars = pygame.sprite.Group() 

#Cria player  
player = Player(player_img_small)
all_sprites.add(player) 

#Cria stars 
star = Stars(star_img_small)
all_sprites.add(star)  
all_stars.add(star) 

#Cria Meteoros 
# meteoros = Meteoros(meteoro_img_small) 
# all_sprites.add(meteoros)  
# all_meteoros.add(meteoros) 

# Adicionando mais meteoros: 
n_meteoros = 8

for i in range(n_meteoros): 
    meteoro = Meteoros(meteoro_img_small) 
    all_sprites.add(meteoro)  
    all_meteoros.add(meteoro) 

# Cria meteoros                                         <<----------------- FAZER METEOROS E ESTRELAS
#or i in range (8): criar meterorosss V12 linha 119

# Estados do JOGO 
JOGANDO = 0
ACABADO = 1

#################################  LOOP PRINCIPAL    ###############################################################################
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
            if event.key == pygame.K_LEFT:
                player.speedx -= 8
            if event.key == pygame.K_RIGHT:
                player.speedx += 8

        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                player.speedx += 8
            if event.key == pygame.K_RIGHT:
                player.speedx -= 8
        #####################################################################
    

    # Para cada loop:
    all_sprites.update()                           #Atualiza as ações de todos os sprites 
    window.fill((0,0,0))                           # Pinta fundo de preto 
    window.blit(background_small, (0, 0))          # Plota cenário como background     
    all_sprites.draw(window)                       # Desenha todos os sprites 
    pygame.display.update()                        # Mostra novo frame com altereações # Dá para usar pygame.display.flip() também  


###################################################### FINALIZAÇÃO ##################################################################
pygame.quit()  # Finaliza o jogo cancelando todos os recursos que foram utilizados aqui no joguinhoo