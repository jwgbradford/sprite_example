import pygame

WIDTH = 360 # width of our game window
HEIGHT = 480 # height of our game window
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

class MyGame():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.alien_drop = False
        for row_index in range(4):
            for column_index in range(6):
                alien = Alien(20 + (column_index * 40), 20 + (row_index *40))
                alien.add(self.all_sprites)
        while True:
            self.screen.fill(BLACK)
            self.all_sprites.update()
            if self.alien_drop:
                self.aliens.row_end()
            self.all_sprites.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.image.fill(GREEN)
        self.dx = 1

    def update(self):
        self.rect.x += self.dx
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            my_game.alien_drop = True

    def row_end(self):
        self.dx *= -1
        self.rect.y += 40

if __name__ == "__main__":
    my_game = MyGame()