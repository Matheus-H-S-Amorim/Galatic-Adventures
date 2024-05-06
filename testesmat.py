
# INICIALIZAÇÃO 

#Importa e inicia pacotes 
import pygame 
pygame.init()


#Gera tela principal
WIDTH = 1300
HEIGHT = 650
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jogo do Astronauta!')


#Inicia assests
player_WIDTH= 200
player_HEIGHT = 200

font = pygame.font.SysFont(None,48)
background = pygame.image.load('assets/img/fundo_campo.jpg').convert()
background_small= pygame.transform.scale(background, (WIDTH,HEIGHT))

player_img = pygame.image.load('assets/img/astronauta/tile001.png').convert_alpha()
player_img_small= pygame.transform.scale(player_img, (player_WIDTH, player_HEIGHT))


#player configurações
player_x = 0
player_y = HEIGHT-player_HEIGHT-60
player_speedx = 0
player_speedy = 0

# Controlador de velocidade do jogo 
clock = pygame.time.Clock()
FPS = 50



# Inicia jogo 
game = True 


# Loop do jogo 
while game: 
    clock.tick(FPS)  # velocidade do jogo 

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            game = False 

    
    # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                player_speedx -= 8
            if event.key == pygame.K_RIGHT:
                player_speedx += 8
            if event.key == pygame.K_SPACE:
                player_speedy -= 8
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                player_speedx += 8
            if event.key == pygame.K_RIGHT:
                player_speedx -= 8
            if event.key == pygame.K_SPACE:
                player_speedy += 8

    
    # Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca

    player_x += player_speedx
    player_y += player_speedy
    
    window.blit(background_small, (0, 0))                   # plota background 
    window.blit(player_img_small, (player_x, player_y))     #plota personagem


    # Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# Finalização 
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados




