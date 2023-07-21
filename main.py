#  Mo-taz bataineh 148710
import pygame
from pygame.locals import *
import random
from pygame import mixer
import buttin_m
from bird import Bird
from pipe import Pipe
from button import Button
from coins import Coins

mixer.init()
pygame.init()

# control the frame rate
clock = pygame.time.Clock()
fps = 60

# load music and sound effect
pygame.mixer.music.load('assets/bg_soo.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 40.5)
jump_fx = pygame.mixer.Sound('assets/jump_fx.mp3')
jump_fx.set_volume(0.4)
death_fx = pygame.mixer.Sound('assets/death.mp3')
death_fx.set_volume(0.9)
coin_fx = pygame.mixer.Sound('assets/coin.mp3')
coin_fx.set_volume(0.9)

screen_width = 640
screen_height = 700
#  screen & caption & icon
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('WING JUMP')
pygame_icon = pygame.image.load('img/flappy.ico')
pygame.display.set_icon(pygame_icon)

# define font
font = pygame.font.Font('font/Grand9K Pixel.ttf', 39)

# define colours
white = (255, 255, 255)
black = (0, 0, 0)
blue = (122, 197, 205)

# define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
show_tutorial = True
hl_bar = True
max_health = 100
health = 20
ratio = health / max_health
start_game = False

# load images
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/resart_new.png')
tutorial_img = pygame.image.load('img/message.png')


# draw score as text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# reset game when player die
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    hl_bar = True
    return score


# HealthBar
class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))


# create button main menu

start_button = buttin_m.Button(screen_width // 2 - 130, screen_height // 2 - 150, start_img, 1)
exit_button = buttin_m.Button(screen_width // 2 - 110, screen_height // 2 + 50, exit_img, 1)

health_bar = HealthBar(60, 50, 130, 30, 100)

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
coins_groub = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
coin = Coins(int(screen_width / 2)-25, 55)

bird_group.add(flappy)
coins_groub.add(coin)

# create restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

run = True
while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == K_SPACE and flying == False and game_over == False:
            flying = True

    if not start_game:
        # main menu
        screen.fill(blue)
        # add button
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            run = False

    else:

        # draw background
        screen.blit(bg, (0, 0))
        # draw health bar
        if hl_bar:
            health_bar.draw(screen)
        # draw game
        bird_group.draw(screen)
        bird_group.update(flying, game_over, jump_fx)
        pipe_group.draw(screen)
        coins_groub.draw(screen)
        coins_groub.update()

        # draw the ground
        screen.blit(ground_img, (ground_scroll, 600))

        # check the score
        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                    and pass_pipe == False:
                pass_pipe = True

            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    coin_fx.play()
                    pass_pipe = False

        draw_text(str(score), font, white, int(screen_width / 2), 20)

        # look for collision
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            health_bar.hp -= 1
            if health_bar.hp == 0:
                game_over = True
                hl_bar = False
                health_bar.hp = health_bar.max_hp

        # check if bird has hit the ground
        if flappy.rect.bottom >= 600:
            game_over = True
            flying = False

        if game_over == False and flying == True:
            # generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
                top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now

            # draw and scroll the ground
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0

            pipe_group.update(scroll_speed)

        # check for game over and reset
        if game_over:
            death_fx.play(loops=0)
            if button.draw():
                game_over = False
                health_bar = HealthBar(60, 50, 130, 30, 100)
                death_fx.stop()
                score = reset_game()
                hl_bar = True

        # cheek show_tutorial is True
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            show_tutorial = False

        # Display the tutorial image only when show_tutorial is True
        if show_tutorial:
            screen.blit(tutorial_img, (300, 200))

    # quit the game

    pygame.display.update()

pygame.quit()
