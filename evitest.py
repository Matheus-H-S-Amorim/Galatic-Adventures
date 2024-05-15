from funcoes_do_jogo import *   

pygame.init()
pygame.mixer.init()

try:
    modo_jogo(window)
finally:
    pygame.quit()