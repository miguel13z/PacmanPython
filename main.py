import copy
import pygame
from funcoes import *
from config import *
from fantasma import Fantasma

pygame.init()
pygame.mixer.init()

som_bolinha = pygame.mixer.Sound('assets/sound/pacman_chomp.wav')
som_morte = pygame.mixer.Sound('assets/sound/pacman_death.wav')
som_comeco = pygame.mixer.Sound('assets/sound/pacman_beginning.wav')
som_comer_fantasma = pygame.mixer.Sound('assets/sound/pacman_eatghost.wav')
som_powerup = pygame.mixer.Sound('assets/sound/pacman_powerup.wav')

som_comeco.play()
rodando = True
while rodando:
    temporizador.tick(fps)
    tela.fill('black')
    desenha_mapa(ALTURA, LARGURA, tela, flicker, level)
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
    
    blinky = Fantasma(blinky_x, blinky_y, alvos[0], velocidade_fantasma[0], img_blinky, direcao_blinky, blinky_morto, blinky_caixa, 0, powerup, fantasmas_mortos)
    inky = Fantasma(inky_x, inky_y, alvos[1], velocidade_fantasma[1], img_inky, direcao_inky, inky_morto, inky_caixa, 1, powerup, fantasmas_mortos)
    pinky = Fantasma(pinky_x, pinky_y, alvos[2], velocidade_fantasma[2], img_pinky, direcao_pinky, pinky_morto, pinky_caixa, 0, powerup, fantasmas_mortos)
    clyde = Fantasma(clyde_x, clyde_y, alvos[0], velocidade_fantasma[3], img_clyde, direcao_clyde, clyde_morto, clyde_caixa, 1, powerup, fantasmas_mortos)

    desenha_pontuacao(fonte, pontuacao, tela, powerup, vidas, fim_de_jogo, jogo_ganho)
    alvos = busca_alvos(jogador_x, jogador_y, powerup, blinky, inky, pinky, clyde, fantasmas_mortos)
    centro_x = jogador_x + 10
    centro_y = jogador_y + 10
    pode_virar = verifica_posicao(centro_x, centro_y, LARGURA, ALTURA, direcao, level)

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
    pontuacao, powerup, contador_power, fantasmas_mortos, tocar_som_comer, tocar_som_powerup = verifica_colisao(ALTURA, LARGURA, jogador_x, level, centro_x, centro_y, pontuacao, powerup, contador_power, fantasmas_mortos)

    if tocar_som_comer:
        if not pygame.mixer.get_busy():
            som_bolinha.play()
    if tocar_som_powerup:
        som_powerup.play()

    if contador < 19:
        contador += 1
        if contador > 3:
            flicker = False
    else:
        contador = 0
        flicker = True

    if powerup and contador_power < 300:
        contador_power += 1
    elif powerup and contador_power >= 300:
        contador_power = 0
        powerup = False
        fantasmas_mortos = [False, False, False, False]

    if contador_inicio < 240 and not fim_de_jogo and not jogo_ganho:
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
                som_morte.play()
                vidas -= 1
                powerup = False
                contador_power = 0
                contador_inicio = 0
                jogador_x = 203
                jogador_y = 335
                direcao = 0
                comando_direcao = 0

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
        som_comer_fantasma.play()
    if powerup and circulo_jogador.colliderect(inky.rect) and not inky.morto and not fantasmas_mortos[1]:
        inky_morto = True
        fantasmas_mortos[1] = True
        pontuacao += 2 ** fantasmas_mortos.count(True)* 100
        som_comer_fantasma.play()
    if powerup and circulo_jogador.colliderect(pinky.rect) and not pinky.morto and not fantasmas_mortos[2]:
        pinky_morto = True
        fantasmas_mortos[2] = True
        pontuacao += 2 ** fantasmas_mortos.count(True) * 100
        som_comer_fantasma.play()
    if powerup and circulo_jogador.colliderect(clyde.rect) and not clyde.morto and not fantasmas_mortos[3]:
        clyde_morto = True
        fantasmas_mortos[3] = True
        pontuacao += 2 ** fantasmas_mortos.count(True) * 100
        som_comer_fantasma.play()

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
                som_comeco.play()
                vidas -= 1
                powerup = False
                contador_power = 0
                contador_inicio = 0
                jogador_x = 203
                jogador_y = 335
                direcao = 0
                comando_direcao = 0

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

    if jogador_x > LARGURA:
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