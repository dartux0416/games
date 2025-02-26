import pygame
import sys
import os

from Button import Button

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()

        # Basic data
        self.character_class = 'noclass'
        self.name = ""
        self.display_name = self.name
        self.age = 0

        # dnd like, dont fucking mind...
        self.strengt = 0
        self.agility = 0
        self.vitality = 0
        self.vigor = 0
        self.intelligence = 0
        self.endurance = 0
        self.dexterity = 0


        # Movement
        self.direction = ''
        self.speed = 5
        self.is_stunned = False

        self.image = pygame.image.load('../assets/images/sprites/player/animation/start/start.png') # Ensure this file exists
        self.is_animating = False
        self.current_sprite = 0
        self.animation_speed = 0.12

        self.actual_animation = []

        self.anim_move_right = []
        self.anim_move_left = []
        self.anim_move_up = []
        self.anim_move_down = []

        self.anim_idle_left = []
        self.anim_idle_right = []

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def idle(self):
        if self.direction == 'r':
            self.switch_animation(self.anim_idle_right)
        elif self.direction == 'l':
            self.switch_animation(self.anim_idle_left)
        if self.direction == 'u':
            self.switch_animation(self.anim_idle_up)
        if self.direction == 'd':
            self.switch_animation(self.anim_idle_down)

    def move(self, speed, direction):
        if not self.is_stunned:
            moving = False
            if direction == 'up':
                self.rect.y -= speed
                self.switch_animation(self.anim_move_up)
                self.direction = 'u'
                moving = True
            elif direction == 'down':
                self.rect.y += speed
                self.switch_animation(self.anim_move_down)
                self.direction = 'd'
                moving = True
            elif direction == 'left':
                self.rect.x -= speed
                self.switch_animation(self.anim_move_left)
                self.direction = 'l'
                moving = True
            elif direction == 'right':
                self.rect.x += speed
                self.switch_animation(self.anim_move_right)
                self.direction = 'r'
                moving = True

            if not moving:
                self.idle()

    def update(self, events):
        if self.is_animating:
            self.current_sprite += self.animation_speed
            if self.current_sprite >= len(self.actual_animation):
                self.current_sprite = 0
                self.is_animating = False
            self.image = self.actual_animation[int(self.current_sprite)]


    def load_animation(self, foldername):
        images = []
        for file in sorted(
            os.listdir(foldername),
            key=lambda x: int(''.join(filter(str.isdigit, x))) if any(c.isdigit() for c in x) else float('inf')):
            full_path = os.path.join(foldername, file)
            if os.path.isfile(full_path):
                images.append(pygame.image.load(full_path))
        return images

    def switch_animation(self, new_animation):
        if self.actual_animation != new_animation:
            self.actual_animation = new_animation
            self.current_sprite = 0
        self.is_animating = True

    def animate(self):
        self.is_animating = True

    def update(self, events):
        if self.is_animating:
            self.current_sprite += self.animation_speed
            if self.current_sprite >= len(self.actual_animation):
                self.current_sprite = 0
                self.is_animating = False
            self.image = self.actual_animation[int(self.current_sprite)]


class Player(Entity):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

    def move_keys(self, events):
        keys = pygame.key.get_pressed()
        moving = False
        local_speed = self.speed

        if not self.is_stunned:
            # Diagonal movements
            if keys[pygame.K_d] and keys[pygame.K_w]:  # Move up-right
                local_speed = self.speed/1.4
                self.direction = 'r'
                self.rect.x += local_speed
                self.rect.y -= local_speed
                self.switch_animation(self.anim_move_up)
                moving = True
            elif keys[pygame.K_a] and keys[pygame.K_w]:  # Move up-left
                local_speed = self.speed/1.4
                self.direction = 'l'
                self.rect.x -= local_speed
                self.rect.y -= local_speed
                self.switch_animation(self.anim_move_up)
                moving = True
            elif keys[pygame.K_d] and keys[pygame.K_s]:  # Move down-right
                local_speed = self.speed/1.4
                self.direction = 'r'
                self.rect.x += local_speed
                self.rect.y += local_speed
                self.switch_animation(self.anim_move_down)
                moving = True
            elif keys[pygame.K_a] and keys[pygame.K_s]:  # Move down-left
                local_speed = self.speed/1.4
                self.direction = 'l'
                self.rect.x -= local_speed
                self.rect.y += local_speed
                self.switch_animation(self.anim_move_down)
                moving = True
            # Single axis movements
            elif keys[pygame.K_d]:  # Move right
                local_speed = self.speed
                self.direction = 'r'
                self.rect.x += local_speed
                self.switch_animation(self.anim_move_right)
                moving = True
            elif keys[pygame.K_a]:  # Move left
                local_speed = self.speed
                self.direction = 'l'
                self.rect.x -= local_speed
                self.switch_animation(self.anim_move_left)
                moving = True
            elif keys[pygame.K_w]:  # Move up
                local_speed = self.speed
                self.rect.y -= local_speed
                self.direction = 'u'
                self.switch_animation(self.anim_move_up)
                moving = True
            elif keys[pygame.K_s]:  # Move down
                local_speed = self.speed
                self.rect.y += local_speed
                self.direction = 'd'
                self.switch_animation(self.anim_move_down)
                moving = True

        for event in events:
            if event.type == pygame.KEYUP:
                if not any(pygame.key.get_pressed()):
                    self.idle()

            if not moving:
                self.idle()


