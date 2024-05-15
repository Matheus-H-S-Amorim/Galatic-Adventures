from condicoes import *

assets = load_assets()

#Classe do Jogador 
class Player(pygame.sprite.Sprite):
    def __init__(self, img,assets):

        #classe mãe:   
        pygame.sprite.Sprite.__init__(self) 

        self.gravidade = 2

        self.state = ANDANDO 
        
        # Animar player 
        self.images = assets[ANIMACAO_ASTRONA]  # Pega lista de frames 
        self.index = 0 
        self.image = self.images[self.index]  

        # Área de contato do Player 
        self.rect = self.image.get_rect()

        # Centro Width/2
        self.rect.centerx = WIDTH/8  
        
        #Manter no chão
        self.bottom = CHAO                   
        self.rect.top = HEIGHT- player_HEIGHT -500 #Topo 
        self.speedy = 0 # Velocidade em y 
        self.speedx = 0 # Velocidade em x

    # Atualiza Posição do Player
    def update(self,assets):
        self.speedy += self.gravidade #GRAVIDADE = elocidade de queda 
        self.rect.y += self.speedy # Área de contato do player recebe velocidade e se move 
        self.rect.x += self.speedx
        self.index +=1
        
        if self.index >=len(self.images):
            self.index = 0 

        self.image = self.images[self.index]

        # Não anima se: parado ou pulando: 
        if self.state==PARADO or self.state==PULANDO or self.state==CAINDO: 
            self.index = 0 
                
        if self.speedy > 0: # Muda estado
            self.state = CAINDO  
            
        # Se bater no chão, para de cair:
        if self.rect.bottom > CHAO:
            # Reposiciona para a posição do chão:
            self.rect.bottom = CHAO
            # Para de cair:
            self.speedy = 0
            # Atualiza o estado para parado:
            self.state = ANDANDO

        # Não ultrapassa teto e laterais: 
        if self.rect.top<0:
            self.speedy = 0
            self.rect.top = -0

        if self.rect.centerx > WIDTH:
            self.rect.centerx = WIDTH
        
        if self.rect.centerx<0: 
            self.rect.centerx = 0

    # Método para PULAR: 
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
        self.bottom = random.randint(0,CHAO) # Base = GRWOND (para ficar no chao)
        self.rect.top = self.bottom - star_HEIGHT # Topo 
        self.speedx = -5 # Velocidade em x
        self.speedy = 5 # Velocidade em y 

    #ATUALIZANDO A POSIÇÃO DA ESTRELA: 
    def update(self,assets):
        self.rect.centerx += self.speedx
        self.rect.y += self.speedy

        # Se a estrela passar do final da tela, volta e sorteia novas posições e velocidades:
        if self.bottom > CHAO or self.rect.right < 0: 
            self.rect.centerx = random.choice(self.area_nascer)
            self.bottom =  random.randint(0,CHAO) # Base = GRWOND (para ficar no chao)
            self.rect.top = self.bottom - star_HEIGHT # Topo 
            self.speedx = -5 # Velocidade em x
            self.speedy = 5 # velocidade em y

#Classe dos meteoros: 
class Meteoros(pygame.sprite.Sprite):
    def __init__(self, img,assets):

        pygame.sprite.Sprite.__init__(self) 
        self.image = img  
        self.rect = self.image.get_rect() 
        self.rect.centerx = WIDTH + meteoro_WIDTH  
        self.bottom = random.randint(meteoro_HEIGHT, CHAO)
        self.rect.top = self.bottom-meteoro_HEIGHT
        self.speedx = random.choice(([-25,-15])) # Velocidade em x 
        self.speedy = 1 #Velocidade em y 

    #ATUALIZANDO A POSIÇÃO DO METEORO: 
    def update(self,assets):
         self.rect.centerx += self.speedx
         self.rect.y += self.speedy
         # Se o meteoro passar do final da tela, volta e sorteia novas posições e velocidades:
         if self.rect.top > HEIGHT or self.rect.right < 0: 
            self.rect.centerx = WIDTH + meteoro_WIDTH
            self.bottom = random.randint(meteoro_HEIGHT, CHAO)
            self.rect.top = self.bottom-meteoro_HEIGHT    
            self.speedx = random.choice([-25,-15,-10])
            self.speedy = 1 

# Adicionando mais estrelas:
n_estrelas= 5

for i in range(n_estrelas): 
    estrela = Stars(star_img_small,assets) 
    all_sprites.add(estrela)  
    all_stars.add(estrela) 

# Adicionando mais meteoros: 
n_meteoros = 3

for i in range(n_meteoros): 
    meteoro = Meteoros(meteoro_img_small,assets) 
    all_sprites.add(meteoro)  
    all_meteoros.add(meteoro)

#iniciar assets:
assets = load_assets()