import copy
import pygame
from funcoes import desenha_mapa, desenha_jogador, verifica_posicao, mover_jogador
from mapa import mapa

pygame.init()

largura = 420
altura = 475
tela = pygame.display.set_mode((largura, altura))
temporizador = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(mapa)
jogador_x = 200
jogador_y = 308
direcao = 0
contador = 0
flicker = False
pode_virar = [False, False, False, False]
comando_direcao = 0
velocidade = 2

rodando = True
while rodando:
    temporizador.tick(fps)
    tela.fill('black')
    desenha_mapa(altura, largura, tela, flicker)
    desenha_jogador(direcao, tela, contador, jogador_x, jogador_y)
    centro_x = jogador_x + 10
    centro_y = jogador_y + 10
    pode_virar = verifica_posicao(centro_x, centro_y, largura, altura, direcao, level)
    jogador_x, jogador_y = mover_jogador(direcao, jogador_x, jogador_y, pode_virar, velocidade)

    if contador < 19:
        contador += 1
        if contador > 3:
            flicker = False
    else:
        contador = 0
        flicker = True

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
            jogador_x = 293

    pygame.display.flip()


pygame.quit()