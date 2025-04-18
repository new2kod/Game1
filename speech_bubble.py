import pygame
import random

class SpeechBubble:
    def __init__(self, font_size=20):
        self.font = pygame.font.SysFont(None, font_size)
        self.active_bubbles = {}  # {npc_name: {"text": text, "timer": timer}}
        self.bubble_timers = {}   # {npc_name: countdown_to_next_bubble}
        
        # Speech phrases for each character
        self.speech_phrases = {
            'Niamh': ["I'm Niamh!", "I love painting!", "Gus come back here!"],
            'Gus': ["Woof! Woof!", "Ima good boy!", "Snacks please!"],
            'Nikki': ["Hi there!", "Garden party anyone?", "Pssst, wanna hear the latest?"],
            'Paul': ["Where did I park?", "Did I park the car?", "I'm at the Airport!", "I have to be at the Airport!"],
            'Tony': ["Pitu won't let me drive!", "Pitu ate all the cookie!", "Pitu drives better than me!"],
            'Keelan': ["I love pizza!", "GABAGOOL!", "Want to hear a riddle?"],
            'Tain': ["Good day, old chap!", "Fascinating migratory patterns!", "Ha ha ha!", "Thats hillarious"],
            'Chris': ["I almost lost my ear!", "A kitchen fell from the sky!", "Bloody wankers!"],
            'Magda': ["Dogs feelings hurt when you no pet them.", "Sad dogs I see in rain.", "Maaaartin?", "0,3 of something", "Dogs dream about running, yes?"],
            'Ivan': ["Hey, its Ivan", "let's play some pool!", "Is my hair okay?", "Do you have a shower?"]
        }
        
        # Initialize timers for each NPC
        for name in self.speech_phrases.keys():
            self.bubble_timers[name] = random.randint(3000, 20000)  # Random initial delay
            self.active_bubbles[name] = None
    
    def update(self, dt, npcs):
        # Update speech bubbles for all NPCs
        for npc in npcs:
            name = npc.name
            
            # Skip if NPC doesn't have speech phrases
            if name not in self.speech_phrases:
                continue
                
            # If no active bubble, count down to next bubble
            if self.active_bubbles[name] is None:
                self.bubble_timers[name] -= dt
                if self.bubble_timers[name] <= 0:
                    # Create new speech bubble
                    self.active_bubbles[name] = {
                        "text": random.choice(self.speech_phrases[name]),
                        "timer": 8000  # Show for 8 seconds
                    }
                    self.bubble_timers[name] = 15000  # 30 seconds until next bubble
            else:
                # Update active bubble timer
                self.active_bubbles[name]["timer"] -= dt
                if self.active_bubbles[name]["timer"] <= 0:
                    self.active_bubbles[name] = None
                    self.bubble_timers[name] = 15000  # 30 seconds until next bubble
    
    def draw(self, surface, npcs):
        # Draw speech bubbles for all NPCs
        for npc in npcs:
            name = npc.name
            
            # Skip if NPC doesn't have an active bubble
            if name not in self.active_bubbles or self.active_bubbles[name] is None:
                continue
                
            # Draw speech bubble
            self._draw_speech_bubble(surface, npc, self.active_bubbles[name]["text"])
    
    def _draw_speech_bubble(self, surface, npc, text):
        # Calculate bubble position (above sprite)
        bubble_x = npc.rect.centerx
        bubble_y = npc.rect.top - 10
        
        # Render text
        text_surface = self.font.render(text, True, (0, 0, 0))
        
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
        screen_width, screen_height = surface.get_size()
        if bubble_rect.left < 0:
            bubble_rect.left = 0
        if bubble_rect.right > screen_width:
            bubble_rect.right = screen_width
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