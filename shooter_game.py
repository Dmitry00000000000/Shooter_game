#Создай собственный Шутер!
from time import *
from time import time as timer
from pygame import *
from random import randint
window = display.set_mode((700,500))
display.set_caption('Шутер')
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
bullet_sound = mixer.Sound('fire.ogg')
mixer.music.set_volume(0.2)
bullet_sound.set_volume(0.2)
background = transform.scale(image.load('galaxy.jpg'), (700,500))
bcount = 0
gcount = 0
life = 5
num_fire = 0
rel_time = False
game = True
finish = False
clock = time.Clock()
FPS = 60
class GameSprite(sprite.Sprite):
    def __init__(self, qimage, x, y, qspeed, qx, qy):
        super().__init__()
        self.image = transform.scale(image.load(qimage), (qx,qy))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = qspeed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 15,20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        direction = 'down'
        global bcount
        if self.rect.y >= -70:
            self.rect.y += self.speed
        if self.rect.y >= 550:
            self.rect.y = -70            
            self.rect.x = randint(5,630)
            bcount += 1
        
class Rock(GameSprite):
    def update(self):
        direction = 'down'
        if self.rect.y >= -70:
            self.rect.y += self.speed
        if self.rect.y >= 550:
            self.rect.y = -70            
            self.rect.x = randint(5,630)

class Bullet(GameSprite):
    def update(self):
        direction = 'up'
        self.rect.y -= self.speed
        if self.rect.y <= -70:
            self.kill()

font.init()
font2 = font.SysFont('Arial',80)
font1 = font.SysFont('Arial', 36)
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(3):
    asteroid = Rock('asteroid.png', randint(200,500),-70,randint(1,3),80,80)
    asteroids.add(asteroid)
for i in range(5):
    monster = Enemy('ufo.png',randint(200,500),-70,randint(1,5),80,50)
    monsters.add(monster)
player = Player('rocket.png',350,430,5,65,65)

win = font2.render('YOU WIN',1,(255,255,0)) 
lose = font2.render('YOU LOSE', 1, (255,0,0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()    
                    bullet_sound.play()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:   
                    rel_time = True
                    start = timer()   
    if finish != True:
        window.blit(background, (0,0))
        sprite_list = sprite.groupcollide(monsters,bullets, True, True)
        for i in sprite_list:
            gcount += 1
            monster = Enemy('ufo.png',randint(200,500),-70,randint(1,3),80,50)
            monsters.add(monster)
        if sprite.spritecollide(player,asteroids,True) or sprite.spritecollide(player,monsters,True):
            life -= 1
        text_lose = font1.render('Пропущенно: ' + str(bcount), 1, (255,255,255))
        if rel_time == True:
            end = timer() - start
            if end >= 3:
                num_fire = 0
                rel_time = False

            else:
                reload_ = font1.render('reloading...', 1, (255,0,0))
                window.blit(reload_, (450,450))
        
        if gcount == 10:
            finish = True
            window.blit(win, (200,250))
        if bcount >= 3 or life <= 0:
            finish = True
            window.blit(lose, (200,250))
        text_life = font1.render('Жизнь(-и): ' + str(life),1,(0,255,0))
        text_win = font1.render('Счёт: ' + str(gcount), 1, (255,255,255))
        window.blit(text_lose, (10,60))
        window.blit(text_win, (10,20))
        window.blit(text_life, (500,20))
        player.update()
        bullets.update()
        monsters.draw(window)
        asteroids.draw(window)
        asteroids.update()
        player.reset()
        monsters.update()
        bullets.draw(window)

    display.update()
    clock.tick(FPS)

