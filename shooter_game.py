from pygame import *
from random import randint

width = 700
height = 500

root = display.set_mode((width, height))

bg = transform.scale(image.load('galaxy.jpg'),(width, height))

clock = time.Clock()

score = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, x, y, w, h, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(sprite_image), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def redraw(self):
        root.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        elif keys[K_RIGHT] and self.rect.x < width - 60:
            self.rect.x += self.speed

    def fire(self):
        bullets.add(Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > height:
            self.rect.y = -40
            self.rect.x = randint(80,width - 80)
            lost += 1
            print('lost')

class Bullet(GameSprite):
    def update(self):
        self.rect.y-= self.speed
        if self.rect.y < 0:
            self.kill()

mixer.init()

mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

font.init()
my_font = font.Font(None, 36)
gameover_font = font.Font(None, 72)

bullets = sprite.Group()


ship = Player('rocket.png', 300, 330, 80, 100, 10)

camets = sprite.Group()
for i in range(5):
    camets.add(Enemy('ufo.png', randint(80,width - 80), randint(-200, -40), 80, 50, randint(1, 5)))

game_on = True
game_off = False

BLACK = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)

while game_on:
    for e in event.get():
        if e.type == QUIT:
            game_on = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()

    if not game_off:
        root.blit(bg, (0, 0))

        text_score = my_font.render(f'Счёт:{score}', True, BLACK)
        text_lost = my_font.render(f'Пропушено:{lost}', True, BLACK)

        root.blit(text_score, (80, 40))
        root.blit(text_lost, (80, 70))

        ship.update()
        ship.redraw()

        camets.update()
        camets.draw(root)

        bullets.update()
        bullets.draw(root)

        collides = sprite.groupcollide(camets, bullets, True, True)
        for i in range(len(collides)):
            score += 1
            camets.add(Enemy('ufo.png', randint(80,width - 80), randint(-200, -40), 80, 50, randint(1, 5)))

        if sprite.spritecollide(ship, camets, False) or lost >= 5:
            game_off = True
            text_gameover = gameover_font.render('GAME OVER',True, RED)
            root.blit(text_gameover, (220, 230))

        if score >= 5:
            game_off = True
            text_win = gameover_font.render('YOU WIN',True, GREEN)
            root.blit(text_win, (220, 230))

        display.update()

    clock.tick(60)