from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_left_right, size_up_down, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_left_right, size_up_down))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

time_fire = 0
many_of_bullet = 0

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

        Sprite_x = self.rect.x
        Sprite_y = self.rect.y

        Sprite_center_x = self.rect.centerx
        Sprite_top = self.rect.top

    def fire(self):
        global time_fire
        global many_of_bullet
        keys = key.get_pressed()
        if keys[K_DOWN]:
            bullet = Bullet("bullet.png", self.rect.centerx-12, self.rect.top, 25, 30, randint(-15,-5))
            bullets.add(bullet)
            many_of_bullet += 1

            time_fire = 0


lost = 0
score = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global many_of_bullet
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            many_of_bullet -= 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global score
        global many_of_bullet
        if self.rect.y <= 0:
            self.kill()
            many_of_bullet -= 1

       


            


win_width = 1000
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

player = Player("rocket.png", 20, 500, 80, 90, 5)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 90, 90, randint(1, 2))
    monsters.add(monster)

bullets = sprite.Group()


font.init()
font2 = font.SysFont("Arial", 25)

clock = time.Clock()
FPS = 90
game = True
finish = 1

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish == 1:
        if sprite.groupcollide(monsters, bullets, True, True):
            score += 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 90, 90, randint(2, 3))
            monsters.add(monster)

        window.blit(background,(0, 0))

        text_score = font2.render("Очки = " + str(score), True, (255, 255, 255))
        text_lose = font2.render("Пропущено = " + str(lost), True, (255, 255, 255))
        window.blit(text_score, (10, 10))
        window.blit(text_lose, (10, 32))

        player.update()
        monsters.update()
        bullets.update()

        player.reset()

        monsters.draw(window)
        bullets.draw(window)

        time_fire += 1
        if time_fire > 25 and many_of_bullet < 7:
            player.fire()

        if score >= lost+10:
            finish = 101
            time_fire = 0
            lost = 0
            score = 0

        elif lost >= score+5:
            finish = 404
            time_fire = 0
            lost = 0
            score = 0





    elif finish == 101:
        window.blit(background,(0, 0))
        text_score = font2.render("Вы победили!", True, (255, 255, 255))
        text_lose = font2.render("Вы победили!", True, (255, 255, 255))
        time_fire += 1
        window.blit(background,(0, 0))
        window.blit(text_score, (10, 10))
        window.blit(text_lose, (10, 32))
        time_fire += 1
        if time_fire > 200:
            finish = 1
        

    elif finish == 404:
        window.blit(background,(0, 0))
        text_score = font2.render("Вы проиграли", True, (255, 255, 255))
        text_lose = font2.render("Вы проиграли", True, (255, 255, 255))
        time_fire += 1
        window.blit(background,(0, 0))
        window.blit(text_score, (10, 10))
        window.blit(text_lose, (10, 32))
        time_fire += 1
        if time_fire > 200:
            finish = 1
        
        

    display.update()
    clock.tick(FPS)
