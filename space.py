import pygame, random

# set CONSTANTS
WIDTH = 360 # width of our game window
HEIGHT = 480 # height of our game window

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# set Classes
class MyGame():
    def __init__(self):
        pygame.init()
        #pygame.mixer.init()  # for sound
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()

    def main_loop(self):
        self.add_star_field(400)
        while True:
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.game_over()
            self.update()

    def update(self):
        self.all_sprites.update()
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.update()
        self.clock.tick(60)

    def game_over(self):
        pygame.quit()
        raise SystemExit

    def add_star_field(self, number_of_stars):
        for _ in range(number_of_stars):
            self.add_star()

    def add_star(self):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        star = Star(x, y)
        star.add(self.all_sprites)

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y += 1
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.left = random.randint(0, WIDTH)

if __name__ == "__main__":
    my_game = MyGame()
    my_game.main_loop()