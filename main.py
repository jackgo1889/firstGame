import pygame
from sys import exit
from random import randint, choice

# Player Class (inherits from pygame.Sprite class)
class Player(pygame.sprite.Sprite):

    # Constructor Method
    def __init__(self):

        # Inherit from Sprite Class
        super().__init__()

        # Import images of player, store in list
        player_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_1, player_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/audio_jump.mp3')
        self.jump_sound.set_volume(0.5)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_movement(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index > len(self.player_walk):
                self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_movement()

class Obstacle(pygame.sprite.Sprite):


    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.y < -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    # empty list in python evaluates to false
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        # Only copy existing item in the list if the obstacle is on the screen
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list

    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 300:
        # jump
        player_surface = player_jump
    else:
        # walk
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

# Starts and initializes pygame
pygame.init()


# Display a screen
width, height = 800, 400
screen = pygame.display.set_mode((width, height))

# Gives a title to the screen
pygame.display.set_caption("fuck bitches get money, respectfully")

# Creates a clock
clock = pygame.time.Clock()

# Fonts
font_type, font_size = 'font/Pixeltype.ttf', 50
test_font = pygame.font.Font(font_type, font_size)
intro_surf = test_font.render('Jump, bitch.', False, (111, 196, 169))
intro_rect = intro_surf.get_rect(center=(400, 100))
close_surf = test_font.render('Jump higher breh...', False, (111, 196, 169))
close_rect = close_surf.get_rect(center=(400, 100))


# Initialize active game state
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.5)
bg_music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Backgrounds
sky = pygame.image.load('graphics/sky.png').convert()
ground = pygame.image.load('graphics/ground.png').convert()

# Snail
#snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
#snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
#snail_frames = [snail_frame_1, snail_frame_2]

#snail_frame_index = 0
#snail_surf = snail_frames[snail_frame_index]

# Fly
#fly_frame_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
#fly_frame_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
#fly_frames = [fly_frame_1, fly_frame_2]

#fly_frame_index = 0
#fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

# Player
#player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
#player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
#player_walk = [player_walk_1,player_walk_2]
#player_index = 0
#player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

# Takes player surface and draws rectangle around it
#player_surface = player_walk[player_index]
#player_rect = player_surface.get_rect(midbottom=(80, 300))

# Initializes gravity for player
#player_gravity = 0

# Intro Screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_message = test_font.render('Press any key to start', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

"""
Screen is displayed only while True,
have to break within the while loop to quit.
"""

# Timers

# create custom user event
obstacle_timer = pygame.USEREVENT + 1

# triggers obstacle every 1200 milliseconds
pygame.time.set_timer(obstacle_timer, 1200)

#snail_animation_timer = pygame.USEREVENT + 2
#pygame.time.set_timer(snail_animation_timer, 300)

#fly_animation_timer = pygame.USEREVENT + 3
#pygame.time.set_timer(fly_animation_timer, 200)
while True:
    # looks for all possible player inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # un-initializes pygame
            pygame.quit()
            exit()

        if game_active:
            # Checks for mouse movement
            # if event.type == pygame.MOUSEMOTION:
            # if player_rect.collidepoint(event.pos):
            # print('collision')

            # Checks for mouse press
            #if event.type == pygame.MOUSEBUTTONDOWN:
                #if player_rect.collidepoint(event.pos):
                    #player_gravity = -20

            # Checks for mouse release
            #if event.type == pygame.MOUSEBUTTONUP:
                #print("mouse up")

            # Check for space press
            #if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_SPACE:

                    # Jump only if Player is on ground
                    #if player_rect.bottom == 300:
                        #player_gravity = -20

            # Spawn an obstacle
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                # Triggers True (1), or False (0)
                # if randint(0, 2):
                    # obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                # else:
                    # obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))

            # Snail animation
            #if event.type == snail_animation_timer:
                #if snail_frame_index == 0:
                    #snail_frame_index = 1
                #else:
                    #snail_frame_index = 0

                #snail_surf = snail_frames[snail_frame_index]

            # Fly animation
            #if event.type == fly_animation_timer:
                #if fly_frame_index == 0:
                    #fly_frame_index = 1
                #else:
                    #fly_frame_index = 0

                #fly_surf = fly_frames[fly_frame_index]
        else:
            if event.type == pygame.KEYDOWN:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        # Check for key release
        # if event.type == pygame.KEYUP:
        # print('key up')

    """
    Attaches surfaces to the screen
    Surfaces are applied in the order called
    (0,0) is the top left
    down = increase y
    right = increase x
    """
    if game_active:
        x, y = 0, 0
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))
        score = display_score()

        # Drawing rectangle around the score
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # screen.blit(score_surf, score_rect)

        # Drawing line from the top left to the bottom right of the screen
        # pygame.draw.line(screen, 'red', (0, 0), (800, 400))

        # Drawing an ellipse specifically defining its dimensions
        # pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50, 200, 100, 100))

        """
        Drawing a moving surface
        Keep in mind that without a proper background
        display.update() will continuously generate snail
        w/o getting rid of it, looks sloppy!
        """
        # moves the snail left
        # snail_movement = 5
        # snail_rect.x -= snail_movement

        # stores all possible key inputs
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        # print('jump')

        # Initializing snail
        # screen.blit(snail1, snail_rect)

        # Initializing Player
        # player_gravity += 1
        # player_rect.y += player_gravity

        # Creating Floor
        # if player_rect.bottom >= 300:
            # player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surface, player_rect)

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collision_sprite()

    # gives x, y coordinates of mouse
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    # print(pygame.mouse.get_pressed())

    # Runs when game ends
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))

        if score == 0:
            screen.blit(intro_surf, intro_rect)
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(close_surf, close_rect)
            screen.blit(score_message, score_message_rect)

    """
    rect1.collidepoint((x,y))
    + using the mouse
    """
    # updates the display
    pygame.display.update()

    # sets maximum constant frame rate
    clock.tick(60)
