from sprites import *

def modo_jogo (window):

    clock = pygame.time.Clock()
    
    assets = load_assets()

    # Carrega o fundo do jogo:
    background = pygame.image.load(path.join(IMG_DIR, 'fundo\\fundo_planeta_vermelho.png')).convert()#assets[BACKGROUND_IMG]
    # Redimensiona o fundo:
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()

    #Cria player: 
    player = Player(player_img_small,assets)
    all_sprites.add(player)

    modo = JOGANDO

    while modo!= ACABADO:
        clock.tick(FPS) # Velocidade do Jogo 

        # Processa todos os eventos que estão acontecendo (mouse, teclado, botão, etc):
        for event in pygame.event.get():
            # Se Fechou Jogo: 
            if event.type == pygame.QUIT:
                modo = ACABADO

            # Se Apertou Tecla:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()

            #Movimentação:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speedx -= 13

                if event.key == pygame.K_RIGHT:
                    player.speedx += 13

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.speedx += 13

                if event.key == pygame.K_RIGHT:
                    player.speedx -= 13
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    player.gravidade*=-1
        
        #Colisão:
        if  pygame.sprite.spritecollide(player,all_stars,True):
            estrela.kill()
        if  pygame.sprite.spritecollide(player,all_meteoros,False):
            player.kill()

        # MOVER FUNDO            
        window.fill((0,0,0)) # Pinta fundo de preto

        # Atualiza fundo:
        background_rect.x += world_speed
        if background_rect.right < 0:
            background_rect.x += background_rect.width
        # Desenha, duplica, redimensiona e torna cíclico o fundo:
        window.blit(background, background_rect)
        background_rect2 = background_rect.copy()
        background_rect2.x += background_rect2.width
        window.blit(background, background_rect2)
        
        # Para cada loop:
        all_sprites.update(assets) #Atualiza as ações de todos os sprites 
        all_sprites.draw(window) # Desenha todos os sprites 
        pygame.display.update() # Mostra novo frame com alterações

    