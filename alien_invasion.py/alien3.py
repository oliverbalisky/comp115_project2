import pygame
from pygame.sprite import Sprite
from settings3 import Settings 


class Alien(Sprite):
  """A class to represent a single alien in the fleet."""
  def __init__(self, ai_game, position, direction):
    """Initialize the alien and set its starting position."""
    super().__init__()
    self.screen = ai_game.screen
    self.settings = ai_game.settings
    self.game_settings = Settings ()
    
    # # Load the alien image and set its rect attribute.
    self.image = pygame.image.load('images/alien.bmp')
    self.rect = self.image.get_rect()

    # Start each new alien near the top left of the screen.
    self.rect.x, self.rect.y = position


    # Store the alien's exact horizontal position.
    self.x = float(self.rect.x)
    self.y = float(self.rect.y)

    self.direction = direction

    

  def update(self):
    
    if self.direction == "top_left":
        self.rect.x += self.settings.alien_speed
        self.rect.y += self.settings.alien_speed
    elif self.direction == "top_right":
        self.rect.x -= self.settings.alien_speed
        self.rect.y += self.settings.alien_speed
    elif self.direction == "bottom_left":
        self.rect.x += self.settings.alien_speed
        self.rect.y -= self.settings.alien_speed
    elif self.direction == "bottom_right":
        self.rect.x -= self.settings.alien_speed
        self.rect.y -= self.settings.alien_speed
    elif self.direction == "bottom_middle":
        self.rect.x += self.settings.alien_speed
        self.rect.y -= self.settings.alien_speed

    if self.rect.right < 0 or self.rect.left > self.settings.screen_width or self.rect.bottom < 0 or self.rect.top > self.settings.screen_height:
            
            self.kill()
            self.remove()
            
            

