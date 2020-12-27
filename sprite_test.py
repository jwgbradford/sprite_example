import pygame, random, time

WIDTH = 720
HEIGHT = 960
TESTSIZE = 8000

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# using simple surfaces in pygame
def make_piece():
    image = pygame.Surface((1, 1))
    image.fill((255, 255, 255))
    return image

    def update(self):
        self.rect.y += 1
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.left = random.randint(0, WIDTH)

#using classes and sprite.Sprite objects
class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, size, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.image.fill(colour)

class Star(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 1, (255, 255, 255))

    def update(self):
        ## try using these
        #if random.randint(0, 100) > 99:
            #self.rect.y += 1
        #self.add(updated)
            #if self.rect.top > HEIGHT:
            #    self.rect.bottom = 0

        ## down to here, and comment line below to see impact of random (about 0.2 sec)
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

## use this block to test sprite.Group
all_sprites = pygame.sprite.Group()
for _ in range(TESTSIZE):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    star = Star(x, y)
    star.add(all_sprites)
updated = pygame.sprite.Group()

## use this block to test simple list of images
#images = []
#for i in range(TESTSIZE):
#    images.append(make_piece())

font = pygame.font.Font(None, 30)
tic = time.perf_counter()

while True:
    screen.fill((0, 0, 0))
    ## if testing simple list, use this
#    for element in images:
#        screen.blit(element, (random.randint(0, WIDTH), random.randint(0, HEIGHT)))

    ## if testing sprite.Group use this
    all_sprites.update()
    all_sprites.draw(screen)

    toc = time.perf_counter() # simple performance timer
    time_txt = str(toc - tic)
    txt = font.render(time_txt, True, (255, 255, 255))
    screen.blit(txt, (WIDTH / 2, 100))

    pygame.display.update()
    #updated.empty()
    # we put the second timer after the screen update
    # as it could be a bottleneck (it isn't)
    tic = time.perf_counter()