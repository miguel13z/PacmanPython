import pygame
from mapa import mapa
import copy

pygame.init()

LARGURA = 420
ALTURA = 475
tela = pygame.display.set_mode((LARGURA, ALTURA))
temporizador = pygame.time.Clock()
fps = 60
level = copy.deepcopy(mapa)

img_blinky = pygame.transform.scale(pygame.image.load(f'assets/img/fantasmas/red.png'), (20, 20))
img_clyde = pygame.transform.scale(pygame.image.load(f'assets/img/fantasmas/orange.png'), (20, 20))
img_pinky = pygame.transform.scale(pygame.image.load(f'assets/img/fantasmas/pink.png'), (20, 20))
img_inky = pygame.transform.scale(pygame.image.load(f'assets/img/fantasmas/blue.png'), (20, 20))
img_spooked = pygame.transform.scale(pygame.image.load(f'assets/img/fantasmas/powerup.png'), (20, 20))
img_dead = pygame.transform.scale(pygame.image.load(f'assets/img/fantasmas/dead.png'), (20, 20))

jogador_x = 203
jogador_y = 335
direcao = 0

blinky_x = 200
blinky_y = 165
direcao_blinky = 0

inky_x = 175
inky_y = 208
direcao_inky = 2

pinky_x = 225
pinky_y = 208
direcao_pinky = 2

clyde_x = 200
clyde_y = 208
direcao_clyde = 2

contador = 0
flicker = False
pode_virar = [False, False, False, False]
comando_direcao = 0
velocidade = 2
pontuacao = 0
powerup = False
contador_power = 0 
fantasmas_mortos = [False, False, False, False]
alvos = [(jogador_x, jogador_y), (jogador_x, jogador_y), (jogador_x, jogador_y), (jogador_x, jogador_y)]

blinky_morto = False
inky_morto = False
clyde_morto = False
pinky_morto = False

blinky_caixa = False
inky_caixa= False
clyde_caixa = False
pinky_caixa = False

velocidade_fantasma = [0, 0, 0, 0]
contador_inicio = 0
movendo = False
vidas = 3
fim_de_jogo = False
jogo_ganho = False