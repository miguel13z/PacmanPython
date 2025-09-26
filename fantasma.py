import pygame
from config import *

class Fantasma:
    def __init__(self, coord_x, coord_y, alvo, velocidade, img, direcao, morto, caixa, id, powerup_status, fantasmas_mortos_list):
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
        
        self.powerup_ativo = powerup_status
        self.lista_fantasmas_mortos = fantasmas_mortos_list

        self.vira, self.na_caixa = self.verifica_colisao()
        self.rect = self.desenha()

    def desenha(self):
        if (not self.powerup_ativo and not self.morto) or (self.lista_fantasmas_mortos[self.id] and self.powerup_ativo and not self.morto):
            tela.blit(self.img, (self.coord_x, self.coord_y))
        elif self.powerup_ativo and not self.morto and not self.lista_fantasmas_mortos[self.id]:
            tela.blit(img_spooked, (self.coord_x, self.coord_y))
        else:
            tela.blit(img_dead, (self.coord_x, self.coord_y))

        fantasma_rect = pygame.rect.Rect((self.coord_x - 10, self.coord_y - 10), (18, 18))
        return fantasma_rect
    
    def verifica_colisao(self):
        num1 = ALTURA // 32
        num2 = LARGURA // 30
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

        if self.coord_x > LARGURA:
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
        if self.coord_x > LARGURA:
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
        if self.coord_x > LARGURA:
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
        if self.coord_x > LARGURA:
            self.coord_x = -23
        elif self.coord_x < -25:
            self.coord_x = 410
        return self.coord_x, self.coord_y, self.direcao