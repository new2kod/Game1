import pygame
import random
import math

class NPCMovement:
    """Class to handle random movement of NPCs."""
    def __init__(self, npc_sprite):
        self.npc = npc_sprite
        self.original_x = npc_sprite.rect.x
        self.original_y = npc_sprite.rect.y
        self.movement_timer = 0
        self.movement_delay = random.randint(3000, 8000)  # Random delay between movements
        self.is_moving = False
        self.move_direction = None
        self.move_distance = 0
        self.move_progress = 0
        self.move_speed = 1  # Pixels per frame
        
    def update(self):
        current_time = pygame.time.get_ticks()
        
        # If not moving, check if it's time to start a new movement
        if not self.is_moving:
            if current_time - self.movement_timer > self.movement_delay:
                self.start_new_movement()
                self.movement_timer = current_time
        else:
            # Continue current movement
            self.continue_movement()
            
    def start_new_movement(self):
        # Randomly decide whether to move or not
        if random.random() < 0.7:  # 70% chance to move
            self.is_moving = True
            self.move_direction = random.choice(["up", "down", "left", "right"])
            self.move_distance = random.randint(10, 40)  # Random distance to move
            self.move_progress = 0
        else:
            # Reset timer for next potential movement
            self.movement_delay = random.randint(2000, 7000)
            
    def continue_movement(self):
        if self.move_progress >= self.move_distance:
            # Movement complete
            self.is_moving = False
            self.movement_delay = random.randint(1000, 6000)
            return
            
        # Move in the chosen direction
        if self.move_direction == "up":
            self.npc.rect.y -= self.move_speed
        elif self.move_direction == "down":
            self.npc.rect.y += self.move_speed
        elif self.move_direction == "left":
            self.npc.rect.x -= self.move_speed
        elif self.move_direction == "right":
            self.npc.rect.x += self.move_speed
            
        self.move_progress += self.move_speed
        
        # Ensure NPC doesn't move too far from original position
        max_distance = 200
        dx = self.npc.rect.x - self.original_x
        dy = self.npc.rect.y - self.original_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > max_distance:
            # Move back toward original position
            angle = math.atan2(dy, dx)
            self.npc.rect.x = self.original_x + int(math.cos(angle) * max_distance)
            self.npc.rect.y = self.original_y + int(math.sin(angle) * max_distance)
            self.is_moving = False  # Stop current movement
