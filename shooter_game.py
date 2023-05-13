from pygame import *
from random import randint
from time import time as timer
 
#music
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
 
#fonts 
font.init()
font2 = font.Font(None, 36)
win = font2.render('You WIN! :D :D', True, (255, 255, 255))
lose = font2.render('You Lose T_T', True, (100, 0, 0))
#images
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"
 
score = 0
lost = 0
max_lost = 3
 
#CLASSES
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        #Properties
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        #Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        #draw the character on the window
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
 
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
             self.rect.x += self.speed
 
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
 
class Enemy(GameSprite):
    def update(self):
        global lost
        #automatic movement
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
 
class Bullet(GameSprite):
    #movement
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

#window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
#sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
 
for i in range(1,3):
    myasteroid = Enemy(img_ast, randint(30, win_width - 80), -40, 80, 50, randint(1,7))
    asteroids.add(myasteroid)
for i in range(1,6):
    myufo = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(myufo)
rel_time = False
num_fire = 0 

finish = False
run = True
while run == True:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
 
    if not finish:
        window.blit(background, (0,0))
 
        #Score text
        text_score = font2.render("Score: " + str(score), 1, (255,255,255))
        window.blit(text_score,(10,20))
        #Missed Text
        text_lose = font2.render("Missed: " + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))
 
        ship.update()
        ship.reset()
 
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer() 

            if now_time - last_time < 6:
                rel_text = font2.render('Wait, reloading...', 1, (150,0,0))
                window.blit(rel_text,(290,460))
            else:
                num_fire = 0 
                rel_time = False

        #collision bullets, ufo
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            myufo = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(myufo)
        #Win condition
        if score >= 10:
            finish = True
            window.blit(win, (200,200))

        #Lose condition
        if (sprite.spritecollide(ship, monsters, False) or lost >= max_lost or 
        sprite.spritecollide(ship, asteroids, False)):

            finish = True
            window.blit(lose, (200,200))

        display.update()
 
    time.delay(50)#0.05sec