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

jogador_x = 203
jogador_y = 335
direcao = 0

blinky_x = 200
blinky_y = 165
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

velocidade_fantasma = [0, 0, 0, 0]

contador_inicio = 0
movendo = False
vidas = 3
fim_de_jogo = False
jogo_ganho = False

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
        if self.na_caixa:
            tela.blit(self.img, (self.coord_x, self.coord_y))
        elif (not powerup and not self.morto) or (fantasmas_mortos[self.id] and powerup and not self.morto):
            tela.blit(self.img, (self.coord_x, self.coord_y))
        elif powerup and not self.morto and not fantasmas_mortos[self.id]:
            tela.blit(img_spooked, (self.coord_x, self.coord_y))
        else:
            tela.blit(img_dead, (self.coord_x, self.coord_y))

        fantasma_rect = pygame.rect.Rect((self.coord_x - 10, self.coord_y - 10), (18, 18))
        return fantasma_rect
    
    def verifica_colisao(self):
        num1 = altura // 32
        num2 = largura // 30
        num3 = num2 // 2
        self.vira = [False, False, False, False]
        if 0 < self.centro_x // num2 < 29:
            if level[(self.centro_y - num3) // num1][self.centro_x // num2] == 9:
                self.vira[2] = True
            if level[self.centro_y // num1][(self.centro_x - num3) // num2] < 3 \
                    or (level[self.centro_y // num1][(self.centro_x - num3) // num2] == 9 and (
                    self.na_caixa or self.morto)):
                self.vira[1] = True
            if level[self.centro_y // num1][(self.centro_x + num3) // num2] < 3 \
                    or (level[self.centro_y // num1][(self.centro_x + num3) // num2] == 9 and (
                    self.na_caixa or self.morto)):
                self.vira[0] = True
            if level[(self.centro_y + num3) // num1][self.centro_x // num2] < 3 \
                    or (level[(self.centro_y + num3) // num1][self.centro_x // num2] == 9 and (
                    self.na_caixa or self.morto)):
                self.vira[3] = True
            if level[(self.centro_y - num3) // num1][self.centro_x // num2] < 3 \
                    or (level[(self.centro_y - num3) // num1][self.centro_x // num2] == 9 and (
                    self.na_caixa or self.morto)):
                self.vira[2] = True

            centro_tile_x_min = (num2 // 2) - 2
            centro_tile_x_max = (num2 // 2) + 2
            centro_tile_y_min = (num1 // 2) - 2
            centro_tile_y_max = (num1 // 2) + 2

            if self.direcao == 2 or self.direcao == 3:
                if centro_tile_x_min <= self.centro_x % num2 <= centro_tile_x_max:
                    if level[(self.centro_y + num3) // num1][self.centro_x // num2] < 3 \
                            or (level[(self.centro_y + num3) // num1][self.centro_x // num2] == 9 and (
                            self.na_caixa or self.morto)):
                        self.vira[3] = True
                    if level[(self.centro_y - num3) // num1][self.centro_x // num2] < 3 \
                            or (level[(self.centro_y - num3) // num1][self.centro_x // num2] == 9 and (
                            self.na_caixa or self.morto)):
                        self.vira[2] = True
                if centro_tile_y_min <= self.centro_y % num1 <= centro_tile_y_max:
                    if level[self.centro_y // num1][(self.centro_x - num2) // num2] < 3 \
                            or (level[self.centro_y // num1][(self.centro_x - num2) // num2] == 9 and (
                            self.na_caixa or self.morto)):
                        self.vira[1] = True
                    if level[self.centro_y // num1][(self.centro_x + num2) // num2] < 3 \
                            or (level[self.centro_y // num1][(self.centro_x + num2) // num2] == 9 and (
                            self.na_caixa or self.morto)):
                        self.vira[0] = True

            if self.direcao == 0 or self.direcao == 1:
                if centro_tile_x_min <= self.centro_x % num2 <= centro_tile_x_max:
                    if level[(self.centro_y + num3) // num1][self.centro_x // num2] < 3 \
                            or (level[(self.centro_y + num3) // num1][self.centro_x // num2] == 9 and (
                            self.na_caixa or self.morto)):
                        self.vira[3] = True
                    if level[(self.centro_y - num3) // num1][self.centro_x // num2] < 3 \
                            or (level[(self.centro_y - num3) // num1][self.centro_x // num2] == 9 and (
                            self.na_caixa or self.morto)):
                        self.vira[2] = True
                if centro_tile_y_min <= self.centro_y % num1 <= centro_tile_y_max:
                    if level[self.centro_y // num1][(self.centro_x - num3) // num2] < 3 \
                            or (level[self.centro_y // num1][(self.centro_x - num3) // num2] == 9 and (
                            self.na_caixa or self.morto)):
                        self.vira[1] = True
                    if level[self.centro_y // num1][(self.centro_x + num3) // num2] < 3 \
                            or (level[self.centro_y // num1][(self.centro_x + num3) // num2] == 9 and (
                            self.na_caixa or self.morto)):
                        self.vira[0] = True
        else:
            self.vira[0] = True
            self.vira[1] = True

        
        if 190 < self.coord_x < 230 and 190 < self.coord_y < 230:
            self.na_caixa = True
        else:
            self.na_caixa = False

        return self.vira, self.na_caixa
    
    def clyde_movimento(self):
        if self.direcao == 0:
            if self.alvo[0] > self.coord_x and self.vira[0]:
                self.coord_x += self.velocidade
            elif not self.vira[0]:
                if self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
            elif self.vira[0]:
                if self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                if self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                else:
                    self.coord_x += self.velocidade
        elif self.direcao == 1:
            if self.alvo[1] > self.coord_y and self.vira[3]:
                self.direcao = 3
            elif self.alvo[0] < self.coord_x and self.vira[1]:
                self.coord_x -= self.velocidade
            elif not self.vira[1]:
                if self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
            elif self.vira[1]:
                if self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                if self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                else:
                    self.coord_x -= self.velocidade
        elif self.direcao == 2:
            if self.alvo[0] < self.coord_x and self.vira[1]:
                self.direcao = 1
                self.coord_x -= self.velocidade
            elif self.alvo[1] < self.coord_y and self.vira[2]:
                self.direcao = 2
                self.coord_y -= self.velocidade
            elif not self.vira[2]:
                if self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
            elif self.vira[2]:
                if self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                else:
                    self.coord_y -= self.velocidade
        elif self.direcao == 3:
            if self.alvo[1] > self.coord_y and self.vira[3]:
                self.coord_y += self.velocidade
            elif not self.vira[3]:
                if self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
            elif self.vira[3]:
                if self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                else:
                    self.coord_y += self.velocidade

        if self.coord_x > largura:
            self.coord_x = -23
        elif self.coord_x < -25:
            self.coord_x = 410
        return self.coord_x, self.coord_y, self.direcao


    def blinky_movimento(self):
        if self.direcao == 0:
            if self.alvo[0] > self.coord_x and self.vira[0]:
                self.coord_x += self.velocidade
            elif not self.vira[0]:
                if self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
            elif self.vira[0]:
                self.coord_x += self.velocidade
        elif self.direcao == 1:
            if self.alvo[0] < self.coord_x and self.vira[1]:
                self.coord_x -= self.velocidade
            elif not self.vira[1]:
                if self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
            elif self.vira[1]:
                self.coord_x -= self.velocidade
        elif self.direcao == 2:
            if self.alvo[1] < self.coord_y and self.vira[2]:
                self.direcao = 2
                self.coord_y -= self.velocidade
            elif not self.vira[2]:
                if self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
            elif self.vira[2]:
                self.coord_y -= self.velocidade
        elif self.direcao == 3:
            if self.alvo[1] > self.coord_y and self.vira[3]:
                self.coord_y += self.velocidade
            elif not self.vira[3]:
                if self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
            elif self.vira[3]:
                self.coord_y += self.velocidade
        if self.coord_x > largura:
            self.coord_x = -23
        elif self.coord_x < -25:
            self.coord_x = 410
        return self.coord_x, self.coord_y, self.direcao

    def inky_movimento(self):
        if self.direcao == 0:
            if self.alvo[0] > self.coord_x and self.vira[0]:
                self.coord_x += self.velocidade
            elif not self.vira[0]:
                if self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
            elif self.vira[0]:
                if self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                if self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                else:
                    self.coord_x += self.velocidade
        elif self.direcao == 1:
            if self.alvo[1] > self.coord_y and self.vira[3]:
                self.direcao = 3
            elif self.alvo[0] < self.coord_x and self.vira[1]:
                self.coord_x -= self.velocidade
            elif not self.vira[1]:
                if self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
            elif self.vira[1]:
                if self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                if self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                else:
                    self.coord_x -= self.velocidade
        elif self.direcao == 2:
            if self.alvo[1] < self.coord_y and self.vira[2]:
                self.direcao = 2
                self.coord_y -= self.velocidade
            elif not self.vira[2]:
                if self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
            elif self.vira[2]:
                self.coord_y -= self.velocidade
        elif self.direcao == 3:
            if self.alvo[1] > self.coord_y and self.vira[3]:
                self.coord_y += self.velocidade
            elif not self.vira[3]:
                if self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
            elif self.vira[3]:
                self.coord_y += self.velocidade
        if self.coord_x > largura:
            self.coord_x = -23
        elif self.coord_x < -25:
            self.coord_x = 410
        return self.coord_x, self.coord_y, self.direcao

    def pinky_movimento(self):
        if self.direcao == 0:
            if self.alvo[0] > self.coord_x and self.vira[0]:
                self.coord_x += self.velocidade
            elif not self.vira[0]:
                if self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
            elif self.vira[0]:
                self.coord_x += self.velocidade
        elif self.direcao == 1:
            if self.alvo[1] > self.coord_y and self.vira[3]:
                self.direcao = 3
            elif self.alvo[0] < self.coord_x and self.vira[1]:
                self.coord_x -= self.velocidade
            elif not self.vira[1]:
                if self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
            elif self.vira[1]:
                self.coord_x -= self.velocidade
        elif self.direcao == 2:
            if self.alvo[0] < self.coord_x and self.vira[1]:
                self.direcao = 1
                self.coord_x -= self.velocidade
            elif self.alvo[1] < self.coord_y and self.vira[2]:
                self.direcao = 2
                self.coord_y -= self.velocidade
            elif not self.vira[2]:
                if self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.alvo[1] > self.coord_y and self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.vira[3]:
                    self.direcao = 3
                    self.coord_y += self.velocidade
                elif self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
            elif self.vira[2]:
                if self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                else:
                    self.coord_y -= self.velocidade
        elif self.direcao == 3:
            if self.alvo[1] > self.coord_y and self.vira[3]:
                self.coord_y += self.velocidade
            elif not self.vira[3]:
                if self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.alvo[1] < self.coord_y and self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[2]:
                    self.direcao = 2
                    self.coord_y -= self.velocidade
                elif self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                elif self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
            elif self.vira[3]:
                if self.alvo[0] > self.coord_x and self.vira[0]:
                    self.direcao = 0
                    self.coord_x += self.velocidade
                elif self.alvo[0] < self.coord_x and self.vira[1]:
                    self.direcao = 1
                    self.coord_x -= self.velocidade
                else:
                    self.coord_y += self.velocidade
        if self.coord_x > largura:
            self.coord_x = -23
        elif self.coord_x < -25:
            self.coord_x = 410
        return self.coord_x, self.coord_y, self.direcao

def busca_alvos(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if jogador_x < 210:
        fuga_x = 420
    else:
        fuga_x = 0
    if jogador_y < 210:
        fuga_y = 420
    else:
        fuga_y = 0

    local_retorno = (200, 200)
    saida_caixa = (211, 50)

    if powerup:
        if not blinky.morto and not fantasmas_mortos[0]:
            blink_alvo = (fuga_x, fuga_y)
        elif blinky.na_caixa:
            blink_alvo = saida_caixa
        else:
            blink_alvo = local_retorno

        if not inky.morto and not fantasmas_mortos[1]:
            ink_alvo = (fuga_x, jogador_y)
        elif inky.na_caixa:
            ink_alvo = saida_caixa
        else:
            ink_alvo = local_retorno

        if not pinky.morto and not fantasmas_mortos[2]:
            pink_alvo = (jogador_x, fuga_y)
        elif pinky.na_caixa:
            pink_alvo = saida_caixa
        else:
            pink_alvo = local_retorno

        if not clyde.morto and not fantasmas_mortos[3]:
            clyd_alvo = (450, 450)
        elif clyde.na_caixa:
            clyd_alvo = saida_caixa
        else:
            clyd_alvo = local_retorno

    else:
        if not blinky.morto:
            if blinky.na_caixa:
                blink_alvo = saida_caixa
            else:
                blink_alvo = (jogador_x, jogador_y)
        else:
            blink_alvo = local_retorno

        if not inky.morto:
            if inky.na_caixa:
                ink_alvo = saida_caixa
            else:
                ink_alvo = (jogador_x, jogador_y)
        else:
            ink_alvo = local_retorno

        if not pinky.morto:
            if pinky.na_caixa:
                pink_alvo = saida_caixa
            else:
                pink_alvo = (jogador_x, jogador_y)
        else:
            pink_alvo = local_retorno

        if not clyde.morto:
            if clyde.na_caixa:
                clyd_alvo = saida_caixa
            else:
                clyd_alvo = (jogador_x, jogador_y)
        else:
            clyd_alvo = local_retorno

    return [blink_alvo, ink_alvo, pink_alvo, clyd_alvo]


rodando = True
while rodando:
    temporizador.tick(fps)
    tela.fill('black')
    desenha_mapa(altura, largura, tela, flicker, level)
    centro_x = jogador_x + 10
    centro_y = jogador_y + 10
    if powerup:
        velocidade_fantasma = [1, 1, 1, 1]
    else:
        velocidade_fantasma = [2, 2, 2, 2]
    
    if fantasmas_mortos[0]:
        velocidade_fantasma[0] = 2
    if fantasmas_mortos[1]:
        velocidade_fantasma[1] = 2
    if fantasmas_mortos[2]:
        velocidade_fantasma[2] = 2
    if fantasmas_mortos[3]:
        velocidade_fantasma[3] = 2
        
    if blinky_morto:
        velocidade_fantasma[0] = 4
    if inky_morto:
        velocidade_fantasma[1] = 4
    if pinky_morto:
        velocidade_fantasma[2] = 4
    if clyde_morto:
        velocidade_fantasma[3] = 4

    jogo_ganho = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            jogo_ganho = False

    circulo_jogador = pygame.draw.circle(tela, 'black', (centro_x, centro_y), 10, 1)

    desenha_jogador(direcao, tela, contador, jogador_x, jogador_y)
    
    blinky = Fantasma(blinky_x, blinky_y, alvos[0], velocidade_fantasma[0], img_blinky, direcao_blinky, blinky_morto, blinky_caixa, 0)
    inky = Fantasma(inky_x, inky_y, alvos[1], velocidade_fantasma[1], img_inky, direcao_inky, inky_morto, inky_caixa, 1)
    pinky = Fantasma(pinky_x, pinky_y, alvos[2], velocidade_fantasma[2], img_pinky, direcao_pinky, pinky_morto, pinky_caixa, 0)
    clyde = Fantasma(clyde_x, clyde_y, alvos[0], velocidade_fantasma[3], img_clyde, direcao_clyde, clyde_morto, clyde_caixa, 1)

    desenha_pontuacao(fonte, pontuacao, tela, powerup, vidas, fim_de_jogo, jogo_ganho)
    alvos = busca_alvos(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)
    centro_x = jogador_x + 10
    centro_y = jogador_y + 10
    pode_virar = verifica_posicao(centro_x, centro_y, largura, altura, direcao, level)
    if movendo:
        jogador_x, jogador_y = mover_jogador(direcao, jogador_x, jogador_y, pode_virar, velocidade)
        if not blinky_morto and not blinky.na_caixa:
            blinky_x, blinky_y, direcao_blinky = blinky.blinky_movimento()
        else:
            blinky_x, blinky_y, direcao_blinky = blinky.clyde_movimento()

        if not pinky.morto and not pinky.na_caixa:
            pinky_x, pinky_y, direcao_pinky = pinky.pinky_movimento()
        else:
            pinky_x, pinky_y, direcao_pinky = pinky.clyde_movimento()
        
        if not inky.morto and not inky.na_caixa:
            inky_x, inky_y, direcao_inky = inky.inky_movimento()
        else:
            inky_x, inky_y, direcao_inky = inky.clyde_movimento()
        
        clyde_x, clyde_y, direcao_clyde = clyde.clyde_movimento()
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
        fantasmas_mortos = [False, False, False, False]

    if contador_inicio < 180 and not fim_de_jogo and not jogo_ganho:
        movendo = False
        contador_inicio += 1
    else:
        movendo = True


    if not powerup:
        if (circulo_jogador.colliderect(blinky.rect) and not blinky.morto) or \
                (circulo_jogador.colliderect(inky.rect) and not inky.morto) or \
                (circulo_jogador.colliderect(pinky.rect) and not pinky.morto) or \
                (circulo_jogador.colliderect(clyde.rect) and not clyde.morto):
            if vidas > 0:
                vidas -= 1
                powerup = False
                contador_power = 0
                contador_inicio = 0
                jogador_x = 200
                jogador_y = 335
                direcao = 0
                comando_direcao = 0

                blinky_x = 25
                blinky_y = 25
                direcao_blinky = 0

                inky_x = 200
                inky_y = 195
                direcao_inky = 2

                pinky_x = 200
                pinky_y = 218
                direcao_pinky = 2

                clyde_x = 200
                clyde_y = 218
                direcao_clyde = 2

                fantasmas_mortos = [False, False, False, False]
               
                blinky_morto = False
                inky_morto = False
                clyde_morto = False
                pinky_morto = False
            else:
                fim_de_jogo = True
                movendo = False
                contador_inicio = 0

    if powerup and circulo_jogador.colliderect(blinky.rect) and not blinky.morto and not fantasmas_mortos[0]:
        blinky_morto = True
        fantasmas_mortos[0] = True
        pontuacao += 2 ** fantasmas_mortos.count(True) * 100
    if powerup and circulo_jogador.colliderect(inky.rect) and not inky.morto and not fantasmas_mortos[1]:
        inky_morto = True
        fantasmas_mortos[1] = True
        pontuacao += 2 ** fantasmas_mortos.count(True)* 100
    if powerup and circulo_jogador.colliderect(pinky.rect) and not pinky.morto and not fantasmas_mortos[2]:
        pinky_morto = True
        fantasmas_mortos[2] = True
        pontuacao += 2 ** fantasmas_mortos.count(True) * 100
    if powerup and circulo_jogador.colliderect(clyde.rect) and not clyde.morto and not fantasmas_mortos[3]:
        clyde_morto = True
        fantasmas_mortos[3] = True
        pontuacao += 2 ** fantasmas_mortos.count(True) * 100

    if powerup and circulo_jogador.colliderect(blinky.rect) and fantasmas_mortos[0]:
        if vidas > 0:
                vidas -= 1
                powerup = False
                contador_power = 0
                contador_inicio = 0
                jogador_x = 200
                jogador_y = 335
                direcao = 0
                comando_direcao = 0

                blinky_x = 25
                blinky_y = 25
                direcao_blinky = 0

                inky_x = 200
                inky_y = 195
                direcao_inky = 2

                pinky_x = 200
                pinky_y = 218
                direcao_pinky = 2

                clyde_x = 200
                clyde_y = 218
                direcao_clyde = 2

                fantasmas_mortos = [False, False, False, False]
               
                blinky_morto = False
                inky_morto = False
                clyde_morto = False
                pinky_morto = False
        else:
            fim_de_jogo = True
            movendo = False
            contador_inicio = 0
    if powerup and circulo_jogador.colliderect(blinky.rect) and fantasmas_mortos[1]:
        if vidas > 0:
                vidas -= 1
                powerup = False
                contador_power = 0
                contador_inicio = 0
                jogador_x = 200
                jogador_y = 335
                direcao = 0
                comando_direcao = 0

                blinky_x = 25
                blinky_y = 25
                direcao_blinky = 0

                inky_x = 200
                inky_y = 195
                direcao_inky = 2

                pinky_x = 200
                pinky_y = 218
                direcao_pinky = 2

                clyde_x = 200
                clyde_y = 218
                direcao_clyde = 2

                fantasmas_mortos = [False, False, False, False]
               
                blinky_morto = False
                inky_morto = False
                clyde_morto = False
                pinky_morto = False
        else:
            fim_de_jogo = True
            movendo = False
            contador_inicio = 0
    if powerup and circulo_jogador.colliderect(blinky.rect) and fantasmas_mortos[2]:
        if vidas > 0:
                vidas -= 1
                powerup = False
                contador_power = 0
                contador_inicio = 0
                jogador_x = 200
                jogador_y = 335
                direcao = 0
                comando_direcao = 0

                blinky_x = 25
                blinky_y = 25
                direcao_blinky = 0

                inky_x = 200
                inky_y = 195
                direcao_inky = 2

                pinky_x = 200
                pinky_y = 218
                direcao_pinky = 2

                clyde_x = 200
                clyde_y = 218
                direcao_clyde = 2

                fantasmas_mortos = [False, False, False, False]
               
                blinky_morto = False
                inky_morto = False
                clyde_morto = False
                pinky_morto = False
        else:
            fim_de_jogo = True
            movendo = False
            contador_inicio = 0
    if powerup and circulo_jogador.colliderect(blinky.rect) and fantasmas_mortos[3]:
        if vidas > 0:
                vidas -= 1
                powerup = False
                contador_power = 0
                contador_inicio = 0
                jogador_x = 200
                jogador_y = 335
                direcao = 0
                comando_direcao = 0

                blinky_x = 25
                blinky_y = 25
                direcao_blinky = 0

                inky_x = 200
                inky_y = 195
                direcao_inky = 2

                pinky_x = 200
                pinky_y = 218
                direcao_pinky = 2

                clyde_x = 200
                clyde_y = 218
                direcao_clyde = 2

                fantasmas_mortos = [False, False, False, False]
               
                blinky_morto = False
                inky_morto = False
                clyde_morto = False
                pinky_morto = False
        else:
            fim_de_jogo = True
            movendo = False
            contador_inicio = 0

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
            if event.key == pygame.K_SPACE and (fim_de_jogo or jogo_ganho):
                vidas -= 1
                powerup = False
                contador_power = 0
                contador_inicio = 0
                jogador_x = 200
                jogador_y = 335
                direcao = 0
                comando_direcao = 0

                blinky_x = 25
                blinky_y = 25
                direcao_blinky = 0

                inky_x = 200
                inky_y = 195
                direcao_inky = 2

                pinky_x = 200
                pinky_y = 218
                direcao_pinky = 2

                clyde_x = 200
                clyde_y = 218
                direcao_clyde = 2

                fantasmas_mortos = [False, False, False, False]
               
                blinky_morto = False
                inky_morto = False
                clyde_morto = False
                pinky_morto = False

                pontuacao = 0
                vidas = 3
                level = copy.deepcopy(mapa)
                fim_de_jogo = False
                jogo_ganho = False

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

    if blinky.na_caixa and blinky.morto:
        blinky_morto = False
    if inky.na_caixa and inky.morto:
        inky_morto = False
    if pinky.na_caixa and pinky.morto:
        pinky_morto = False
    if clyde.na_caixa and clyde.morto:
        clyde_morto = False

    pygame.display.flip()


pygame.quit()