# ============================ STAGES & SCREENS ================================

def pause():
    pygame.mouse.set_visible(True)

    resume_button = Button(
        screen,
        50, 50,
        200, 50,
        "Unpause",
        pygame.font.Font('../assets/fonts/font.ttf', 30),
        ((255, 0, 0), (0, 255, 0), (0, 0, 255)),
        ((70, 70, 70), (70, 255, 20), (10, 40, 255)),
        ((0, 0, 0), (40, 255, 23), (50, 80, 255)),
        opacity=100
    )

    quit_button = Button(
        screen,
        50, 120,
        200, 50,
        "Exit",
        pygame.font.Font('../assets/fonts/font.ttf', 30),
        ((255, 0, 0), (0, 255, 0), (0, 0, 255)),
        ((70, 70, 70), (70, 255, 20), (10, 40, 255)),
        ((0, 0, 0), (40, 255, 23), (50, 80, 255)),
        opacity=100
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Exit intro on ESC key

            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.handle_event(event):
                    return  # Exit the intro and start the game
                elif quit_button.handle_event(event):
                    quit_sure()

        # Drawing
        screen.fill((30, 80, 200))

        resume_button.draw()
        quit_button.draw()

        pygame.display.flip()
        clock.tick(60)

def quit_sure():
    pygame.mouse.set_visible(True)

    resume_button = Button(
        screen,
        150, 200,
        200, 50,
        "Back",
        pygame.font.Font('../assets/fonts/font.ttf', 30),
        ((255, 0, 0), (0, 255, 0), (0, 0, 255)),
        ((70, 70, 70), (70, 255, 20), (10, 40, 255)),
        ((0, 0, 0), (40, 255, 23), (50, 80, 255)),
        opacity=100
    )

    quit_button = Button(
        screen,
        450, 200,
        200, 50,
        "Exit",
        pygame.font.Font('../assets/fonts/font.ttf', 30),
        ((255, 0, 0), (0, 255, 0), (0, 0, 255)),
        ((70, 70, 70), (70, 255, 20), (10, 40, 255)),
        ((0, 0, 0), (40, 255, 23), (50, 80, 255)),
        opacity=100
    )

    s = pygame.Surface((800, 800))
    s.set_alpha(100)
    s.fill((0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Exit intro on ESC key

            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.handle_event(event):
                    return  # Exit the intro and start the game
                elif quit_button.handle_event(event):
                    pygame.quit()
                    sys.exit()  # Exit the game

        # Drawing
        screen.fill((30, 80, 200))

        screen.blit(s, (0, 0))

        resume_button.draw()
        quit_button.draw()

        pygame.display.flip()
        clock.tick(60)



pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.mouse.set_visible(False)

player = Player(100, 100)

player.anim_move_right = player.load_animation('../assets/images/sprites/player/animation/anim_walk_right')
player.anim_move_left = player.load_animation('../assets/images/sprites/player/animation/anim_walk_left')
player.anim_move_up = player.load_animation('../assets/images/sprites/player/animation/anim_walk_up')
player.anim_move_down = player.load_animation('../assets/images/sprites/player/animation/anim_walk_down')

player.anim_idle_right = player.load_animation('../assets/images/sprites/player/animation/anim_idle_right')
player.anim_idle_left = player.load_animation('../assets/images/sprites/player/animation/anim_idle_left')
player.anim_idle_up = player.load_animation('../assets/images/sprites/player/animation/anim_idle_up')
player.anim_idle_down = player.load_animation('../assets/images/sprites/player/animation/anim_idle_down')

player.anim_idle = player.load_animation('../assets/images/sprites/player/animation/anim_idle')

player.actual_animation = player.anim_move_right

player_group = pygame.sprite.Group()
player_group.add(player)

screen.fill("White")

pause()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pause()

    screen.fill((30, 30, 30))

    player.move_keys(events)
    player_group.draw(screen)
    player_group.update(events)

    pygame.display.flip()
    clock.tick(60)
