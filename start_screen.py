import pygame
import sys
import random
from pygame.locals import *

class StartScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_title = pygame.font.SysFont(None, 64)
        self.font_text = pygame.font.SysFont(None, 32)
        self.font_small = pygame.font.SysFont(None, 24)
        
        # Load character sprites
        self.sprites = {
            'erik': pygame.image.load('assets/images/erik.png'),
            'niamh': pygame.image.load('assets/images/niamh.png'),
            'gus': pygame.image.load('assets/images/gus.png'),
            'nikki': pygame.image.load('assets/images/nikki.png'),
            'paul': pygame.image.load('assets/images/paul.png'),
            'tony': pygame.image.load('assets/images/tony.png'),
            'keelan': pygame.image.load('assets/images/keelan.png'),
            'chris': pygame.image.load('assets/images/chris.png')
        }
        
        # Scale sprites
        for name, sprite in self.sprites.items():
            original_width = sprite.get_width()
            original_height = sprite.get_height()
            self.sprites[name] = pygame.transform.scale(sprite, (original_width * 2, original_height * 2))
        
        # Initialize sprite positions and directions
        self.sprite_positions = {
            'erik': [100, 400, 1, 1],  # [x, y, x_direction, y_direction]
            'niamh': [700, 300, -1, 1],
            'gus': [500, 500, 1, -1],
            'nikki': [300, 200, -1, -1],
            'paul': [600, 600, 1, 1],
            'tony': [200, 500, -1, 1],
            'keelan': [800, 400, 1, -1],
            'chris': [400, 300, -1, -1]
        }
        
        # Speech bubble phrases for each character
        self.speech_phrases = {
            'erik': ["Hi, I'm Erik!", "I love Niamh!", "Can you help me?"],
            'niamh': ["Hello, I'm Niamh!", "I like painting!", "Herbs are fascinating!"],
            'gus': ["Woof! Woof!", "I love kiffiffeffess!", "Treats please!"],
            'nikki': ["Hi there!", "Garden party anyone?", "What theme should I choose?"],
            'paul': ["Where did I park?", "When did I park it?", "Have you seen my car?"],
            'tony': ["Pitu won't let me drive!", "My dog loves treats!", "She drives better than me!"],
            'keelan': ["I love pizza!", "Fine salami is the best!", "Want to hear a riddle?"],
            'chris': ["I almost lost my ear!", "A kitchen fell from the sky!", "I love cool games!"]
        }
        
        # Initialize speech bubbles (None means no active bubble)
        self.active_bubbles = {name: None for name in self.sprites.keys()}
        self.bubble_timers = {name: random.randint(0, 3000) for name in self.sprites.keys()}
        
    def update(self, dt):
        # Update sprite positions
        for name, pos in self.sprite_positions.items():
            # Move sprite
            pos[0] += pos[2] * 0.5  # x position
            pos[1] += pos[3] * 0.5  # y position
            
            # Bounce off screen edges
            if pos[0] < 0 or pos[0] > self.screen_width - self.sprites[name].get_width():
                pos[2] *= -1  # Reverse x direction
            if pos[1] < 0 or pos[1] > self.screen_height - self.sprites[name].get_height():
                pos[3] *= -1  # Reverse y direction
        
        # Update speech bubbles
        for name in self.sprites.keys():
            self.bubble_timers[name] -= dt
            
            if self.bubble_timers[name] <= 0:
                if self.active_bubbles[name] is None:
                    # Create new speech bubble
                    self.active_bubbles[name] = random.choice(self.speech_phrases[name])
                    self.bubble_timers[name] = 3000  # Show for 3 seconds
                else:
                    # Hide speech bubble
                    self.active_bubbles[name] = None
                    self.bubble_timers[name] = random.randint(27000, 33000)  # ~30 seconds until next bubble
    
    def draw(self, surface):
        # Fill background
        surface.fill((100, 150, 255))  # Light blue background
        
        # Draw title
        title_text = self.font_title.render("Erik <3 Niamh : Get Kisses", True, (255, 255, 255))
        surface.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 50))
        
        # Draw storyline text
        storyline = [
            "The best thing is kisses from Niamh, for Erik to get a kiss from Niamh,",
            "but Gus loves them kiffiffeffess too! To get a kiss Eeik has to get his",
            "shit together and use his brain and know random stuff..",
            "Tired of all questions? Eat kebab and keep going!",
            "Can you help Erik get a few?"
        ]
        
        y_offset = 150
        for line in storyline:
            text_surface = self.font_text.render(line, True, (255, 255, 255))
            surface.blit(text_surface, (self.screen_width // 2 - text_surface.get_width() // 2, y_offset))
            y_offset += 30
        
        # Draw controls
        controls = [
            "Controls:",
            "W, A, S, D - Movement",
            "SPACE - Interact with characters / Continue dialogue",
            "E - End interaction",
            "Mouse - Click on answer options"
        ]
        
        y_offset = 300
        for line in controls:
            text_surface = self.font_text.render(line, True, (255, 255, 255))
            surface.blit(text_surface, (self.screen_width // 2 - text_surface.get_width() // 2, y_offset))
            y_offset += 30
        
        # Draw sprites and their speech bubbles
        for name, pos in self.sprite_positions.items():
            # Draw sprite
            surface.blit(self.sprites[name], (int(pos[0]), int(pos[1])))
            
            # Draw speech bubble if active
            if self.active_bubbles[name] is not None:
                self._draw_speech_bubble(surface, name, pos, self.active_bubbles[name])
        
        # Draw "Press SPACE to start" text
        start_text = self.font_title.render("Press SPACE to start", True, (255, 255, 255))
        surface.blit(start_text, (self.screen_width // 2 - start_text.get_width() // 2, 700))
    
    def _draw_speech_bubble(self, surface, name, pos, text):
        # Calculate bubble position (above sprite)
        bubble_x = pos[0] + self.sprites[name].get_width() // 2
        bubble_y = pos[1] - 40
        
        # Render text
        text_surface = self.font_small.render(text, True, (0, 0, 0))
        
        # Calculate bubble size
        padding = 10
        bubble_width = text_surface.get_width() + padding * 2
        bubble_height = text_surface.get_height() + padding * 2
        
        # Draw bubble
        bubble_rect = pygame.Rect(
            bubble_x - bubble_width // 2,
            bubble_y - bubble_height,
            bubble_width,
            bubble_height
        )
        
        # Make sure bubble stays on screen
        if bubble_rect.left < 0:
            bubble_rect.left = 0
        if bubble_rect.right > self.screen_width:
            bubble_rect.right = self.screen_width
        if bubble_rect.top < 0:
            bubble_rect.top = 0
        
        # Draw bubble background
        pygame.draw.rect(surface, (255, 255, 255), bubble_rect, 0, 10)
        pygame.draw.rect(surface, (0, 0, 0), bubble_rect, 2, 10)
        
        # Draw text
        surface.blit(text_surface, (bubble_rect.x + padding, bubble_rect.y + padding))
        
        # Draw pointer
        pointer_points = [
            (bubble_rect.centerx, bubble_rect.bottom),
            (bubble_rect.centerx - 10, bubble_rect.bottom - 10),
            (bubble_rect.centerx + 10, bubble_rect.bottom - 10)
        ]
        pygame.draw.polygon(surface, (255, 255, 255), pointer_points)
        pygame.draw.polygon(surface, (0, 0, 0), pointer_points, 2)
