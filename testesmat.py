
# INICIALIZAÇÃO 

#Importa e inicia pacotes 
import pygame 
pygame.init()

#Gera tela principal
window = pygame.display.set_mode((600, 300))
pygame.display.set_caption('Jogo do Astronauta!')

# Inicia jogo 
game = True 


# Loop do jogo 
while game: 

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            game = False 
        if event.type== pygame.KEYUP:
            game = False
    
    # Gera saídas
    window.fill((0, 0, 255))  # Preenche com a cor branca

    # Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# Finalização 
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

