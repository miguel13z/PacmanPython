import pygame
from gamemap import mapa
from math import pi

def desenha_mapa():
    num1 = (altura - 50) // 32
    num2 = largura // 30
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 2)
            if mapa[i][j] == 2:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 5)
            if mapa[i][j] == 3:
                pygame.draw.line(screen, cor_mapa, (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if mapa[i][j] == 4:
                pygame.draw.line(screen, cor_mapa, (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if mapa[i][j] == 5:
                pygame.draw.arc(screen, cor_mapa, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1], 0, pi / 2, 3)
            if mapa[i][j] == 6:
                pygame.draw.arc(screen, cor_mapa, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], pi / 2, pi, 3)
            if mapa[i][j] == 7:
                pygame.draw.arc(screen, cor_mapa, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], pi, 3 * pi / 2, 3)
            if mapa[i][j] == 8:
                pygame.draw.arc(screen, cor_mapa, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * pi / 2, 2 * pi, 3)
            if mapa[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


largura = 500
altura = 500
largura_pacman = 20
altura_pacman = 20
cor_mapa = 'blue'

pygame.init()

screen = pygame.display.set_mode((largura, altura))


pacman = pygame.image.load('img/pacman.png').convert()
pacman = pygame.transform.scale(pacman, (largura_pacman, altura_pacman))

pacman_left = pygame.transform.flip(pacman, True, False)
pacman_up = pygame.transform.rotate(pacman, 90)
pacman_down = pygame.transform.rotate(pacman, -90)

pacman_move = pacman
pacman_rect = pacman_move.get_rect()
pacman_rect.topleft = (30, 30)

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))

    screen.blit(pacman_move, pacman_rect)

    desenha_mapa()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_LEFT]:
        pacman_move = pacman_left
        pacman_rect.x -= 10 
    elif keys[pygame.K_RIGHT]:
        pacman_move = pacman
        pacman_rect.x += 10
    elif keys[pygame.K_UP]:
        pacman_move = pacman_up
        pacman_rect.y -= 10
    elif keys[pygame.K_DOWN]:
        pacman_move = pacman_down
        pacman_rect.y += 10

    pygame.display.flip()
    clock.tick(60)

pygame.quit()