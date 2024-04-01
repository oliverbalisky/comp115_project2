class Settings:
   """A class to store all settings for Alien Invasion."""
   def __init__(self):
     """Initialize the game's static settings."""

     #background settings
     self.screen_width = 1200
     self.screen_height = 800
     self.bg_color = (0, 0, 0)

     #ship settings 
     self.ship_speed = 8
     self.ship_limit = 5
     
     #bullet settings 
     self.bullet_speed = 30.5
     self.bullet_width = 10
     self.bullet_height = 10
     self.bullet_color = (240, 0, 0)
     self.bullets_allowed = 50

     # alien settings 
     self.aliens_allowed = 15
     self.alien_hit_list = []

     # how quickly the game speeds up 
     self.speedup_scale = 1.1

     # how quicly the alien point values increase 
     self.score_scale = 1.5
     self.initialize_dynamic_settings()
  
   def initialize_dynamic_settings(self):
    """Initialize settings that change throughout the game."""

    self.alien_speed = 1.0

    # scoring poit settings 
    self.alien_points = 50

   def increase_speed(self):
    """Increase speed settings and alien point values."""

    self.alien_speed *= self.speedup_scale

    self.alien_points = int(self.alien_points * self.score_scale)
 