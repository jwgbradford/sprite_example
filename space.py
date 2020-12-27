import pygame, random

# set CONSTANTS
WIDTH = 360
HEIGHT = 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# set Classes
class MyGame():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.main_loop()

    def main_loop(self):
        self.add_star_field(400)
        self.add_player()
        self.playing = True
        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            self.update()

    def update(self):
        self.screen.fill(BLACK)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.display.update()
        self.clock.tick(60)

    def add_star_field(self, number_of_stars):
        for _ in range(number_of_stars):
            self.add_star()

    def add_star(self):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        star = Star(x, y)
        star.add(self.all_sprites)

    def add_player(self):
        player = Player()
        player.add(self.all_sprites)

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, size, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.image.fill(colour)

class Star(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 1, WHITE)

    def update(self):
        self.rect.y += 1
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.left = random.randint(0, WIDTH)

class Player(GameObject):
    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT - 50, 25, BLUE)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 10:
            self.rect.x += 2
        elif keys[pygame.K_LEFT] and self.rect.left > 10:
            self.rect.x -= 2

if __name__ == "__main__":
    my_game = MyGame()