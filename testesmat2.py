
# INICIALIZAÇÃO 

#Importa e inicia pacotes 
import pygame 
pygame.init()
import random

#Gera tela principal
WIDTH = 1300
HEIGHT = 650
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jogo do Astronauta!')


#Inicia assests
player_WIDTH= 200
player_HEIGHT = 200
# METEOR_WIDTH = 200
# METEOR_HEIGHT = 200

background = pygame.image.load('assets/img/fundo_campo.jpg').convert()
background_small= pygame.transform.scale(background, (WIDTH,HEIGHT))

player_img = pygame.image.load('assets/img/astronauta/tile001.png').convert_alpha()
player_img_small= pygame.transform.scale(player_img, (player_WIDTH, player_HEIGHT))


#player configurações
player_x = 0
player_y = HEIGHT-player_HEIGHT-60
player_speedx = 0
player_speedy = 0

# Gravidade
GRAVITY = 2
# Velocidade inicial  pulo
JUMP_SIZE = 30
# Atura do chão
GROUND = HEIGHT * 5 // 6

# Define estados possíveis do jogador
STILL = 0
JUMPING = 1
FALLING = 2


# Controlador de velocidade do jogo 
clock = pygame.time.Clock()
FPS = 50


### CLASSES

#Classe do Jogador 
class Player(pygame.sprite.Sprite):
    def __init__(self, img):

        pygame.sprite.Sprite.__init__(self) # constói classe pai(Sprite)

        # Define estado atual
        self.state = STILL

        self.image = img
        self.rect = self.image.get_rect()
        # Começa no topo da janela e cai até o chão
        self.rect.centerx = WIDTH / 2
        self.rect.top = 0
        self.speedy = 0
        #self.speedx = 0 

        # Método  atualiza a posição do Player
    def update(self):
        self.speedy += GRAVITY

        # Atualiza o estado para caindo
        if self.speedy > 0:
            self.state = FALLING 
        self.rect.y += self.speedy

        # Se bater no chão, para de cair
        if self.rect.bottom > GROUND:
            # Reposiciona para a posição do chão
            self.rect.bottom = GROUND
            # Para de cair
            self.speedy = 0
            # Atualiza o estado para parado
            self.state = STILL
        
    
    #Método pro Player pular 
    def jump(self):
        # Só pula se n tiver pulando ou caindo 
        if self.state == STILL:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING


#game screen
def game_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Cria Sprite do jogador
    player = Player(player_img_small)
    # Cria um grupo de todos os sprites e adiciona o jogador.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)








# Inicia jogo 
game = True 

#Cria grupo de Sprites 
all_sprites = pygame.sprite.Group()
#Cria player  
player = Player(player_img_small)
all_sprites.add(player)

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

        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera o estado do jogador.
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                player.jump()

        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite. O grupo chama o método update() de cada Sprite dentre dele.
        all_sprites.update()

        # A cada loop, redesenha o fundo e os sprites
        window.blit(background_small, (0, 0))  

        # window.fill((0,0,0))
        all_sprites.draw(window)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()


        
        
        # # Atualizando a posição das sprites
        # all_sprites.update()
        
        # #Desenha sprites
        # all_sprites.draw(window)

    
    # Gera saídas
    # window.fill((0, 0, 0))  # Preenche com a cor branca

    
                     # plota background 
    # window.blit(player_img_small, (player_x, player_y))     #plota personagem


    # Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador


# Finalização 
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados




#Classe do Meteoro 
# class Meteoro(pygame.sprite.Sprite):
#     def __init__(self, img):
        
#         # Construtor da classe mãe (Sprite).
#         pygame.sprite.Sprite.__init__(self)

#         self.image = img
#         self.rect = self.image.get_rect()
#         self.rect.x = random.randint(0, WIDTH-METEOR_WIDTH)
#         self.rect.y = random.randint(-100, -METEOR_HEIGHT)
#         self.speedx = random.randint(-3, 3)
#         self.speedy = random.randint(2, 9)

#     def update(self):
#         # Atualizando a posição do meteoro
#         self.rect.x += self.speedx
#         self.rect.y += self.speedy

#         # Se o meteoro passar do final da tela, volta para cima e sorteia
#         # novas posições e velocidades
#         if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
#             self.rect.x = random.randint(0, WIDTH-METEOR_WIDTH)
#             self.rect.y = random.randint(-100, -METEOR_HEIGHT)
#             self.speedx = random.randint(-3, 3)
#             self.speedy = random.randint(2, 9)
