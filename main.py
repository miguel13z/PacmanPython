import copy
import pygame
from funcoes import desenha_mapa, desenha_jogador, verifica_posicao, mover_jogador, verifica_colisao, desenha_pontuacao
from mapa import mapa

pygame.init()

largura = 420
altura = 475
tela = pygame.display.set_mode((largura, altura))
temporizador = pygame.time.Clock()
fps = 60
fonte = pygame.font.Font('freesansbold.ttf', 15)
level = copy.deepcopy(mapa)

img_blinky = pygame.transform.scale(pygame.image.load(f'img/fantasmas/red.png'), (20, 20))
img_clyde = pygame.transform.scale(pygame.image.load(f'img/fantasmas/orange.png'), (20, 20))
img_pinky = pygame.transform.scale(pygame.image.load(f'img/fantasmas/pink.png'), (20, 20))
img_inky = pygame.transform.scale(pygame.image.load(f'img/fantasmas/blue.png'), (20, 20))
img_spooked = pygame.transform.scale(pygame.image.load(f'img/fantasmas/powerup.png'), (20, 20))
img_dead = pygame.transform.scale(pygame.image.load(f'img/fantasmas/dead.png'), (20, 20))

jogador_x = 220
jogador_y = 330
direcao = 0

blinky_x = 25
blinky_y = 25
direcao_blinky = 0

inky_x = 200
inky_y = 195
direcao_inky = 2

# o rosa n está aparecendo na tela pq está sendo carregado na mesma posição do clyde

pinky_x = 200
pinky_y = 218
direcao_pinky = 2

clyde_x = 200
clyde_y = 218
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

velocidade_fantasma = 2

contador_inicio = 0
movendo = False
vidas = 3

#Criando a classe Fantasma apenas por enquanto
class Fantasma:
    def __init__(self, coord_x, coord_y, alvo, velocidade, img, direcao, morto, caixa, id):
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.centro_x = self.coord_x + 10
        self.centro_y = self.coord_y + 10
        self.alvo = alvo
        self.velocidade = velocidade
        self.direcao = direcao
        self.morto = morto
        self.img = img
        self.na_caixa = caixa
        self.id = id
        self.vira, self.na_caixa = self.verifica_colisao()
        self.rect = self.desenha()

    def desenha(self):
        if (not powerup and not self.morto) or (fantasmas_mortos[self.id] and powerup and not self.morto):
            tela.blit(self.img, (self.coord_x, self.coord_y))
        elif powerup and not self.morto and not fantasmas_mortos[self.id]:
            tela.blit(img_spooked, (self.coord_x, self.coord_y))
        else:
            tela.blit(img_dead, (self.coord_x, self.coord_y))

        fantasma_rect = pygame.rect.Rect((self.coord_x - 10, self.coord_y - 10), (18, 18))
        return fantasma_rect
    
    def verifica_colisao(self):
        self.vira = [False, False, False, False]
        self.na_caixa = True
        return self.vira, self.na_caixa

rodando = True
while rodando:
    temporizador.tick(fps)
    tela.fill('black')
    desenha_mapa(altura, largura, tela, flicker)
    desenha_jogador(direcao, tela, contador, jogador_x, jogador_y)

    blinky = Fantasma(blinky_x, blinky_y, alvos[0], velocidade_fantasma, img_blinky, direcao_blinky, blinky_morto, blinky_caixa, 0)
    inky = Fantasma(inky_x, inky_y, alvos[1], velocidade_fantasma, img_inky, direcao_inky, inky_morto, inky_caixa, 1)
    pinky = Fantasma(pinky_x, pinky_y, alvos[2], velocidade_fantasma, img_pinky, direcao_pinky, pinky_morto, pinky_caixa, 0)
    clyde = Fantasma(clyde_x, clyde_y, alvos[0], velocidade_fantasma, img_clyde, direcao_clyde, clyde_morto, clyde_caixa, 1)

    desenha_pontuacao(fonte, pontuacao, tela, powerup, vidas)
    centro_x = jogador_x + 10
    centro_y = jogador_y + 10
    pode_virar = verifica_posicao(centro_x, centro_y, largura, altura, direcao, level)
    if movendo:
        jogador_x, jogador_y = mover_jogador(direcao, jogador_x, jogador_y, pode_virar, velocidade)
    pontuacao, powerup, contador_power, fantasmas_mortos = verifica_colisao(altura, largura, jogador_x, level, centro_x, centro_y, pontuacao, powerup, contador_power, fantasmas_mortos)

    if contador < 19:
        contador += 1
        if contador > 3:
            flicker = False
    else:
        contador = 0
        flicker = True

    if powerup and contador_power < 600:
        contador_power += 1
    elif powerup and contador_power >= 600:
        contador_power = 0
        powerup = False
        fantasmas_mortos = [False, False, False]

    if contador_inicio < 180:
        movendo = False
        contador_inicio += 1
    else:
        movendo = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                comando_direcao = 0
            if event.key == pygame.K_LEFT:
                comando_direcao = 1
            if event.key == pygame.K_UP:
                comando_direcao = 2
            if event.key == pygame.K_DOWN:
                comando_direcao = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and comando_direcao == 0:
               comando_direcao = direcao
            if event.key == pygame.K_LEFT and comando_direcao == 1:
               comando_direcao = direcao
            if event.key == pygame.K_UP and comando_direcao == 2:
               comando_direcao = direcao
            if event.key == pygame.K_DOWN and comando_direcao == 3:
               comando_direcao = direcao

    for i in range(4):
        if comando_direcao == i and pode_virar[i]:
            direcao = i

    if jogador_x > largura:
        jogador_x = -23
    elif jogador_x < -25:
        jogador_x = 410

    pygame.display.flip()


pygame.quit()