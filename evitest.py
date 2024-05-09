# Importando as bibliotecas necessárias.
import pygame
import random
from os import path

pygame.init()
pygame.mixer.init() 

# Estabelece a pasta que contem as figuras e sons.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')

# Dados gerais do jogo.
TITULO = 'Exemplo de Fundo em Movimento'
WIDTH = 1300 # Largura da tela
HEIGHT = 650 # Altura da tela
FPS = 50 # Frames por segundo

#Inicia assests
player_WIDTH= 100
player_HEIGHT = 100
meteoro_WIDTH = 150           #POR IMGS METEORO E ESTRELA
meteoro_HEIGHT = 150
star_WIDTH = 50
star_HEIGHT = 50 

PLAYER_IMG = pygame.image.load('assets/img/astronauta/tile001.png').convert_alpha()
player_img_small= pygame.transform.scale(PLAYER_IMG, (player_WIDTH, player_HEIGHT))

BACKGROUND_IMG = pygame.image.load('assets/img/fundo/fundo_planeta_vermelho.png').convert()
background_small = pygame.transform.scale(BACKGROUND_IMG, (WIDTH,HEIGHT))

BLOCK_IMG = background_small

star_img = pygame.image.load('assets/img/estrela.webp').convert_alpha()
star_img_small= pygame.transform.scale(star_img, (star_WIDTH, star_HEIGHT))

meteoro_img = pygame.image.load('assets/img/Meteoro.png').convert_alpha()
meteoro_img_small= pygame.transform.scale(meteoro_img, (meteoro_WIDTH, meteoro_HEIGHT))


# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define a velocidade inicial do mundo
world_speed = -10

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
        self.speedx = 0   

class Meteoros(pygame.sprite.Sprite):
    def __init__(self, img):

        pygame.sprite.Sprite.__init__(self) 

        self.state = PARADO 
        self.image = img  
        self.rect = self.image.get_rect() 
        self.rect.centerx = WIDTH -200 
        self.bottom = random.randint(0, HEIGHT-meteoro_HEIGHT)                     #HEIGHT -10                # Base = GRWOND (para ficar no chao)
        self.rect.top = self.bottom -  meteoro_HEIGHT       # Topo 
        #self.rect.y = [self.bottom,self.rect.top ]         #Eixo y 
        self.speedy = random.randint(-3, 3)                 # Velocidade em y 
        self.speedx = random.randint(2, 9)                  #Velocidade em x  

    #ATUALIZANDO A POSIÇÃO DO METEORO: 

    def update(self):
         self.rect.centerx += self.speedx
         self.rect.y += self.speedy
         # Se o meteoro passar do final da tela, volta e sorteia novas posições e velocidades
         if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
             self.rect.centerx = random.randint(0, WIDTH-meteoro_WIDTH)
             #self.rect.y = random.randint(-100, -meteoro_HEIGHT)
             self.bottom = random.randint(0, HEIGHT-meteoro_HEIGHT)
             self.rect.top = self.bottom -  meteoro_HEIGHT
             self.speedx = random.randint(-3, 3)
             self.speedy = random.randint(2, 9)

# Outras constantes
all_sprites = pygame.sprite.Group()
all_meteoros = pygame.sprite.Group()
all_stars = pygame.sprite.Group()


star = Stars(star_img_small)
all_sprites.add(star)  
all_stars.add(star)

METEOROS = 8

for i in range(METEOROS): 
    meteoro = Meteoros(meteoro_img_small) 
    all_sprites.add(meteoro)  
    all_meteoros.add(meteoro)     

FUNDOS = 2

TILE_SIZE = 80


# Class que representa os blocos do cenário
class Tile(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, tile_img, x, y, speedx):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Aumenta o tamanho do tile.
        tile_img = pygame.transform.scale(background_small, (TILE_SIZE, TILE_SIZE))

        # Define a imagem do tile.
        self.image = tile_img
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Posiciona o tile
        self.rect.x = x
        self.rect.y = y

        self.speedx = speedx

    def update(self):
        self.rect.x += self.speedx


