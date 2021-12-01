from os import write
import pygame
import random
import csv # csv for highscore
from pygame import display
from color_library import *
import prompt as pr

pygame.init() 

# Lets load the game images and put them into variables
player_image = pygame.image.load('images/player_pad.png')
missile_image = pygame.image.load('images/missile.png')
asteroids_image = pygame.image.load('images/asteroids.png')
explosion_image = pygame.image.load('images/explosion.png')

# Lets create different variations of asteroids!
# aOID = asteroid
aOID_sheet = list()
aOID_width, aOID_height = asteroids_image.get_size()
# lets divide the images on the png to different elements on the list!
for row in range(int(aOID_height/35)): # height of each asteroid is 20px
    for column in range(int(aOID_width/35)): # width of each asteroid is 20px
        aOID_sheet.append(asteroids_image.subsurface((column*35, row*35, 35, 35)))
number_of_aOIDs = len(aOID_sheet)

# Lets create different variations of explosions!
# exPLO = explosion
exPLO_sheet = list()
exPLO_width, exPLO_height = explosion_image.get_size()
# lets divide the images on the png to different elements on the list!
for row in range(int(exPLO_height/35)): # height of each asteroid is 20px
    for column in range(int(exPLO_width/35)): # width of each asteroid is 20px
        exPLO_sheet.append(explosion_image.subsurface((column*35, row*35, 35, 35)))
number_of_exPLOs = len(exPLO_sheet)
current_frame = 0

# If we want to use sprites we create a class that inherits from the Sprite class.
# Each class has an associated image and a rectangle.
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = aOID_sheet[random.randint(0,(number_of_aOIDs-1))]
        self.rect = self.image.get_rect()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.clock = 0
    def new_frame(self):
        self.clock += 1
        image = exPLO_sheet[self.clock-1]
        return image
    def cords_of_explosion(self):
        return (self.x_pos, self.y_pos)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.rect = self.image.get_rect()


class Missile(pygame.sprite.Sprite,):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_image
        self.rect = self.image.get_rect()

# Read CSV file of highscores
# highscore
with open('high_score.csv', 'r', encoding='utf-8') as score_file:
    reader = csv.reader(score_file)
    top_scores = []
    for element in reader:
        top_scores.append(element)
    if len(top_scores) != 0:
        if top_scores[-1] == '':
            top_scores.pop(-1)

# Screen
screen_width = 960
screen_height = 540
screen_ratio = screen_width/screen_height
screen_size = (screen_width, screen_height)
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_icon(aOID_sheet[0])
pygame.display.set_caption('AST BLASTER!')

# RWD FEATURES
base_font_size = {
    'GAME OVER' : 33,
}

# stars - background
stars = []
for star in range(35):
    star_loc_x = random.randrange(0, screen_width)
    star_loc_y = random.randrange(0, screen_height)
    stars.append([star_loc_x, star_loc_y])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
asteroid_list = pygame.sprite.Group()

# Group to hold missiles
missile_list = pygame.sprite.Group()

# This is a list of every sprite.
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List holding explosions  
explosion_list = list()

# shooting feature
def shoot(gun):
    shot = Missile()
    if gun == 'from left gun':
        shot.rect.x = player.rect.x + 7
    if gun == 'from right gun':
        shot.rect.x = player.rect.x + 31
    shot.rect.y = player.rect.y +8
    missile_list.add(shot)
    all_sprites_list.add(shot)   

# Create a player block
player = Player()
player.rect.x = (screen_width/2) - 21
player.rect.y = screen_height-40

all_sprites_list.add(player)

# Loop until the user clicks the close button.
running = True
game_on = True

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
score = 0
timer = 0
player_name = ''
waiting_for_saving = True
input_boxes = []

# -------- Main Program Loop -----------
while running:
    # Background
    screen.fill(BLACK)
    for star in stars:
        star[1] += 4
        if star[1] > screen_height:
            star[0] = random.randrange(0, screen_width)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(screen, LIGHTSLATEGREY, star, 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_on == True:
                shoot('from left gun')
                shoot('from right gun')
        for box in input_boxes:
            box.handle_event(event)
    
    if game_on:           
        if timer == 120:
            for i in range(4):
                block = Asteroid()
                # Set a random location for the block
                block.rect.x = random.randint(20, screen_width-20)
                block.rect.y = random.randint(-100, -20)  # don't let the asteroids start to low
                asteroid_list.add(block)
                all_sprites_list.add(block)
                timer = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            if player.rect.x < -42:
                player.rect.x = screen_width
            player.rect.x -= 8
        elif key[pygame.K_RIGHT]:
            if player.rect.x > screen_width:
                player.rect.x = -42
            player.rect.x += 8

        # See if a player's missile has collided with an asternoid.
        # if so: remove both of them from their lists.
            
        if score == 0:
            None
        else:
            score_display = pr.Message(screen_size, 'Score: '+str(score), 20)
            screen.blit(score_display.get_render(), score_display.align('right', int(score_display.text_height/2), 15))
            
        # Missiles move at a constant speed up the screen, towards the enemy
        for shot in missile_list:
            shot.rect.y -= 15

        # All the asteroids move down the screen at a constant speed
        for asteroid in asteroid_list:
            asteroid.rect.y += 3
        
        # Draw all the spites
        all_sprites_list.draw(screen)

        #Draw all explosions in their current posistions
        for explosion in explosion_list:
            if explosion.clock == 16:
                explosion_list.remove(explosion)
            else:
                screen.blit(explosion.new_frame(), explosion.cords_of_explosion())
        
        # Check if a missile has hit an asteriod
        collision_dict = pygame.sprite.groupcollide(missile_list, asteroid_list, True, True) # group comparrsion list
        for sprite in collision_dict: # check each element of both lists
            if collision_dict[sprite]: # any two are colliding, remove both from their lists
                score += 1 # score goes up by one
                explosion_list.append(Explosion(sprite.rect.x, sprite.rect.y))
    
    # check if game is still running
    for block in asteroid_list:
        if block.rect.y >= (screen_height-35):
                 game_on = False
    if game_on == False:
        # Harðkóðaðar upplýsingar sem að breytast ekki
        display_lost = pr.Message(screen_size, 'GAME OVER', round(base_font_size['GAME OVER']*screen_ratio))
        display_score = pr.Message(screen_size, ('YOUR SCORE: '+str(score)), 30)
        display_scoreboard_header = pr.Message(screen_size, 'TOP 10 HIGH SCORES', 20,)
        display_creator = pr.Message(screen_size, 'Created by Axel Bjarkar', 10)

        screen.blit(display_lost.get_render(), display_lost.center(10))
        screen.blit(display_score.get_render(), display_score.center(75))
        screen.blit(display_scoreboard_header.get_render(), display_scoreboard_header.align('right', 200, 10))
        screen.blit(display_creator.get_render(), display_creator.align('left', 520, 10))

        # Save takki
        if waiting_for_saving == True:
            display_save_score = pr.Message(screen_size, 'SAVE SCORE', 20)
            screen.blit(display_save_score.get_render(), display_save_score.align('left', 200, 10))
            input_boxes.append(pr.InputBox(screen, 10, 230, display_save_score.text_width, 32, '', WHITE, WHITE, True))
            for box in input_boxes:
                box.update()
                box.draw()
                if box.finished():
                    waiting_for_saving = False
                    player_name = box.get_text()
        else:
            display_save_score = pr.Message(screen_size, 'SCORE SAVED!', 25)
            screen.blit(display_save_score.get_render(), display_save_score.align('left', 200, 10))

        # Topp 5 spilendur, allra tíma
        count = 0
        modifier = 30
        for top_score in top_scores:
            if count == 10:
                break
            display_p = pr.Message(screen_size, top_score[0], 16)
            display_pscore = pr.Message(screen_size, top_score[1], 16)
            screen.blit(display_p.get_render(), display_p.align('right', 200+modifier, 10))
            screen.blit(display_pscore.get_render(), display_pscore.align('right', 200+modifier, display_scoreboard_header.y_pos))
            modifier += 25
            count += 1
        
    # Limit to 60 frames per second
    clock.tick(60)
    timer += 1
    current_frame += 1
    if current_frame > 16:
        current_frame = 0

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

if player_name != '':
    top_scores.append([player_name, score])
    top_scores.sort(key = lambda x: int(x[1]), reverse=True)
    print(top_scores)

    with open('high_score.csv', 'w', encoding='utf-8', newline='') as score_file:
        writer = csv.writer(score_file)
        for every_score in top_scores:
            print(every_score)
            writer.writerow(every_score)