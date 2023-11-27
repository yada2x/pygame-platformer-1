import pygame
import sys
from scripts.entities import Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

class Game:
    def __init__(self):
        pygame.init() # Starts up pygame
        pygame.display.set_caption('gamer time')

        self.screen = pygame.display.set_mode((640, 480)) # The window of the game, initalised with a size 640x480
        self.display = pygame.Surface((320, 240)) # Actual surface of the window

        self.clock = pygame.time.Clock() # Limits FPS

        self.movement = [False, False] # Which key we are holding 0 for LEFT 1 for RIGHT
    
        # A dict story all game assets for efficient look up, when asking for an asset it calls a function from utils.py
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), 6),
            'player/run': Animation(load_images('entities/player/run'), 4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
        }

        self.clouds = Clouds(self.assets['clouds'], 16)

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, 16)

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

        self.scroll = [0, 0]

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0)) # Covers everything from the last update, refreshing the screen

            # Special math thing to make it move smoother to the character
            # Take X/Y (player location) and minus from half the width/height to place the character in the centre (otherwise they would be in the top left)
            # We then subtract what we have currently to calculate the distance for the camera to travel
            # Divide by 30 to only apply 1/30th of the distance for smoothness, the larger the distance the faster, the closer the slower.
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2  - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1])) # Deals with floats that cause jittering, this is now applied as the offset.

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for event in pygame.event.get(): # Checks inputs from Windows OS
                if event.type == pygame.QUIT:
                    pygame.quit() # Closes pygame
                    sys.exit() # Closes the application
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update() # Updates the display
            self.clock.tick(60) # Forces 60 FPS

Game().run()