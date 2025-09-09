import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500))

jogador_img = pygame.image.load('img/jogador.png').convert()
jogador_img = pygame.transform.scale(jogador_img, (20, 20))

jogador_rect = jogador_img.get_rect()

jogador_rect.topleft = (30, 30)

running = True

clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))

    screen.blit(jogador_img, jogador_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        jogador_rect.x -= 10
    
    if keys[pygame.K_RIGHT]:
        jogador_rect.x += 10
    
    if keys[pygame.K_UP]:
        jogador_rect.y -= 10
    
    if keys[pygame.K_DOWN]:
        jogador_rect.y += 10

    pygame.display.flip()

pygame.quit()