import pygame
import random
import math

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, food_type):
        super().__init__()
        self.food_type = food_type
        self.load_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.energy_value = 10  # Each food item restores 10% energy
        
    def load_image(self):
        if self.food_type == "pizza":
            self.image = pygame.image.load('assets/images/pizza.png')
        elif self.food_type == "kebab":
            self.image = pygame.image.load('assets/images/kebab.png')
        elif self.food_type == "meatball":
            self.image = pygame.image.load('assets/images/meatball.png')
        elif self.food_type == "apple":
            self.image = pygame.image.load('assets/images/apple.png')
        else:
            # Default to apple if type is unknown
            self.image = pygame.image.load('assets/images/apple.png')
            
        # Make sprite twice the size
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (original_width * 2, original_height * 2))
