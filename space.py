import pygame, random

# set CONSTANTS
WIDTH = 360 # width of our game window
HEIGHT = 480 # height of our game window

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set Classes
class MyGame():
    def __init__(self):
        pygame.init()
        #pygame.mixer.init()  # for sound
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.star_field = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()

    def main_loop(self):
        self.add_star_field(400)
        self.add_aliens(6, 4)
        self.add_player()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over()
            self.update()

    def update(self):
        self.aliens_drop = False
        self.shoot = False
        self.star_field.update()
        self.aliens.update()
        self.players.update()
        if self.shoot:
            self.shoot_laser()
        self.lasers.update()
        if self.aliens_drop:
            for alien in self.aliens:
                alien.row_end()
        self.screen.fill(BLACK)
        self.star_field.draw(self.screen)
        self.aliens.draw(self.screen)
        self.players.draw(self.screen)
        self.lasers.draw(self.screen)
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
        star.add(self.star_field)

    def add_aliens(self, aliens, rows):
        for row_index in range(rows):
            for column_index in range(aliens):
                alien = Alien(20 + (column_index * 40), 20 + (row_index *40))
                alien.add(self.aliens)

    def add_player(self):
        player = Player()
        player.add(self.players)

    def shoot_laser(self):
        x = self.players()
        laser = laser(x)
        laser.add(self.lasers)

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

class Alien(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 25, GREEN)
        self.dx = 1

    def update(self):
        self.rect.x += self.dx
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            my_game.aliens_drop = True

    def row_end(self):
        self.dx *= -1
        self.rect.y += 40

class Player(GameObject):
    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT - 50, 25, BLUE)

    def update(self):
        keys = pygame.key.get_pressed()  #check pressed keys
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 10:
            self.rect.x += 2
        elif keys[pygame.K_LEFT] and self.rect.left > 10:
            self.rect.x -= 2
        elif keys[pygame.K_SPACE]:
            my_game.shoot = True

if __name__ == "__main__":
    my_game = MyGame()
    my_game.main_loop()