# Classe Jogador que representa o herói
class Player(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, img):

        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Aumenta o tamanho da imagem
        player_img_small= pygame.transform.scale(PLAYER_IMG, (player_WIDTH, player_HEIGHT))

        # Define a imagem do sprite. Nesse exemplo vamos usar uma imagem estática (não teremos animação durante o pulo)
        self.image = player_img_small
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Começa no centro da janela
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 70

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

        def jump(self):
            if self.state == PARADO:                   # ATIVADO: pulo único            # Desativado: Pulo Múltiplo
                self.speedy -= TAM_PULO
                self.state = PULANDO

# Carrega todos os assets de uma vez.

assets = {}
assets[PLAYER_IMG] = pygame.image.load(path.join(IMG_DIR, 'astronauta.png')).convert_alpha()
assets[BLOCK_IMG] = pygame.image.load(path.join(IMG_DIR, 'fundo_planeta_vermelho.png')).convert()
assets[BACKGROUND_IMG] = pygame.image.load(path.join(IMG_DIR, 'fundo_planeta_vermelho.png')).convert()



def game_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega assets

    # Carrega o fundo do jogo
    background = assets[BACKGROUND_IMG]
    # Redimensiona o fundo
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()

    # Cria Sprite do jogador
    player = Player(assets[PLAYER_IMG])
    # Cria um grupo de todos os sprites e adiciona o jogador.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Cria um grupo para guardar somente os sprites do mundo (obstáculos, objetos, etc).
    # Esses sprites vão andar junto com o mundo (fundo)
    world_sprites = pygame.sprite.Group()
    # Cria blocos espalhados em posições aleatórias do mapa
    for i in range(FUNDOS):
        block_x = random.randint(0, WIDTH)
        block_y = random.randint(0, int(HEIGHT * 0.5))
        block = Tile(assets[BLOCK_IMG], block_x, block_y, world_speed)
        world_sprites.add(block)
        # Adiciona também no grupo de todos os sprites para serem atualizados e desenhados
        all_sprites.add(block)

    PLAYING = 0
    DONE = 1

    state = PLAYING
    while state != DONE:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():

            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = DONE

        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite. O grupo chama o método update() de cada Sprite dentre dele.
        all_sprites.update()

        # Verifica se algum bloco saiu da janela
        for block in world_sprites:
            if block.rect.right < 0:
                # Destrói o bloco e cria um novo no final da tela
                block.kill()
                block_x = random.randint(WIDTH, int(WIDTH * 1.5))
                block_y = random.randint(0, int(HEIGHT * 0.5))
                new_block = Tile(assets[BLOCK_IMG], block_x, block_y, world_speed)
                all_sprites.add(new_block)
                world_sprites.add(new_block)

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        all_sprites.update()                           #Atualiza as ações de todos os sprites 
        window.fill((0,0,0))                           # Pinta fundo de preto 
        window.blit(background_small, (0, 0))          # Plota cenário como background     
        all_sprites.draw(window)                       # Desenha todos os sprites 
        pygame.display.update()        
        # Atualiza a posição da imagem de fundo.
        background_rect.x += world_speed
        # Se o fundo saiu da janela, faz ele voltar para dentro.
        if background_rect.right < 0:
            background_rect.x += background_rect.width
        # Desenha o fundo e uma cópia para a direita.
        # Assumimos que a imagem selecionada ocupa pelo menos o tamanho da janela.
        # Além disso, ela deve ser cíclica, ou seja, o lado esquerdo deve ser continuação do direito.
        screen.blit(background, background_rect)
        # Desenhamos a imagem novamente, mas deslocada da largura da imagem em x.
        background_rect2 = background_rect.copy()
        background_rect2.x += background_rect2.width
        screen.blit(background, background_rect2)

        all_sprites.draw(screen)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()


# Inicialização do Pygame.


# Tamanho da tela.
WIDTH = 1300                                                  # Largura 
HEIGHT = 650 
window = pygame.display.set_mode((WIDTH, HEIGHT))             # Cria Janela com Largura e Altura 

# Nome do jogo
pygame.display.set_caption('Jogo do Astronauta!')             # Título da Janela 

# Imprime instruções
# print('*' * len(TITULO))
# print(TITULO.upper())
# print('*' * len(TITULO))
# print('Este exemplo não é interativo.')

# Comando para evitar travamentos.
try:
    game_screen(window)
finally:
    pygame.quit()
