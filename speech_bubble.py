import pygame
import random

class SpeechBubble:
    def __init__(self, font_size=20):
        self.font = pygame.font.SysFont(None, font_size)
        self.active_bubbles = {}  # {npc_name: {"text": text, "timer": timer}}
        self.bubble_timers = {}   # {npc_name: countdown_to_next_bubble}
        
        # Speech phrases for each character
        self.speech_phrases = {
            'Niamh': ["I'm Niamh!", "I love painting!", "Herbs are fascinating!"],
            'Gus': ["Woof! Woof!", "I love kiffiffeffess!", "Treats please!"],
            'Nikki': ["Hi there!", "Garden party anyone?", "What theme should I choose?"],
            'Paul': ["Where did I park?", "When did I park it?", "Did I park my car?"],
            'Tony': ["Pitu won't let me drive!", "She ate all the snacks!", "She drives better than me!"],
            'Keelan': ["I love pizza!", "Fine salami is the best!", "Want to hear a riddle?"],
            'Tain': ["Good day, old chap!", "Fascinating migratory patterns!", "Ha ha ha!"],
            'Chris': ["I almost lost my ear!", "A kitchen fell from the sky!", "I love cool games!"],
            'Magda': ["Dogs feelings hurt when you no pet them.", "Sad dogs I see in rain.", "Dogs dream about running, yes?"]
        }
        
        # Initialize timers for each NPC
        for name in self.speech_phrases.keys():
            self.bubble_timers[name] = random.randint(0, 10000)  # Random initial delay
            self.active_bubbles[name] = None
    
    def update(self, dt, npcs):
        # Update speech bubbles for all NPCs
        for npc in npcs:
            name = npc.name
            
            # Skip if NPC doesn't have speech phrases
            if name not in self.speech_phrases:
                continue
                
            # Update timer
            if name in self.bubble_timers:
                self.bubble_timers[name] -= dt
                
                if self.bubble_timers[name] <= 0:
                    if self.active_bubbles[name] is None:
                        # Create new speech bubble
                        self.active_bubbles[name] = {
                            "text": random.choice(self.speech_phrases[name]),
                            "timer": 5000  # Show for 3 seconds
                        }
                    else:
                        # Hide speech bubble
                        self.active_bubbles[name] = None
                        self.bubble_timers[name] = 15000  # 30 seconds until next bubble
                
                # Update active bubble timer
                if self.active_bubbles[name] is not None:
                    self.active_bubbles[name]["timer"] -= dt
                    if self.active_bubbles[name]["timer"] <= 0:
                        self.active_bubbles[name] = None
                        self.bubble_timers[name] = 30000  # 30 seconds until next bubble
    
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
