import pygame
import time
from mapa import mapa
from math import pi

def desenha_pontuacao(fonte, pontuacao, tela, powerup, vidas, fim_de_jogo, jogo_ganho):
    texto_pontuacao = fonte.render(f'Score: {pontuacao}', True, 'white')
    tela.blit(texto_pontuacao, (10,460))
    if powerup:
        pygame.draw.circle(tela, 'blue', (100, 465), 5)
        
    for i in range(vidas):
        tela.blit(pygame.transform.scale(imagens_jogador[0], (15, 15)), (350 + i * 20, 458))

    if fim_de_jogo:
        pygame.draw.rect(tela, 'white', [10, 100, 400, 150], 0, 10)
        pygame.draw.rect(tela, 'dark grey', [20, 110, 380, 130], 0, 10)
        texto_fim_de_jogo = fonte.render('Game Over! \nPressione espaço para recomeçar!', True, 'red')
        tela.blit(texto_fim_de_jogo, (40, 170))

    if jogo_ganho:
        pygame.draw.rect(tela, 'white', [10, 100, 400, 150], 0, 10)
        pygame.draw.rect(tela, 'dark grey', [20, 110, 380, 130], 0, 10)
        texto_fim_de_jogo = fonte.render('Parabéns, você venceu! \nPressione espaço para recomeçar!', True, 'green')
        tela.blit(texto_fim_de_jogo, (40, 170))

def verifica_colisao(altura, largura, jogador_x, level, centro_x, centro_y, pontuacao, power, contador_power, fantasmas_mortos):
    num1 = altura // 32
    num2 = largura // 30
    som_comer = False
    som_powerup = False
    if 0 < jogador_x < 400:
        linha = centro_y // num1
        coluna = centro_x // num2

        if level[linha][coluna] == 1:
            level[linha][coluna] = 0
            pontuacao += 10
            som_comer = True

        if level[linha][coluna] == 2:
            level[linha][coluna] = 0
            pontuacao += 50
            power = True
            contador_power = 0
            fantasmas_mortos = [False, False, False, False]
            som_powerup = True


    return pontuacao, power, contador_power, fantasmas_mortos, som_comer, som_powerup

def desenha_mapa(altura, largura, tela, flicker, mapa_atual):
    num1 = altura // 32
    num2 = largura // 30
    for i in range(len(mapa_atual)):
        for j in range(len(mapa_atual[i])):
            if mapa_atual[i][j] == 1:
                pygame.draw.circle(tela, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 2)
            if mapa_atual[i][j] == 2 and not flicker:
                pygame.draw.circle(tela, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 5)
            if mapa_atual[i][j] == 3:
                pygame.draw.line(tela, 'blue', (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if mapa_atual[i][j] == 4:
                pygame.draw.line(tela, 'blue', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if mapa_atual[i][j] == 5:
                pygame.draw.arc(tela, 'blue', [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1], 0, pi / 2, 3)
            if mapa_atual[i][j] == 6:
                pygame.draw.arc(tela, 'blue', [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], pi / 2, pi, 3)
            if mapa_atual[i][j] == 7:
                pygame.draw.arc(tela, 'blue', [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], pi, 3 * pi / 2, 3)
            if mapa_atual[i][j] == 8:
                pygame.draw.arc(tela, 'blue', [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * pi / 2, 2 * pi, 3)
            if mapa_atual[i][j] == 9:
                pygame.draw.line(tela, 'white', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

imagens_jogador = []
for i in range(1, 5):
    imagens_jogador.append(pygame.transform.scale(pygame.image.load(f'assets/img/jogador/{i}.png'), (20, 20)))

def desenha_jogador(direcao, tela, contador, jogador_x, jogador_y):
    if direcao == 0:
        tela.blit(imagens_jogador[contador // 5], (jogador_x, jogador_y))
    if direcao == 1:
        tela.blit(pygame.transform.flip(imagens_jogador[contador // 5], True, False), (jogador_x, jogador_y))
    if direcao == 2:
        tela.blit(pygame.transform.rotate(imagens_jogador[contador // 5], 90), (jogador_x, jogador_y))
    if direcao == 3:
        tela.blit(pygame.transform.rotate(imagens_jogador[contador // 5], 270), (jogador_x, jogador_y))

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

def busca_alvos(blinky, inky, pinky, clyde, jogador_x, jogador_y, fantasmas_mortos, powerup):
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

