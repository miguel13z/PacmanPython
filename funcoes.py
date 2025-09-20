import pygame
from mapa import mapa
from math import pi

def verifica_colisao(altura, largura, jogador_x, level, centro_x, centro_y, pontuacao):
    num1 = altura // 32
    num2 = largura // 30
    if 0 < jogador_x < 400:
        linha = centro_y // num1
        coluna = centro_x // num2

        if level[linha][coluna] == 1:
            level[linha][coluna] = 0
            mapa[linha][coluna] = 0
            pontuacao += 10

        if level[linha][coluna] == 2:
            level[linha][coluna] = 0
            mapa[linha][coluna] = 0
            pontuacao += 50

    return pontuacao

def desenha_mapa(altura, largura, tela, flicker):
    num1 = altura // 32
    num2 = largura // 30
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == 1:
                pygame.draw.circle(tela, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 2)
            if mapa[i][j] == 2 and not flicker:
                pygame.draw.circle(tela, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 5)
            if mapa[i][j] == 3:
                pygame.draw.line(tela, 'blue', (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if mapa[i][j] == 4:
                pygame.draw.line(tela, 'blue', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if mapa[i][j] == 5:
                pygame.draw.arc(tela, 'blue', [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1], 0, pi / 2, 3)
            if mapa[i][j] == 6:
                pygame.draw.arc(tela, 'blue', [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], pi / 2, pi, 3)
            if mapa[i][j] == 7:
                pygame.draw.arc(tela, 'blue', [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], pi, 3 * pi / 2, 3)
            if mapa[i][j] == 8:
                pygame.draw.arc(tela, 'blue', [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * pi / 2, 2 * pi, 3)
            if mapa[i][j] == 9:
                pygame.draw.line(tela, 'white', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

imagens_jogador = []
for i in range(1, 5):
    imagens_jogador.append(pygame.transform.scale(pygame.image.load(f'img/jogador/{i}.png'), (20, 20)))

def desenha_jogador(direcao, tela, contador, jogador_x, jogador_y):
    if direcao == 0:
        tela.blit(imagens_jogador[contador // 5], (jogador_x, jogador_y))
    if direcao == 1:
        tela.blit(pygame.transform.flip(imagens_jogador[contador // 5], True, False), (jogador_x, jogador_y))
    if direcao == 2:
        tela.blit(pygame.transform.rotate(imagens_jogador[contador // 5], 90), (jogador_x, jogador_y))
    if direcao == 3:
        tela.blit(pygame.transform.rotate(imagens_jogador[contador // 5], 270), (jogador_x, jogador_y))

# No seu arquivo de funções (funcoes.py), substitua a função inteira por esta:

def verifica_posicao(centro_x, centro_y, largura, altura, direcao, level):
    pode_virar = [False, False, False, False]
    num1 = altura // 32
    num2 = largura // 30
    num3 = num2 // 2

    if centro_x // num2 < 29:
        if direcao == 0:
            if level[centro_y // num1][(centro_x - num3) // num2] < 3:
                pode_virar[1] = True
        if direcao == 1:
            if level[centro_y // num1][(centro_x + num3) // num2] < 3:
                pode_virar[0] = True
        if direcao == 2:
            if level[(centro_y + num3) // num1][centro_x // num2] < 3:
                pode_virar[3] = True
        if direcao == 3:
            if level[(centro_y - num3) // num1][centro_x // num2] < 3:
                pode_virar[2] = True

        centro_tile_x_min = (num2 // 2) - 2
        centro_tile_x_max = (num2 // 2) + 2
        centro_tile_y_min = (num1 // 2) - 2
        centro_tile_y_max = (num1 // 2) + 2
        
        if direcao == 2 or direcao == 3: 
            if centro_tile_x_min <= centro_x % num2 <= centro_tile_x_max:
                if level[(centro_y + num3) // num1][centro_x // num2] < 3:
                    pode_virar[3] = True
                if level[(centro_y - num3) // num1][centro_x // num2] < 3:
                    pode_virar[2] = True
            if centro_tile_y_min <= centro_y % num1 <= centro_tile_y_max:
                if level[centro_y // num1][(centro_x - num2) // num2] < 3:
                    pode_virar[1] = True
                if level[centro_y // num1][(centro_x + num2) // num2] < 3:
                    pode_virar[0] = True

        if direcao == 0 or direcao == 1: 
            if centro_tile_x_min <= centro_x % num2 <= centro_tile_x_max:
                if level[(centro_y + num1) // num1][centro_x // num2] < 3:
                    pode_virar[3] = True
                if level[(centro_y - num1) // num1][centro_x // num2] < 3:
                    pode_virar[2] = True
            if centro_tile_y_min <= centro_y % num1 <= centro_tile_y_max:
                if level[centro_y // num1][(centro_x - num3) // num2] < 3:
                    pode_virar[1] = True
                if level[centro_y // num1][(centro_x + num3) // num2] < 3:
                    pode_virar[0] = True
    else:
        pode_virar[0] = True
        pode_virar[1] = True

    return pode_virar

def mover_jogador(direcao, jogador_x, jogador_y, pode_virar, velocidade):
    if direcao == 0 and pode_virar[0]:
        jogador_x += velocidade
    elif direcao == 1 and pode_virar[1]:
        jogador_x -= velocidade
    if direcao == 2 and pode_virar[2]:
        jogador_y -= velocidade
    elif direcao == 3 and pode_virar[3]:
        jogador_y += velocidade

    return jogador_x, jogador_y