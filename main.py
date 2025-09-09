import pygame

def main():
    pygame.init()

    screen = pygame.display.set_mode((500, 500))

    pacman = pygame.image.load('img/pacman.png').convert()
    pacman = pygame.transform.scale(pacman, (20, 20))

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

main()