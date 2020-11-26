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
YELLOW = (255, 255, 0)

# set Classes
class MyGame():
    def __init__(self):
        pygame.init()
        #pygame.mixer.init()  # for sound
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.score = 0
        self.font = pygame.font.Font(None, 30)
        self.add_star_field(400)
        self.aliens_drop = False
        self.add_aliens(6, 4)
        self.add_player()
        self.main_loop()

    def main_loop(self):
        self.playing = True
        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            self.update()
        self.game_over()

    def update(self):
        self.screen.fill(BLACK)
        self.all_sprites.update()
        self.hit_check()
        if self.aliens_drop:
            self.aliens.row_end()
        self.all_sprites.draw(self.screen)
        self.display_score()
        pygame.display.update()
        self.clock.tick(60)

    def game_over(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            txt = self.font.render('Press x to exit', True, WHITE)
            self.screen.blit(txt, (WIDTH / 2, 100))
            txt = self.font.render('Press space to', True, WHITE)
            self.screen.blit(txt, (WIDTH / 2, 120))
            txt = self.font.render('play again', True, WHITE)
            self.screen.blit(txt, (WIDTH / 2, 160))

    def add_star_field(self, number_of_stars):
        for _ in range(number_of_stars):
            self.add_star()

    def add_star(self):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        star = Star(x, y)
        star.add(self.all_sprites)

    def add_aliens(self, aliens, rows):
        for row_index in range(rows):
            for column_index in range(aliens):
                alien = Alien(20 + (column_index * 40), 20 + (row_index *40))
                alien.add(self.aliens, self.all_sprites)

    def add_player(self):
        player = Player(self.screen )
        player.add(self.players, self.all_sprites)

    def hit_check(self):
        self.check_aliens()
        self.check_player()

    def check_aliens(self):
        for player in self.players:
            laser_beams = player.lasers
            hit_aliens = pygame.sprite.groupcollide(self.aliens, laser_beams, True, True)
            if len(hit_aliens) > 0:
                self.score += 10

    def check_player(self):
        player_hit = pygame.sprite.groupcollide(self.players, self.aliens, False, False)
        if len(player_hit) > 0:
            self.aliens.empty()
            self.players.empty()
            self.playing = False

    def display_score(self):
        score_txt = str(self.score)
        txt = self.font.render(score_txt, True, WHITE)
        self.screen.blit(txt, (WIDTH / 2, 20))

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
            self.row_end()# = True

    def row_end(self):
        self.dx *= -1
        self.rect.y += 40

class Player(GameObject):
    def __init__(self, screen):
        super().__init__(WIDTH / 2, HEIGHT - 50, 25, BLUE)
        self.screen = screen
        self.lasers = pygame.sprite.Group()
        self.shoot_timer = 20

    def update(self):
        keys = pygame.key.get_pressed()  #check pressed keys
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 10:
            self.rect.x += 2
        elif keys[pygame.K_LEFT] and self.rect.left > 10:
            self.rect.x -= 2
        if keys[pygame.K_SPACE] and self.shoot_timer == 0:
            self.shoot_laser()
            self.shoot_timer = 20
        self.lasers.update()
        self.lasers.draw(self.screen)
        if self.shoot_timer > 0:
            self.shoot_timer -= 1

    def shoot_laser(self):
        laser = Laser(self.rect.centerx, self.rect.top)
        laser.add(self.lasers)

class Laser(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 1, YELLOW)
        self.image = pygame.Surface((2, 6))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.image.fill(YELLOW)

    def update(self):
        self.rect.y -= 2
        if self.rect.bottom <= 0:
            self.kill()

if __name__ == "__main__":
    my_game = MyGame()