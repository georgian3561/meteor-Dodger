import pygame, sys, random
from pygame import mixer

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, path,x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.shield_surface = pygame.image.load('Assets/shield.png')
        self.health = 5

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen_constair()
        self.display_health()

    def screen_constair(self):
        if self.rect.right >= 1280:
             self.rect.right = 1280

        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= 720:
            self.rect.bottom = 720

    def display_health(self):
        for index,shield in enumerate(range(self.health)):
            screen.blit(self.shield_surface, (10+index*40, 10))

    def get_damage(self, damage_amount):
        self.health -= damage_amount

class Meteors(pygame.sprite.Sprite):
    def __init__(self, path, x_pos,y_pos, x_speed, y_speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

        if self.rect.centery >= 800:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, path, pos, speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed

    def update(self):
        self.rect.centery -= self.speed

        if self.rect.centery <= -100:
            self.kill()

def main_game():
    global laser_active
    laser_grp.draw(screen)
    spaceship_group.draw(screen)
    meteors_grp.draw(screen)

    laser_grp.update()
    meteors_grp.update()
    spaceship_group.update()

    # Collision
    if pygame.sprite.spritecollide(spaceship_group.sprite, meteors_grp, True):
        spaceship_group.sprite.get_damage(1)

    for laser in laser_grp:
        pygame.sprite.spritecollide(laser, meteors_grp, True)

    if pygame.time.get_ticks() - laser_timer >= 200:
        laser_active = True

    return 1

def end_game():
    text_surface = game_font.render('Game Over', True, (255, 255, 255))
    text_rect = text_surface.get_rect(center = (640, 340))
    screen.blit(text_surface, text_rect)


    score_surface = game_font.render(f'Score: {score}', True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (640, 380))
    screen.blit(score_surface, score_rect)


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
game_font = pygame.font.Font('Assets/LazenbyCompSmooth.ttf', 40)
score = 0
laser_timer = 0
laser_active = False

mixer.music.load('DeathMatch (Boss Theme).ogg')
mixer.music.play(-1)


spaceship = SpaceShip('Assets/spaceship.png', 640, 650)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

meteors_grp = pygame.sprite.Group()
METEOR_EVENT =  pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT, 150)

laser_grp = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == METEOR_EVENT:
            meteor_path = random.choice(('Assets/Meteor1.png', 'Assets/Meteor2.png', 'Assets/Meteor3.png'))
            random_x_pos = random.randrange(0, 1280)
            random_y_pos = random.randrange(-500, -50)
            random_x_speed = random.randrange(-1, 1)
            random_y_speed = random.randrange(3, 9)
            meteor = Meteors(meteor_path, random_x_pos,random_y_pos, random_x_speed, random_y_speed)
            meteors_grp.add(meteor)

        if event.type == pygame.MOUSEBUTTONDOWN and laser_active:
            new_laser = Laser('Assets/Laser.png', event.pos, 15)
            laser_grp.add(new_laser)
            laser_active = False
            laser_timer = pygame.time.get_ticks()


        if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.health <= 0:
            spaceship_group.sprite.health = 5
            meteors_grp.empty()
            score = 0

    screen.fill((42, 45, 51))
    if spaceship_group.sprite.health > 0:
        score += main_game()

    else:
        end_game()

    pygame.display.update()
    clock.tick(120)
