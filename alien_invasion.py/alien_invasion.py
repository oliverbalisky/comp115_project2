import sys
import pygame

from time import sleep
from game_stats import GameStats
from random import randint 
from settings import Settings
from ship import Ship  
from bullet import Bullet
from alien import Alien 
from button import Button 
from scoreboard import Scoreboard 

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")

        
        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        # Create an instance to store game statistics, and create a scoreboard.
        self.sb = Scoreboard(self)

        # Set the background color.
        # self.bg_color = (230, 230, 230)

        self.ship = Ship(self)
   
        self.bullets = pygame.sprite.Group()
       
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

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
        """Create the fleet of aliens."""
        # create an alien and keep adding aliens until there aint no room left
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

    

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2  * alien_width):
                # self._create_alien(random_number_x, random_number_y)
                self._create_alien(current_x,current_y)
                current_x += 2 * alien_width

      

        #this stuff - im not sure if I need :
        # alien_width = alien.rect.width
        # self.aliens.add(alien)

            #finished a row; reset x value and incriment y value.
            current_x = alien_width
            current_y += 2 * alien_height
        
    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""

        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        # new_alien.
        new_alien.rect.y = y_position
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
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
    def _check_fleet_edges(self):
         """Respond appropriately if any aliens have reached an edge."""
         for alien in self.aliens.sprites():
           if alien.check_edges():
             self._change_fleet_direction()
             break
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _update_bullets(self):

        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        
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
        '''self.bullets_x_right or self.bullets_x_left or self.bullets_y_down or'''
        if not self.aliens:
            # destroy  exsititng  bullets  and  create  new fleet .
        
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

        if collisions:
            
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

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
