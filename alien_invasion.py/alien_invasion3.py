import sys
import pygame
import random

from time import sleep
from game_stats import GameStats
from random import randint
from settings3 import Settings
from ship import Ship  
from bullet import Bullet
from alien3 import Alien 
from button import Button 
from scoreboard import Scoreboard 

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""

        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")
 
        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        # Create an instance to store game statistics, and create a scoreboard.
        self.sb = Scoreboard(self)

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
       
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.alien_hit_list = []

        # Start Alien Invasion in an active state.
        self.game_active = False

        # make the play button.
        self.play_button = Button(self,"Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update_ship()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            self.clock.tick(60)      
    
    def _check_events(self):
            """Respond to keypresses and mouse events."""
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    sys.exit() 

                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:

            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
       
            # Reset the game statistics.
            self.stats.reset_stats()
            self.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right.   
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True   
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_w: 
            self._fire_bullet("K_w")
        elif event.key == pygame.K_d:
            self._fire_bullet("K_d")
        elif event.key == pygame.K_a:
            self._fire_bullet("K_a")
        elif event.key == pygame.K_s:
            self._fire_bullet("K_s")
           

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False 
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self, event):
        """create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed and event=='K_w':
            
            # self.bullet.moving_up = True
            new_bullet = Bullet(self, "up")
            self.bullets.add(new_bullet)

        elif len(self.bullets) < self.settings.bullets_allowed and event=='K_s':
     
            new_bullet = Bullet(self, "down")
            self.bullets.add(new_bullet)
            

        elif len(self.bullets) < self.settings.bullets_allowed and event=='K_d':
           
            new_bullet = Bullet(self, "right")
            self.bullets.add(new_bullet)
        
            
        elif len(self.bullets) < self.settings.bullets_allowed and event=='K_a':

            new_bullet = Bullet(self, "left")
            self.bullets.add(new_bullet)

        
    def _create_fleet(self):

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.alien_width = self.rect.x
        self.alien_height = self.rect.y

        """Create the fleet of aliens."""

        # for side in range(self.settings.aliens_allowed):
        side = random.choice(["top_left", "top_right", "bottom_left", "bottom_right", "bottom_middle"])


        if len(self.aliens) < self.settings.aliens_allowed and side == "top_left":
            x = random.randint(0, self.settings.screen_width - self.alien_width)
            y = -self.alien_height
            position = (x,y)

        elif len(self.aliens) < self.settings.aliens_allowed and side == "top_right":
            x = random.randint(0, self.settings.screen_width - self.alien_width)
            y = -self.alien_height
            position = (x,y)
    
        elif len(self.aliens) < self.settings.aliens_allowed and side == "bottom_left":
            x = -self.alien_width
            y = random.randint(0, self.settings.screen_height - self.alien_height)
            position = (x,y)

        elif len(self.aliens) < self.settings.aliens_allowed and side == "bottom_right":
            x = self.settings.screen_width
            y = random.randint(0, self.settings.screen_height - self.alien_height)
            position = (x,y)

        elif len(self.aliens) < self.settings.aliens_allowed and side == "bottom_middle":
            x = random.randint(0,self.settings.screen_width)
            y = self.settings.screen_height - self.alien_height
            position = (x,y)
        new_alien = Alien(self, position, side)
        self.aliens.add(new_alien)



    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard 
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
     
            self.aliens.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)  
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    


    def _update_aliens(self):
        # """Check if the fleet is at an edge, then update positions."""
       
        if len(self.aliens) < self.settings.aliens_allowed:  # Control the number of aliens spawned at a time
            self._create_fleet()

        self.aliens.update()

        for alien in self.aliens:    
            if pygame.sprite.groupcollide(self.bullets, self.aliens, True, True):
                self.aliens.remove(alien)

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        if self.game_active == False:
            self.alien_hit_list.clear()


    def _update_bullets(self):

        """Update position of bullets and get rid of old bullets."""

        self.bullets.update()
        
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.bottom >= self.settings.screen_height:
                self.bullets.remove(bullet)

        for bullet in self.bullets.copy():
             if bullet.rect.left >= self.settings.screen_width or bullet.rect.right <= 0:
                self.bullets.remove(bullet)

        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):

        # respond to bullet - alien collisions 
        # remove any bullets and aliens that have collided 
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if not self.aliens:
            # destroy  exsititng  bullets  and  create  new fleet .
        
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()


        if collisions:
            
            if int(len(self.alien_hit_list)) % 15 == 0:
                self.settings.increase_speed()
            
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.settings.alien_hit_list.append(1)
   
            self.sb.prep_score()
            self.sb.check_high_score()
            self._create_fleet()

            self.alien_hit_list.append(1)

    def _update_screen(self):
            """update images on screen, and flip to the new screen"""
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitme()
            self.aliens.draw(self.screen)
            # Draw the score information.
            self.sb.show_score()

            # Draw the play button if the game is inactive.
            if not self.game_active:
                self.play_button.draw_button()

            pygame.display.flip()
            

if __name__ == '__main__':
        # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

