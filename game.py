import pygame
import sys
import os
import math
import random
from pygame.locals import *
from food import Food
from sign import Sign
from npc_movement import NPCMovement
from game_modifications import GameModifications
from speech_bubble import SpeechBubble

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 780
FPS = 60
TITLE = "Erik <3 Niamh"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Player movement speed
PLAYER_SPEED = 5

# Global flag for sound availability
SOUND_ENABLED = True

# Try to initialize the mixer for sound
try:
    pygame.mixer.init()
except pygame.error:
    SOUND_ENABLED = False
    print("Sound initialization failed. Game will run without sound.")

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/images/erik.png')
        # Make sprite twice the size
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (original_width * 2, original_height * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PLAYER_SPEED
        self.direction = "down"  # Default direction
        self.energy = 100  # Full energy
        
    def update(self, keys, obstacles):
        # Store original position to revert if collision occurs
        original_x = self.rect.x
        original_y = self.rect.y
        
        # Handle movement
        if keys[K_w]:  # Up
            self.rect.y -= self.speed
            self.direction = "up"
        if keys[K_s]:  # Down
            self.rect.y += self.speed
            self.direction = "down"
        if keys[K_a]:  # Left
            self.rect.x -= self.speed
            self.direction = "left"
        if keys[K_d]:  # Right
            self.rect.x += self.speed
            self.direction = "right"
            
        # Check for collisions with obstacles
        if obstacles:
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle.rect):
                    # Revert to original position if collision
                    self.rect.x = original_x
                    self.rect.y = original_y
                    break
        
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def reduce_energy(self, amount):
        self.energy -= amount
        if self.energy < 0:
            self.energy = 0
        return self.energy
        
    def add_energy(self, amount):
        self.energy += amount
        if self.energy > 100:
            self.energy = 100
        return self.energy

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_name, name):
        super().__init__()
        self.image = pygame.image.load(f'assets/images/{sprite_name}.png')
        # Make sprite twice the size
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (original_width * 2, original_height * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.interaction_radius = 50  # Increased due to larger sprites
        self.dialogues = []
        self.questions = []
        self.current_dialogue = 0
        self.current_question = 0
        self.wrong_answers = 0  # Track wrong answers
        self.question_order = []  # List to store shuffled question indices
        self.dialogue_order = []  # List to store dialogue sequence (first + 3 random)
        self.shuffle_questions()  # Initialize with shuffled question order
        self.setup_dialogue_order()  # Initialize with first dialogue + 3 random

    def shuffle_questions(self):
        """Shuffle the order of questions."""
        self.question_order = list(range(len(self.questions)))
        random.shuffle(self.question_order)
        self.current_question = 0  # Reset to start of new order

    def setup_dialogue_order(self):
        """Set up dialogue order: first dialogue, then 3 random from the rest."""
        self.dialogue_order = [0]  # Always start with the first dialogue
        if len(self.dialogues) > 1:
            # Get indices of remaining dialogues (excluding the first)
            remaining_indices = list(range(1, len(self.dialogues)))
            # Randomly select up to 3 indices (or fewer if not enough dialogues)
            selected_indices = random.sample(remaining_indices, min(3, len(remaining_indices)))
            self.dialogue_order.extend(selected_indices)
        self.current_dialogue = 0  # Reset to start of sequence

    def can_interact(self, player):
        # Calculate distance between player and NPC
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        
        return distance <= self.interaction_radius
    
    def get_current_dialogue(self):
        if self.current_dialogue < len(self.dialogue_order):
            dialogue_index = self.dialogue_order[self.current_dialogue]
            return self.dialogues[dialogue_index]
        return None
    
    def advance_dialogue(self):
        self.current_dialogue += 1
        if self.current_dialogue >= len(self.dialogue_order):
            self.setup_dialogue_order()  # Set up new sequence for next cycle
            return True  # Dialogue sequence completed
        return False
    
    def get_current_question(self):
        if self.current_question < len(self.question_order):
            question_index = self.question_order[self.current_question]
            return self.questions[question_index]
        return None
    
    def advance_question(self):
        self.current_question += 3
        if self.current_question >= len(self.question_order):
            self.shuffle_questions()  # Reshuffle questions for the next cycle
            return True  # All questions asked
        return False
        
    def reset_wrong_answers(self):
        self.wrong_answers = 0
        self.shuffle_questions()  # Reshuffle questions when resetting
        self.setup_dialogue_order()  # Reset dialogue sequence

class GusMovement:
    """Class to handle Gus's movement around Niamh with different speeds and patterns."""
    def __init__(self, gus_sprite, niamh_sprite):
        self.gus = gus_sprite
        self.niamh = niamh_sprite
        self.angle = 0
        self.distance = 120  # Base distance from Niamh
        self.speed = 0.01   # Base rotation speed
        self.pattern_timer = 0
        self.current_pattern = 0
        self.pattern_duration = 5000  # 5 seconds per pattern
        self.distance_variation = 0
        self.speed_variation = 0
        
    def update(self):
        # Change pattern every few seconds
        current_time = pygame.time.get_ticks()
        if current_time - self.pattern_timer > self.pattern_duration:
            self.change_pattern()
            self.pattern_timer = current_time
            
        # Update angle based on current speed
        self.angle += self.speed + self.speed_variation
        
        # Calculate new position based on pattern
        current_distance = self.distance + self.distance_variation
        
        # Apply the current pattern
        if self.current_pattern == 0:
            # Circular pattern
            dx = math.cos(self.angle) * current_distance
            dy = math.sin(self.angle) * current_distance
        elif self.current_pattern == 1:
            # Figure-8 pattern
            dx = math.cos(self.angle) * current_distance
            dy = math.sin(self.angle * 2) * current_distance / 2
        elif self.current_pattern == 2:
            # Elliptical pattern
            dx = math.cos(self.angle) * current_distance * 1.5
            dy = math.sin(self.angle) * current_distance * 0.7
        elif self.current_pattern == 3:
            # Bouncy pattern
            dx = math.cos(self.angle) * current_distance
            dy = math.sin(self.angle) * current_distance * (1 + 0.3 * math.sin(self.angle * 5))
        
        # Update Gus's position relative to Niamh
        self.gus.rect.x = self.niamh.rect.x + dx
        self.gus.rect.y = self.niamh.rect.y + dy
        
        # Keep Gus on screen
        if self.gus.rect.left < 0:
            self.gus.rect.left = 0
        if self.gus.rect.right > SCREEN_WIDTH:
            self.gus.rect.right = SCREEN_WIDTH
        if self.gus.rect.top < 0:
            self.gus.rect.top = 0
        if self.gus.rect.bottom > SCREEN_HEIGHT:
            self.gus.rect.bottom = SCREEN_HEIGHT
    
    def change_pattern(self):
        # Randomly select a new pattern
        self.current_pattern = random.randint(0, 3)
        
        # Randomize speed and distance variations
        self.speed_variation = random.uniform(-0.01, 0.03)
        self.distance_variation = random.uniform(-20, 30)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        # No visible image, just a collision rectangle
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Transparent

class DialogueBox:
    def __init__(self, width, height):
        self.rect = pygame.Rect(50, 400, width - 100, 180)  # Fixed height of 180 pixels
        self.font = pygame.font.SysFont(None, 28)
        self.active = False
        self.current_text = ""
        self.current_name = ""
        self.continue_text = "Press SPACE to continue or E to end"
        # Cache for sprite images to avoid reloading
        self.sprite_cache = {}
        
    def set_dialogue(self, text, name):
        self.current_text = text
        self.current_name = name
        self.active = True
        
    def clear(self):
        self.active = False
        self.current_text = ""
        self.current_name = ""
        
    def draw(self, surface):
        if not self.active:
            return
            
        # Draw dialogue box background
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 3)
        
        # Draw NPC sprite instead of name
        if self.current_name:
            # Load sprite image if not cached
            if self.current_name not in self.sprite_cache:
                try:
                    sprite_image = pygame.image.load(f'assets/images/{self.current_name.lower()}.png')
                    # Scale sprite to a smaller size (e.g., 32x32 pixels)
                    sprite_image = pygame.transform.scale(sprite_image, (320, 320))
                    self.sprite_cache[self.current_name] = sprite_image
                except pygame.error:
                    # Fallback to empty surface if sprite not found
                    self.sprite_cache[self.current_name] = pygame.Surface((32, 32), pygame.SRCALPHA)
            
            # Draw sprite above top-left corner
            sprite_image = self.sprite_cache[self.current_name]
            surface.blit(sprite_image, (self.rect.x + 10, self.rect.y - 42))  # Adjusted y to place above box
        
        # Draw text with word wrapping
        words = self.current_text.split(' ')
        x, y = self.rect.x + 10, self.rect.y + 10
        line_height = self.font.get_height()
        max_width = self.rect.width - 20
        
        space_width = self.font.size(' ')[0]
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            test_width = self.font.size(test_line)[0]
            
            if test_width > max_width:
                text_surface = self.font.render(current_line, True, WHITE)
                surface.blit(text_surface, (x, y))
                y += line_height
                current_line = word + " "
            else:
                current_line = test_line
                
        # Render the last line
        if current_line:
            text_surface = self.font.render(current_line, True, WHITE)
            surface.blit(text_surface, (x, y))
            
        # Draw continue prompt
        continue_surface = self.font.render(self.continue_text, True, WHITE)
        surface.blit(continue_surface, (self.rect.right - continue_surface.get_width() - 10, 
                                       self.rect.bottom - continue_surface.get_height() - 10))

class QuestionBox:
    def __init__(self, width, height):
        self.rect = pygame.Rect(50, 400, width - 100, 200)  # Fixed height for question display
        self.font = pygame.font.SysFont(None, 28)
        self.active = False
        self.current_question = ""
        self.current_name = ""
        self.options = []
        self.correct_answers = []
        self.selected_option = None
        self.buttons = []
        self.continue_text = "Press E to end interaction"
        # Cache for sprite images to avoid reloading
        self.sprite_cache = {}
        
    def set_question(self, question, name, options, correct_answers):
        self.current_question = question
        self.current_name = name
        self.options = options
        self.correct_answers = correct_answers
        self.active = True
        self.selected_option = None
        
        # Create buttons for options with dynamic sizing
        self.buttons = []
        padding = 10
        button_spacing = 10
        max_width = (self.rect.width - 20) // len(options)  # Divide available width among options
        start_y = self.rect.bottom + 10
        
        # Calculate button sizes and total width
        button_data = []
        total_width = 0
        for i, option in enumerate(options):
            # Render option text
            option_text = f"{chr(65 + i)}. {option}"
            text_surface = self.font.render(option_text, True, (0, 0, 0))
            
            # Calculate button size based on text
            button_width = min(text_surface.get_width() + padding * 2, max_width *1.5)
            button_height = text_surface.get_height() + padding * 2
            total_width += button_width
            
            button_data.append({
                'width': button_width,
                'height': button_height,
                'text': option_text,
                'text_surface': text_surface,
                'index': i
            })
            
        # Add spacing to total width (except after the last button)
        total_width += button_spacing * (len(options) - 1)
        
        # Calculate starting x to center the buttons
        start_x = self.rect.centerx - total_width // 2
        
        # Assign button positions
        current_x = start_x
        for data in button_data:
            button_rect = pygame.Rect(current_x, start_y, data['width'], data['height'])
            self.buttons.append({
                'rect': button_rect,
                'text': data['text'],
                'text_surface': data['text_surface'],
                'index': data['index']
            })
            current_x += data['width'] + button_spacing
        
    def clear(self):
        self.active = False
        self.current_question = ""
        self.current_name = ""
        self.options = []
        self.correct_answers = []
        self.selected_option = None
        self.buttons = []
        
    def check_click(self, pos):
        if not self.active:
            return None
            
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                self.selected_option = button['index']
                return button['index']
        return None
        
    def is_correct(self):
        if self.selected_option is None:
            return False
        return self.selected_option in self.correct_answers
        
    def draw(self, surface):
        if not self.active:
            return
            
        # Draw question box background
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 3)
        
        # Draw NPC sprite instead of name
        if self.current_name:
            # Load sprite image if not cached
            if self.current_name not in self.sprite_cache:
                try:
                    sprite_image = pygame.image.load(f'assets/images/{self.current_name.lower()}.png')
                    # Scale sprite to a smaller size (e.g., 32x32 pixels)
                    sprite_image = pygame.transform.scale(sprite_image, (320, 320))
                    self.sprite_cache[self.current_name] = sprite_image
                except pygame.error:
                    # Fallback to empty surface if sprite not found
                    self.sprite_cache[self.current_name] = pygame.Surface((32, 32), pygame.SRCALPHA)
            
            # Draw sprite above top-left corner
            sprite_image = self.sprite_cache[self.current_name]
            surface.blit(sprite_image, (self.rect.x + 10, self.rect.y - 42))  # Adjusted y to place above box
        
        # Draw question with word wrapping
        words = self.current_question.split(' ')
        x, y = self.rect.x + 10, self.rect.y + 10
        line_height = self.font.get_height()
        max_width = self.rect.width - 20
        
        space_width = self.font.size(' ')[0]
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            test_width = self.font.size(test_line)[0]
            
            if test_width > max_width:
                text_surface = self.font.render(current_line, True, WHITE)
                surface.blit(text_surface, (x, y))
                y += line_height
                current_line = word + " "
            else:
                current_line = test_line
                
        # Render the last line
        if current_line:
            text_surface = self.font.render(current_line, True, WHITE)
            surface.blit(text_surface, (x, y))
            
        # Draw option buttons styled like speech bubbles
        for button in self.buttons:
            button_rect = button['rect']
            text_surface = button['text_surface']
            padding = 10
            
            # Determine button color
            color = (255, 255, 255)  # White background like speech bubbles
            if self.selected_option == button['index']:
                if button['index'] in self.correct_answers:
                    color = GREEN
                else:
                    color = RED
                    
            # Draw button background (rounded rectangle)
            pygame.draw.rect(surface, color, button_rect, 0, 10)
            pygame.draw.rect(surface, BLACK, button_rect, 2, 10)
            
            # Draw text centered in button
            text_x = button_rect.x + (button_rect.width - text_surface.get_width()) // 2
            text_y = button_rect.y + (button_rect.height - text_surface.get_height()) // 2
            surface.blit(text_surface, (text_x, text_y))
            
            # Draw pointer triangle at the bottom
            pointer_points = [
                (button_rect.centerx, button_rect.bottom),
                (button_rect.centerx - 10, button_rect.bottom - 10),
                (button_rect.centerx + 10, button_rect.bottom - 10)
            ]
            pygame.draw.polygon(surface, color, pointer_points)
            pygame.draw.polygon(surface, BLACK, pointer_points, 2)
            
        # Draw end interaction prompt
        continue_surface = self.font.render(self.continue_text, True, WHITE)
        surface.blit(continue_surface, (self.rect.right - continue_surface.get_width() - 10, 
                                       self.rect.bottom - continue_surface.get_height() - 10))

class EnergyBar:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.border_rect = pygame.Rect(x - 2, y - 2, width + 4, height + 4)
        self.max_energy = 100
        self.current_energy = 100
        self.font = pygame.font.SysFont(None, 24)
        
    def update(self, energy):
        self.current_energy = energy
        
    def draw(self, surface):
        # Draw border
        pygame.draw.rect(surface, BLACK, self.border_rect, 2)
        
        # Calculate energy bar width based on current energy
        energy_width = int((self.current_energy / self.max_energy) * self.rect.width)
        energy_rect = pygame.Rect(self.rect.x, self.rect.y, energy_width, self.rect.height)
        
        # Draw energy bar
        if self.current_energy > 60:
            color = GREEN
        elif self.current_energy > 30:
            color = YELLOW = (255, 255, 0)
        else:
            color = RED
            
        pygame.draw.rect(surface, color, energy_rect)
        
        # Draw energy text
        energy_text = self.font.render(f"Energy: {self.current_energy}%", True, BLACK)
        text_pos = (self.rect.x + 5, self.rect.y - 25)
        surface.blit(energy_text, text_pos)

class SoundManager:
    def __init__(self):
        if not SOUND_ENABLED:
            return
            
        # Load sound effects
        self.interaction_sound = pygame.mixer.Sound('assets/sounds/interaction_sound.mp3')
        self.correct_sound = pygame.mixer.Sound('assets/sounds/correct_sound.mp3')
        self.wrong_sound = pygame.mixer.Sound('assets/sounds/wrong_sound.mp3')
        
        # Set volume levels
        self.interaction_sound.set_volume(0.5)
        self.correct_sound.set_volume(0.7)
        self.wrong_sound.set_volume(0.5)
        
        # Background music
        self.background_music = 'assets/sounds/background_music.mp3'
        
    def play_interaction(self):
        if SOUND_ENABLED:
            self.interaction_sound.play()
        
    def play_correct(self):
        if SOUND_ENABLED:
            self.correct_sound.play()
        
    def play_wrong(self):
        if SOUND_ENABLED:
            self.wrong_sound.play()
        
    def play_background_music(self):
        if SOUND_ENABLED:
            pygame.mixer.music.load(self.background_music)
            pygame.mixer.music.set_volume(0.3)  # Lower volume for background music
            pygame.mixer.music.play(-1)  # Loop indefinitely
        
    def stop_background_music(self):
        if SOUND_ENABLED:
            pygame.mixer.music.stop()

class Game:
    def __init__(self):
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.score = 0
        self.level = 1
        self.correct_answers = 0
        self.required_correct_answers = 5
        self.game_state = "playing"  # playing, dialogue, question, level_complete, game_won
       
        # Create speech bubble system
        self.speech_bubble = SpeechBubble()
       
        # Load assets
        self.load_assets()
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.food_items = pygame.sprite.Group()
        self.signs = pygame.sprite.Group()
        
        # Create player
        self.player = Player(470, 470)
        self.all_sprites.add(self.player)
        
        # Create NPCs
        self.create_npcs()
        
        # Create obstacles (houses, trees, etc.)
        self.create_obstacles()
        
        # Create dialogue and question boxes
        self.dialogue_box = DialogueBox(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.question_box = QuestionBox(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Create energy bar
        self.energy_bar = EnergyBar(SCREEN_WIDTH - 210, 10, 200, 20)
        
        # Current interacting NPC
        self.current_npc = None
        
        # Heart animation for level completion
        self.heart_frames = []
        for i in range(9):
            self.heart_frames.append(pygame.image.load(f'assets/images/heart_{i}.png'))
        self.heart_frame_index = 0
        self.heart_animation_timer = 0
        self.heart_animation_speed = 5  # frames per second
        
        # Sound manager
        self.sound_manager = SoundManager()
        
        # Gus movement handler
        self.gus_movement = None
        self.setup_gus_movement()
        
        # NPC movement handlers
        self.npc_movement_handlers = {}
        
        # Game won animation
        self.game_won = False
        self.game_won_timer = 0
        self.hearts_positions = []
        
        # Apply game modifications
        self.apply_game_modifications()
        
    def apply_game_modifications(self):
        # Add more questions to existing NPCs
        GameModifications.update_npc_questions(self)
        
        # Set up dialogues and questions for new NPCs
        GameModifications.setup_new_npcs(self)
        
        # Create food items
        GameModifications.create_food_items(self)
       
        
        # Set up NPC movement
        GameModifications.setup_npc_movement(self)
        
        
        # Add new game functions
        GameModifications.add_game_functions(self)
        
    def setup_gus_movement(self):
        # Find Niamh and Gus in the NPCs
        niamh_sprite = None
        gus_sprite = None
        
        for npc in self.npcs:
            if npc.name == "Niamh":
                niamh_sprite = npc
            elif npc.name == "Gus":
                gus_sprite = npc
                
        if niamh_sprite and gus_sprite:
            self.gus_movement = GusMovement(gus_sprite, niamh_sprite)
        
    def load_assets(self):
        # Load background
        self.background = pygame.image.load('assets/images/island.png')
        # Scale background to fit new screen size
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Load font
        self.font = pygame.font.SysFont(None, 36)
        
    def create_npcs(self):
        # Create NPCs at different positions on the island
        npc_data = [
            (550, 580, "niamh", "Niamh"),
            (450 + 100, 750, "gus", "Gus"),
            (825, 325, "nikki", "Nikki"),
            (1125, 450, "paul", "Paul"),
            (50, 300, "tony", "Tony"),
            (700, 630, "keelan", "Keelan"),
            (550, 310, "tain", "Tain"),
            (675, 400, "chris", "Chris"),
            (500, 300, "magda", "Magda"),
            (200, 550, "ivan", "Ivan")
        ]
        
        for x, y, sprite_name, name in npc_data:
            npc = NPC(x, y, sprite_name, name)
            self.setup_npc_dialogues(npc)
            self.npcs.add(npc)
            self.all_sprites.add(npc)
    
    def setup_npc_dialogues(self, npc):
        # Set up dialogues and questions for each NPC
        if npc.name == "Niamh":
            npc.dialogues = [
                "Hi there, I'm Niamhy! I love to paint and make stuff, but you already know that",
                "Cadbury should make a Coconut flavored Choclate bar, that would be feckin ?",
                "You (Erik) thinks I'm an expert on herbs, tastefully blending in perfect cooking!",
                "Maybe you'd like meatballs for dinner? Im the best at cooking! ",
                "Did you hear the fecking storm last night",
                "Lets watch Kill Tony! I'm usually in a better mood later in the day.",
                "Gus had such a great poop yesterday!"
            
            ]
            npc.questions = [
                {
                    "question": "Im quite artistic, whats my speciality? ",
                    "options": ["Singing", "Painting", "Kicking", "Biking"],
                    "correct_answers": [1]  # Painting (index 1)
                },
                {
                    "question": "When am I in the best mood?",
                    "options": ["Early morning", "Before breakfast", "Later in the day", "Midnight"],
                    "correct_answers": [2]  # Later in the day (index 2)
                },
                {
                    "question": "What do I make that's the best?",
                    "options": ["Tweets", "Uber Bookings", "Cooking", "Fart sounds"],
                    "correct_answers": [2]  # Cooking (index 2)
                }
            ]
        elif npc.name == "Gus":
            npc.dialogues = [
                "Woof, Woof! I'm Gus (the good boy!)",
                "Wooh, flepp! Niamhy gives the best kisses-ess & belly scrubbies-ess",
                "Woof! Whef, Niamh loves it when I wake her up in the morning!",
                "Pffffsst.. was that a fart?",
                "I had such a great poop yesterday",
                "Woof - I just saw a cat I swear",
                "Im a stinky big boy bobby Gus!",
                "Woof! Niamh’s chicken dinner? Best in my tummy!",
    "Arf arf! Saw a cat on the beach, swear it!",
    "Pffft! That fart means I’m a happy boy!",
    "Woof woof! Belly scrubbies from Niamh, oh yeah!",
    "Grrf! Found a catspot, smells like pooping time!",
    "Woof! Pooped on the beach, Niamh’s so proud!",
    "Arf! Balls are life, chase ‘em all day!",
    "Pffsst! Baths? No way, I’m a stinky Gus!",
    "Woof! Niamh’s kisses make my tail go wild!",
    "Woof woof! Treats? I’m sittin’ already!",
    "Gus the good boy, rollin’ in piss, wooh!",
    "Arf! Early mornin’ with Niamh? Best cuddles!",
    "Woof! Cat ran by, I barked so loud!",
    "Pffft! Smell that? It’s my proudest poop!",
    "Woof woof! Niamh says ‘play,’ I’m ready!",
    "Arf arf! Hate soap, love my stinky fur!",
    "Woof! Dreamin’ of balls and cats, zoom zoom!",
    "Grrf! Niamh’s home! Time to jump high!",
    "Woof! Sniffed a catspot, it’s my treasure!",
    "Pffsst! Farted again, I’m a smelly bob!",
    "Arf! Bringin’ Niamh my ball, let’s go!",
    "Woof woof! Poopin’ right makes me a good boy!",
    "Woof! Cats make me bark, but I’m a good boy!",
    "Arf! Niamh’s treats? I’d sit forev.. few seconds!",
    "Woof! Stinky and proud, that’s Gus bob!"
                
            ]
            npc.questions = [
                {
                    "question": "Woof! What am I usually out looking for?",
                    "options": ["Bones", "Cats", "Toys", "Food"],
                    "correct_answers": [1]  # Cats (index 1)
                },
                {
                    "question": "Woof! Woof! (Who gives the best scratches?)",
                    "options": ["Erik", "Paul", "Niamh", "Tony"],
                    "correct_answers": [2]  # Niamh (index 2)
                },
                {
                    "question": "I run super fast, even when I sleep! What do I catch when I drem?",
                    "options": ["Paul", "Cars", "Balls", "Cats"],
                    "correct_answers": [2, 3]  # A ball (index 2)
                },
                {
                    "question": "When I go down on my front legs, like this, what I want? ",
                    "options": ["Go out", "Play", "Eat ass", "Sleep"],
                    "correct_answers": [1]  # Play (index 2)
                },
                                {
                    "question": "Woof! What I stink like?",
                    "options": ["Coco", "Piss", "Cats", "Baths"],
                    "correct_answers": [1]  # Piss (index 1)
                },            
                {
        "question": "Woof! What’s my favorite thing to chase in the yard?",
        "options": ["Birds", "Balls", "Sticks", "Clouds"],
        "correct_answers": [1]  # Balls
    },
    {
        "question": "Pffft! Who makes my tail wag the most with kisses?",
        "options": ["Tony", "Niamh", "Erik", "Paul"],
        "correct_answers": [1]  # Niamh
    },
    {
        "question": "Woof woof! What do I love to sniff out on my walks?",
        "options": ["Flowers", "Catspots", "Rocks", "Trees"],
        "correct_answers": [1]  # Catspots
    },
    {
        "question": "Arf! What’s the best treat Niamh gives me?",
        "options": ["Carrots", "Bones", "Apples", "Bread"],
        "correct_answers": [1]  # Bones
    },
    {
        "question": "Woof! What do I do when Niamh gets home?",
        "options": ["Sleep", "Bark", "Hide", "Jump"],
        "correct_answers": [3]  # Jump
    },
    {
        "question": "Grrf! Where do I love to get scrubbies?",
        "options": ["Ears", "Back", "Belly", "Paws"],
        "correct_answers": [2]  # Belly
    },
    {
        "question": "Woof! What’s my favorite smell to roll in?",
        "options": ["Grass", "Piss", "Soap", "Mud"],
        "correct_answers": [1]  # Piss
    },
    {
        "question": "Pfft! What do I leave in the yard that makes Niamh proud?",
        "options": ["Toys", "Poop", "Holes", "Sticks"],
        "correct_answers": [1]  # Poop
    },
    {
        "question": "Woof! What do I hate smelling like after Niamh grabs me?",
        "options": ["Treats", "Baths", "Cats", "Dirt"],
        "correct_answers": [1]  # Baths
    },
    {
        "question": "Arf arf! What’s my favorite thing to spot from the Balcony?",
        "options": ["People", "Cars", "Cats", "Birds"],
        "correct_answers": [2]  # Cats
    },
    {
        "question": "Woof! What’s the tastiest thing Niamh cooks for me?",
        "options": ["Soup", "Chicken", "Veggies", "Potato"],
        "correct_answers": [1]  # Chicken Dinner
    },
    {
        "question": "Gus is a good boy! What do I do to prove it?",
        "options": ["Chew shoes", "Sit", "Run away", "Bark"],
        "correct_answers": [1]  # Sit
    },
    {
        "question": "Woof woof! What do I dream of catching besides Treats, Niamh & Balls?",
        "options": ["Treats", "Cats", "Treats", "Niamh"],
        "correct_answers": [1]  # Cats
    },
    {
        "question": "Pffft! What sound do I make when I’m happy?",
        "options": ["Growl", "Whine", "Fart", "Yawn"],
        "correct_answers": [2]  # Fart
    },
    {
        "question": "Woof! What do I do when I see a cat outside?",
        "options": ["Sleep", "Bark", "Hide", "Eat"],
        "correct_answers": [1]  # Bark
    },
    {
        "question": "Arf! What’s my favorite place to poop?",
        "options": ["Couch", "The Beach", "House", "Street"],
        "correct_answers": [1]  # The Beach
    },
    {
        "question": "Woof! What do I love more than a bath?",
        "options": ["Treats", "Soap", "Water", "Shampoo"],
        "correct_answers": [0]  # Treats
    },
    {
        "question": "Grrf! What makes me wiggle all over?",
        "options": ["Rain", "Belly rubs", "Loud noises", "Vacuums"],
        "correct_answers": [1]  # Belly rubs
    },
    {
        "question": "Woof woof! What do I do when Niamh says ‘treat’?",
        "options": ["Run", "Sleep", "Growl", "Sit"],
        "correct_answers": [3]  # Sit
    },
    {
        "question": "Pffft! What smell makes me bark?",
        "options": ["Piss", "Bobbies", "Cats", "Treats"],
        "correct_answers": [1, 2]  # Other Bobbies & Cats
    },
    {
        "question": "Woof! What do I bring to Niamh to play with?",
        "options": ["Shoe", "Ball", "Sock", "Bone"],
        "correct_answers": [1]  # Ball
    },
    {
        "question": "Arf arf! What’s my favorite time with Niamh?",
        "options": ["Bath time", "Walk time", "Sleep time", "Early morning"],
        "correct_answers": [3]  # Early morning in bed.
    },
    {
        "question": "Woof! What do I do if I smell a cat nearby?",
        "options": ["Run home", "Bark", "Hide", "Whine"],
        "correct_answers": [1, 3]  # Bark & Whine
    },
    {
        "question": "Gus here! What’s my proudest moment?",
        "options": ["Pooping right", "Getting wet", "Chewing stuff", "Hiding"],
        "correct_answers": [0]  # Pooping right
    },
    {
        "question": "Woof woof! What makes me the stinkiest good boy?",
        "options": ["Treats", "Baths", "Piss", "Flowers"],
        "correct_answers": [2]  # Piss
    }
                
            ]
        elif npc.name == "Nikki":
            npc.dialogues = [
    "Hi, I'm Nikki! Have you heard the latest?",
    "Everyone's talking about Niamh's amazing paintings!",
    "Did you know she's also great with herbs?",
    "Oh, darling, spill the tea—what’s the latest you’ve heard lately?",
    "I swear, my hands work magic at the massage table, but this paperwork is testing my patience!",
    "Have you seen Tain's new hat? The whole town’s buzzing about it!",
    "Nothing beats a garden party—flowers, chatter, and just a hint of scandal!",
    "I’m drowning in paperwork, but a good gossip keeps my spirits high!",
    "They call me the rapist, but some mishear it as ‘therapist’—can you believe it?",
    "I heard Tony baked a cake that collapsed—oh, the drama in that basement!",
    "A massage from me, and you’ll spill all your secrets—trust me!",
    "I’m planning the next garden party; any ideas for the theme?",
    "These documents won’t file themselves, but I’m smiling through it!",
    "Did you catch wind of Magda’s latest Online order? Bigger than the last one!",
    "My fingers are sore from filing, but they’re still ready for a good knead!",
    "The town’s full of stories—stick with me, and you’ll hear them all!",
    "I’m thinking lavender cocktails for the next garden bash—what do you say?",
    "No matter how many papers pile up, I’ve got gossip to keep me going!"
            ]
            npc.questions = [
    {
        "question": "What is Niamh known for in town?",
        "options": ["Dancing", "Singing", "Painting", "Writing"],
        "correct_answers": [2]  # Painting (index 2)
    },
    {
        "question": "What else is Niamh good at finding?",
        "options": ["Seashells", "Herbs", "Lost items", "Treasure"],
        "correct_answers": [1]  # Herbs (index 1)
    },
    {
        "question": "Who am I in this town?",
        "options": ["The Mayor", "The Gossip", "The Massage", "The Rapist"],
        "correct_answers": [1, 2, 3]  # Anyway..(index 1)
    },
    {
        "question": "What’s the latest thing Tain’s wearing that’s got everyone talking?",
        "options": ["A scarf", "A hat", "Boots", "A cape"],
        "correct_answers": [1]  # Hat (index 1)
    },
    {
        "question": "What do I love to throw in town?",
        "options": ["A dance party", "A book club", "A garden party", "A fishing contest"],
        "correct_answers": [2]  # Garden party (index 2)
    },
    {
        "question": "What have I been buried in lately?",
        "options": ["Gardening", "Documents", "Shit", "Partying"],
        "correct_answers": [1, 2]  # Documents & Shit(index 1)
    },
    {
        "question": "What’s my nickname that some folks get wrong?",
        "options": ["The Baker", "The Rapist", "The Florist", "The Artist"],
        "correct_answers": [1]  # Rapist (misheard for therapist, index 1)
    },
    {
        "question": "What’s Tony’s latest baking mishap?",
        "options": ["Burnt bread", "A collapsed cake", "Salty cookies", "A missing pie"],
        "correct_answers": [1]  # Collapsed cake (index 1)
    },
    {
        "question": "What do I give that’s the best in town?",
        "options": ["Advice", "Massages", "Recipes", "Stories"],
        "correct_answers": [1]  # Massages (index 1)
    },
    {
        "question": "What’s Pauls exaggerating about these days?",
        "options": ["His tires", "Weed prices", "His records", "His shoes"],
        "correct_answers": [1]  # Weed prices (index 1)
    },
    {
        "question": "What do I say my massages make people do?",
        "options": ["Sing", "Sleep", "Spill secrets", "Dance"],
        "correct_answers": [2]  # Spill secrets (index 2)
    },
    {
        "question": "What theme should we have for the garden party?",
        "options": ["The Office", "Brassic", "The Club", "Refugees"],
        "correct_answers": [1]  # Brassic (index 1)
    },
    {
        "question": "What keeps me cheerful despite all the paperwork?",
        "options": ["Gossip", "Music", "Food", "Books"],
        "correct_answers": [0]  # Gossip (index 0)
    },
    {
        "question": "What do I say about my hands at the massage table?",
        "options": ["They’re strong", "They’re magic", "They’re quick", "They’re gentle"],
        "correct_answers": [1]  # Magic (index 1)
    },
    {
        "question": "What’s the town full of, according to me?",
        "options": ["Secrets", "Flowers", "Stories", "Recipes"],
        "correct_answers": [2]  # Stories (index 2)
    },
    {
        "question": "What cocktail flavor did I mention for the party?",
        "options": ["Mint", "Lavender", "Lemon", "Berry"],
        "correct_answers": [1]  # Lavender (index 1)
    },
    {
        "question": "What’s sore from all my filing documents and giving the rapist massages?",
        "options": ["My neck", "My back", "My fingers", "My Crack"],
        "correct_answers": [2]  # My Fingers (index 1)
    },
    {
        "question": "What do I want to hear from you?",
        "options": ["Your plans", "Your gossip", "Your recipes", "Your dreams"],
        "correct_answers": [1]  # Gossip (index 1)
    }
            ]
        elif npc.name == "Paul":
            npc.dialogues = [
    "Hello there, I'm Paul. Have you seen the prices lately?",
    "It's outrageous! I dont know what to do..",
    "I guess I'll have to get to the Airport early..",
    "Well, everythings calm and quiet now",
    "I was there, I saw it myself",
    "Now where did I park the car..?",
    "These herb prices are bleeding me dry, I tell you!",
    "Was it me who parked the car, or did someone move it?",
    "I’ve got to be at the airport—yesterday, tomorrow, always!",
    "I swear, my car’s playing hide-and-seek with me!",
    "Who sets these herb prices? It’s highway robbery!",
    "I’m rushing to the airport, but where’s my blasted car?",
    "Calm? Quiet? Not with these prices climbing!",
    "Did I leave my car at the terminal last week?",
    "Herbs shouldn’t cost more than a plane ticket!",
    "I need to catch a flight, but my car’s gone AWOL!",
    "I checked the market—herb prices are still absurd!",
    "Did I park near the airport, or am I losing it?",
    "Tomorrow’s another airport dash—wish me luck!",
    "These prices make me want to grow my own herbs!",
    "I’d be fine if I could just find my darn car!"
            ]
            npc.questions = [
{
        "question": "Whats bothering me the most? ..Its really concerning to say the least..",
        "options": ["Weather", "Herb Prices", "Dogs", "Fishing"],
        "correct_answers": [1]  # Herb Prices (index 1)
    },
    {
        "question": "Where the fuck did I park me car just now?",
        "options": ["Me, I did it.", "At home", "Over there", "Just here"],
        "correct_answers": [1]  # At home (index 1)
    },
    {
        "question": "When do I have to be at the Airport? ",
        "options": ["Today", "12pm", "5am", "Tomorrow"],
        "correct_answers": [0, 1, 2, 3]  # All are correct
    },
    {
        "question": "What’s got me ready to pull my hair out?",
        "options": ["Flight delays", "Herb prices", "Lost luggage", "Traffic"],
        "correct_answers": [1]  # Herb prices (index 1)
    },
    {
        "question": "Who might’ve parked my car last?",
        "options": ["Me", "A friend", "Nobody", "I don’t know"],
        "correct_answers": [3]  # I don’t know (index 3)
    },
    {
        "question": "Why am I always rushing to the airport?",
        "options": ["Vacation", "Business", "I don’t know", "Emergencies"],
        "correct_answers": [2]  # I don’t know (index 2)
    },
    {
        "question": "What’s more expensive than it should be?",
        "options": ["Herbs", "Gas", "Tickets", "Coffee"],
        "correct_answers": [0]  # Herbs (index 0)
    },
    {
        "question": "Where did I last think I left my car?",
        "options": ["The market", "The airport", "My driveway", "I forgot"],
        "correct_answers": [3]  # I forgot (index 3)
    },
    {
        "question": "What’s my biggest worry besides my car?",
        "options": ["Missing flights", "Herb prices", "Weather", "Time"],
        "correct_answers": [1]  # Herb prices (index 1)
    },
    {
        "question": "When did I last deal with the airport?",
        "options": ["Yesterday", "Last week", "Tomorrow", "All of them"],
        "correct_answers": [3]  # All of them (index 3)
    },
    {
        "question": "What do I say my car’s doing to me?",
        "options": ["Breaking down", "Hiding", "Speeding", "Stalling"],
        "correct_answers": [1]  # Hiding (index 1)
    },
    {
        "question": "What do I compare herb prices to?",
        "options": ["Gold", "Plane tickets", "Water", "Bread"],
        "correct_answers": [1]  # Plane tickets (index 1)
    },
    {
        "question": "What’s my state of mind about my car?",
        "options": ["Confident", "Confused", "Relaxed", "Angry"],
        "correct_answers": [1]  # Confused (index 1)
    },
    {
        "question": "What do I want to do because of herb prices?",
        "options": ["Quit", "Protest", "Grow my own", "Move"],
        "correct_answers": [2]  # Grow my own (index 2)
    },
    {
        "question": "Where do I wonder if my car’s parked?",
        "options": ["The terminal", "Downtown", "My garage", "The shop"],
        "correct_answers": [0]  # The terminal (index 0)
    },
    {
        "question": "What’s never calm for me?",
        "options": ["The weather", "My schedule", "Herb prices", "The airport"],
        "correct_answers": [2]  # Herb prices (index 2)
    },
    {
        "question": "What am I always losing track of?",
        "options": ["My keys", "My car", "My phone", "My wallet"],
        "correct_answers": [1]  # My car (index 1)
    },
    {
        "question": "What do I call the herb prices?",
        "options": ["Fair", "Robbery", "Bargain", "Stable"],
        "correct_answers": [1]  # Robbery (index 1)
    }

            ]
        elif npc.name == "Tony":
            npc.dialogues = [
                "Hey Mate, I'm Tony. I'm trying to make some cookies,",
                "And get real baked mate, bake a cake mate..",
                "Niamh makes the best cooking and baking, dough..",
                "Maaan... Mate.",
                "I wonder what her secret is for such incredicle cooking.",
                "Man Im so high right now I dont even know what Im saying..",
                "You should come over sometime, I have cookie.",
                "911 man, it was an inside job mate!",
                "911, b7.. a7 but thats the FATHER"
            ]
            npc.questions = [
                {
                    "question": "What was I talking about again?",
                    "options": ["Cookie", "Pitu", "Cake, Mate", "Melon"],
                    "correct_answers": [2]  # Cake, Mate (index 2)
                },
                {
                    "question": "What does Niamh make that's the best?",
                    "options": ["Clothes", "Cooking", "Music", "Drw"],
                    "correct_answers": [1, 3]  # Cooking & Art (index 1)
                },
                {
                    "question": "Now, look here mate. Im baked as a cake. Wheres Pitu, can you spot her?",
                    "options": ["Home", "In the car", "Arroyo", "Down There."],
                    "correct_answers": [3]  # Down there (index 1)
                }
            ]
        elif npc.name == "Keelan":
            npc.dialogues = [
                "Greetings, I'm Keelan. I mumbleriddles and you know.. ",
                "Pizza... goes well with herbs.",
                "Herbs, so cool when you think about it.",
                "Did you know the Ovenstoven Mega 2000 can bake whole family at once?",
                "The recordholder in baking most Pizzas doesnt hold any pizza right now dough...",
                "Some herbs are better than other, oh yes.",
                "Thats what I think",
                "I'm a big fan of the Gabagool!"
                "*Mumble* Píotsa’s art, aye, herbs make it heart.",
                "Vintage cars, so grand… wish I had one to hand.",
                "Gabagool on my pizza? *Mumble* That’s the dream, so.",
                "Niamh’s fast, but I’ll race her ‘til the last!",
                "Riddle me this: what’s cheesy and never amiss?",
                "Ovenstoven Mega 2000, *mumble*, cooks pizza like a poem.",
    "Basil’s the king, makes my heart sing.",
    "Fashion’s my game, vintage style, no shame.",
    "Ever hear a car purr? Like pizza dough, it stirs!",
    "*Mumble mumble* Salami’s fine, but gabagool’s divine.",
    "Pizza records? I’d bake ‘til the world shakes.",
    "Humble’s the way, but my pizza saves the day.",
    "Niamh brews tea with herbs, *mumble*, calms my words.",
    "Old cars, chrome shine… wish one was mine.",
    "Riddle: what’s round, tasty, and never hasty?",
    "*Mumble* Thyme on pizza? Oh, it’s sublime.",
    "My scarf’s vintage, aye, makes folks sigh.",
    "Pizza’s my muse, with herbs I can’t lose.",
    "Racing’s fun, but Niamh’s tough, *mumble*, run!",
    "Gabagool’s the star, on pizza, it goes far.",
    "Ever see a car race? Like pizza, sets the pace.",
    "*Mumble* Sage is wise, lifts pizza to the skies.",
    "Style’s not loud, but I’m quietly proud.",
    "Pizza facts, so cool… like ovens, they rule.",
    "Aye, *mumble*, life’s a riddle, pizza’s the middle."
               
            ]
            npc.questions = [
                {
                    "question": "Riddle: I am green and aromatic, used in mental acrobatics. Or just as Pizza topping.. Niamh finds me easily. What herb am I?",
                    "options": ["Basil", "OG Kush", "Gelato", "Thyme"],
                    "correct_answers": [0, 1, 2, 3]  # All are correct
                },
                {
                    "question": "Riddle: I help you sleep at night, with a calming scent. Niamh brews me into tea. What herb am I?",
                    "options": ["Chamomile", "Lavender", "Valerian", "All of these"],
                    "correct_answers": [3]  # All of these (index 3)
                },
                {
                    "question": "Riddle: I am the king of herbs, I even look like a crown. What herb am I?",
                    "options": ["Basil", "Rosemary", "Sage", "Thyme"],
                    "correct_answers": [0]  # Basil (index 0)
                },
                {
        "question": "Riddle, *mumble*: I’m a pizza topping, meaty and fine, loved by Keelan, pairs with wine. What am I?",
        "options": ["Pepperoni", "Gabagool", "Sausage", "Ham"],
        "correct_answers": [1]  # Gabagool
    },
    {
        "question": "Oi, riddle this: I’m a car from olden days, Keelan’s dream with retro blaze. What type am I?",
        "options": ["Ford Mustang", "Toyota Corolla", "Honda Civic", "Tesla Roadster"],
        "correct_answers": [0]  # Ford Mustang
    },
    {
        "question": "*Mumble mumble*, riddle: I’m a herb on pizza, sharp and green, Niamh and I agree, it’s supreme. What am I?",
        "options": ["Oregano", "Cilantro", "Mint", "Dill"],
        "correct_answers": [0]  # Oregano
    },
    {
        "question": "Riddle, so: I’m a race Keelan loves, not with cars but with Niamh’s gloves. Where do we dash?",
        "options": ["Kitchen", "Garden", "Street", "Track"],
        "correct_answers": [2]  # Street
    },
    {
        "question": "Fact, *mumble*: Keelan’s pizza oven gets hot, aye. How hot can the Ovenstoven Mega 2000 go?",
        "options": ["300°C", "400°C", "500°C", "600°C"],
        "correct_answers": [2]  # 500°C
    },
    {
        "question": "Riddle: I’m a salami so fine, Keelan’s choice for a pizza divine. What’s my name?",
        "options": ["Prosciutto", "Chorizo", "Soppressata", "Gabagool"],
        "correct_answers": [3]  # Gabagool
    },
    {
        "question": "*Mumble* riddle: I’m a fashion piece Keelan wears, stylish and cool, shows he cares. What am I?",
        "options": ["Sneakers", "Scarf", "Jacket", "Hat"],
        "correct_answers": [2]  # Jacket
    },
    {
        "question": "Riddle, aye: I’m a pizza Keelan makes, cheesy and grand, best in the land. What’s it called?",
        "options": ["Margherita", "Pepperoni", "Gabagool Supreme", "Veggie"],
        "correct_answers": [2]  # Gabagool Supreme
    },
    {
        "question": "Fact: Keelan mumbles in Irish. What’s a word he might say for ‘pizza’?",
        "options": ["Píotsa", "Cáca", "Arán", "Bia"],
        "correct_answers": [0]  # Píotsa
    },
    {
        "question": "Riddle: I’m a vintage car part Keelan loves, shiny and round, makes hearts throb. What am I?",
        "options": ["Steering wheel", "Hubcap", "Headlight", "Mirror"],
        "correct_answers": [1]  # Hubcap
    },
    {
        "question": "*Mumble mumble*: I’m a herb Keelan uses, woody and strong, pizza’s not wrong. What am I?",
        "options": ["Thyme", "Parsley", "Chives", "Tarragon"],
        "correct_answers": [0]  # Thyme
    },
    {
        "question": "Riddle: Keelan’s humble, but his pizza’s a hit. How many can he bake in one sit?",
        "options": ["One", "Two", "Three", "Four"],
        "correct_answers": [3]  # Four
    },
    {
        "question": "Fact, so: Keelan races Niamh. Who usually wins, *mumble*?",
        "options": ["Keelan", "Niamh", "Tie", "Nobody"],
        "correct_answers": [1, 2]  # Tie (or Niamh)
    },
    {
        "question": "Riddle: I’m a topping Keelan adores, spicy and bold, never ignored. What am I?",
        "options": ["Olives", "Jalapeños", "Mushrooms", "Onions"],
        "correct_answers": [1]  # Jalapeños
    },
    {
        "question": "*Mumble* riddle: I’m a style Keelan rocks, not too loud, makes him proud. What’s it called?",
        "options": ["Grunge", "Vintage", "Sporty", "Formal"],
        "correct_answers": [1]  # Vintage
    },
    {
        "question": "Riddle: I’m a pizza tool Keelan needs, spins the dough with ease. What am I?",
        "options": ["Spatula", "Pizza peel", "Rolling pin", "Knife"],
        "correct_answers": [1]  # Pizza peel
    },
    {
        "question": "Fact: Keelan loves gabagool. What’s it made from, *mumble*?",
        "options": ["Beef", "Pork", "Chicken", "Turkey"],
        "correct_answers": [1]  # Pork
    },
    {
        "question": "Riddle: I’m a car Keelan dreams of, fast and old, worth more than gold. What am I?",
        "options": ["Chevy Camaro", "Ford Focus", "Kia Rio", "Nissan Leaf"],
        "correct_answers": [0]  # Chevy Camaro
    },
    {
        "question": "*Mumble mumble* riddle: I’m a herb for pizza, soft and wise, Keelan’s choice for tasty skies. What am I?",
        "options": ["Sage", "Basil", "Mint", "Coriander"],
        "correct_answers": [0]  # Sage
    },
    {
        "question": "Riddle: Keelan’s humble, but his fashion’s grand. What’s his favorite clothing brand?",
        "options": ["Gucci", "Volcom", "Nike", "Chino"],
        "correct_answers": [1]  # Volcom
    },
    {
        "question": "Fact: Keelan’s pizza record, *mumble*. How many pizzas in an hour, best guess?",
        "options": ["5", "10", "15", "20"],
        "correct_answers": [2]  # 15
    },
    {
        "question": "Riddle: I’m a race Keelan loves, vintage cars, under stars. What’s it called?",
        "options": ["Daytona", "Le Mans", "Monaco", "Indy"],
        "correct_answers": [1]  # Le Mans
    },
    {
        "question": "*Mumble* riddle: I’m a pizza Keelan crafts, simple yet neat, herb and meat. What’s it called?",
        "options": ["Four Cheese", "Basil Gabagool", "Veggie Deluxe", "Meat Feast"],
        "correct_answers": [1]  # Basil Gabagool
    },
    {
        "question": "Riddle: I’m a fact Keelan shares, about pizza, shows he cares. What’s the oldest pizza topping?",
        "options": ["Cheese", "Tomato", "Herbs", "Meat"],
        "correct_answers": [0]  # Cheese
    },
    {
        "question": "Riddle, *mumble*: I’m Keelan’s vibe, quiet and true, helps pizza shine, fashion too. What am I?",
        "options": ["Pride", "Humility", "Confidence", "Humor"],
        "correct_answers": [1]  # Humility
    }

            ]
        # New NPCs will have their dialogues and questions set in GameModifications.setup_new_npcs()
    
    def create_obstacles(self):
        # Create obstacles for houses - adjusted for larger screen
        house_data = [


        ]
        
        for x, y, width, height in house_data:
            obstacle = Obstacle(x, y, width, height)
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)
        
        # Create obstacles for trees - adjusted for larger screen
        tree_positions = [
            (25, 650),
            (50, 650),
            (75, 650),
            (100, 650),
            (125, 650),
            (150, 650),
            (175, 650),
            (200, 650),
            (225, 650),
            (250, 650),
            (275, 650),
            (300, 650),
            (325, 650),
            (350, 650),
            (375, 650),
            (400, 680),
            (425, 680),
            (450, 680),
            (475, 850),
            (500, 850),
            (525, 850),
            (550, 850),
            (575, 850),
            (600, 850),
            (625, 850),
            (650, 850),
            (675, 850),
            (700, 850),
            (725, 850),
            (750, 680),
            (775, 680),
            (800, 680),
            (825, 680),
            (850, 680),
            (875, 680),
            (900, 680),
            (925, 680),
            (950, 680),
            (975, 680),
        ]
        
        for x, y in tree_positions:
            obstacle = Obstacle(x - 10, y, 20, 20)  # Tree trunk area
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)
    
    def run(self):
        # Start background music
        self.sound_manager.play_background_music()
        
        # Main game loop
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
            
    def handle_events(self):
        # Process input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if self.game_state == "playing":
                        # Check for NPC interactions when space is pressed
                        self.check_npc_interactions()
                    elif self.game_state == "dialogue":
                        # Advance dialogue
                        if self.current_npc:
                            dialogue_completed = self.current_npc.advance_dialogue()
                            if dialogue_completed:
                                # Move to question
                                self.start_question()
                            else:
                                # Update dialogue text
                                dialogue = self.current_npc.get_current_dialogue()
                                if dialogue:
                                    self.dialogue_box.set_dialogue(dialogue, self.current_npc.name)
                                    self.sound_manager.play_interaction()
                    elif self.game_state == "level_complete":
                        # Return to playing state after level completion
                        self.game_state = "playing"
                        self.dialogue_box.clear()
                        self.question_box.clear()
                    elif self.game_state == "game_won":
                        # Return to playing state after game won
                        self.game_state = "playing"
                        self.game_won = False
                elif event.key == pygame.K_e:
                    # End interaction when E is pressed
                    if self.game_state == "dialogue" or self.game_state == "question":
                        self.game_state = "playing"
                        self.dialogue_box.clear()
                        self.question_box.clear()
                        if self.current_npc:
                            self.current_npc.reset_wrong_answers()
                        self.current_npc = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.game_state == "question":
                        # Check if an answer option was clicked
                        option_index = self.question_box.check_click(event.pos)
                        if option_index is not None:
                            # Check if answer is correct
                            if self.question_box.is_correct():
                                self.sound_manager.play_correct()
                                self.correct_answers += 1
                                self.score += 100
                                
                                # Reset wrong answer counter
                                if self.current_npc:
                                    self.current_npc.reset_wrong_answers()
                                
                                # Check if level is complete
                                if self.correct_answers >= self.required_correct_answers:
                                    self.level_complete()
                                else:
                                    # Move to next question or back to playing
                                    pygame.time.delay(2000)  # Show correct/wrong color briefly
                                    self.current_npc.advance_question()
                                    question_data = self.current_npc.get_current_question()
                                    if question_data:
                                        self.question_box.set_question(
                                            question_data["question"],
                                            self.current_npc.name,
                                            question_data["options"],
                                            question_data["correct_answers"]
                                        )
                                    else:
                                        self.game_state = "playing"
                                        self.dialogue_box.clear()
                                        self.question_box.clear()
                                        self.current_npc = None
                            else:
                                # Wrong answer, reduce energy and increment wrong answer counter
                                self.sound_manager.play_wrong()
                                # Reduce energy by 20%
                                self.player.reduce_energy(20)
                                
                                # Increment wrong answer counter
                                if self.current_npc:
                                    self.current_npc.wrong_answers += 1
                                    
                                    # End interaction after 2 wrong answers
                                    if self.current_npc.wrong_answers >= 2:
                                        pygame.time.delay(1000)  # Show correct/wrong color briefly
                                        self.game_state = "playing"
                                        self.dialogue_box.clear()
                                        self.question_box.clear()
                                        self.current_npc.reset_wrong_answers()
                                        self.current_npc = None
                                        continue
                                
                                pygame.time.delay(1000)  # Show correct/wrong color briefly
                                
                                # If energy is depleted, reset level
                                if self.player.energy <= 0:
                                    self.reset_level()
                                else:
                                    # Continue with next question
                                    self.current_npc.advance_question()
                                    question_data = self.current_npc.get_current_question()
                                    if question_data:
                                        self.question_box.set_question(
                                            question_data["question"],
                                            self.current_npc.name,
                                            question_data["options"],
                                            question_data["correct_answers"]
                                        )
                                    else:
                                        self.game_state = "playing"
                                        self.dialogue_box.clear()
                                        self.question_box.clear()
                                        self.current_npc = None
                    
    def check_npc_interactions(self):
        # Check if player is close enough to interact with any NPC
        for npc in self.npcs:
            if npc.can_interact(self.player):
                self.current_npc = npc
                self.game_state = "dialogue"
                
                # Reset wrong answer counter
                npc.reset_wrong_answers()
                
                # Play interaction sound
                self.sound_manager.play_interaction()
                
                # Start dialogue
                dialogue = npc.get_current_dialogue()
                if dialogue:
                    self.dialogue_box.set_dialogue(dialogue, npc.name)
                break
    
    def check_food_interactions(self):
        # Check if player collides with any food items
        food_collisions = pygame.sprite.spritecollide(self.player, self.food_items, True)
        for food in food_collisions:
            # Add energy
            self.player.add_energy(food.energy_value)
            # Play sound
            self.sound_manager.play_correct()
                
    def start_question(self):
        # Start question mode
        self.game_state = "question"
        self.dialogue_box.clear()
        
        # Get question data
        question_data = self.current_npc.get_current_question()
        if question_data:
            self.question_box.set_question(
                question_data["question"],
                self.current_npc.name,
                question_data["options"],
                question_data["correct_answers"]
            )
        else:
            # No questions, return to playing
            self.game_state = "playing"
            self.current_npc = None
    
    def level_complete(self):
        # Level complete
        self.game_state = "level_complete"
        self.dialogue_box.clear()
        self.question_box.clear()
        
        # Play success sound
        self.sound_manager.play_correct()
        
        # Reset for next level
        self.level += 1
        self.correct_answers = 0
        
        # Restore energy
        self.player.energy = 100
        
        # Start heart animation
        self.heart_frame_index = 0
        self.heart_animation_timer = pygame.time.get_ticks()
        
        # Check if game is won (level 5 completed)
        if self.level > 5:
            self.game_won = True
            self.game_state = "game_won"
            self.game_won_timer = pygame.time.get_ticks()
            
            # Initialize heart positions for animation
            self.hearts_positions = []
            for _ in range(20):
                self.hearts_positions.append([
                    random.randint(0, self.screen.get_width()),
                    random.randint(-500, 0),
                    random.randint(1, 3)  # Speed
                ])
    
    def reset_level(self):
        # Reset level on wrong answer
        self.game_state = "playing"
        self.dialogue_box.clear()
        self.question_box.clear()
        self.current_npc = None
        self.correct_answers = 0
        
        # Restore energy
        self.player.energy = 100
                
    def update(self):
        # Update game state
        if self.game_state == "playing":
            # Get pressed keys
            keys = pygame.key.get_pressed()
            
            # Update player with key input and obstacles
            self.player.update(keys, self.obstacles)
            
            # Check for food interactions
            self.check_food_interactions()
            
            # Update Gus's movement around Niamh if available
            if self.gus_movement:
                self.gus_movement.update()
            
            # Update speech bubbles
            self.speech_bubble.update(self.clock.get_time(), self.npcs)  
            
            # Update NPC movements
            for handler in self.npc_movement_handlers.values():
                handler.update()
                
        elif self.game_state == "level_complete":
            # Update heart animation
            current_time = pygame.time.get_ticks()
            if current_time - self.heart_animation_timer > 1000 / self.heart_animation_speed:
                self.heart_frame_index = (self.heart_frame_index + 1) % len(self.heart_frames)
                self.heart_animation_timer = current_time
                
                # End animation after 3 seconds
                if current_time - self.heart_animation_timer > 5000:
                    self.game_state = "playing"
        
        elif self.game_state == "game_won":
            # Update game won animation
            current_time = pygame.time.get_ticks()
            
            # Move Erik to Niamh
            niamh_sprite = None
            for npc in self.npcs:
                if npc.name == "Niamh":
                    niamh_sprite = npc
                    break
                    
            if niamh_sprite:
                # Calculate direction to Niamh
                dx = niamh_sprite.rect.centerx - self.player.rect.centerx
                dy = niamh_sprite.rect.centery - self.player.rect.centery
                distance = math.sqrt(dx * dx + dy * dy)
                
                # Move Erik toward Niamh if not already there
                if distance > 10:
                    speed = min(5, distance)
                    if distance > 0:
                        self.player.rect.x += dx * speed / distance
                        self.player.rect.y += dy * speed / distance
                
            # Update falling hearts
            for heart in self.hearts_positions:
                heart[1] += heart[2]  # Move down based on speed
                if heart[1] > self.screen.get_height():
                    # Reset heart to top when it goes off screen
                    heart[1] = random.randint(-100, 0)
                    heart[0] = random.randint(0, self.screen.get_width())
            
            # End animation after 3 seconds
            if current_time - self.game_won_timer > 3000:
                self.game_state = "playing"
                self.game_won = False
        
        # Update energy bar
        self.energy_bar.update(self.player.energy)
        
    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw all sprites
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect)
        
        # Draw sign text
        for sign in self.signs:
            sign.draw_text(self.screen)
        
        # Draw score and level
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (10, 50))
        
        correct_text = self.font.render(f"Correct Answers: {self.correct_answers}/{self.required_correct_answers}", True, WHITE)
        self.screen.blit(correct_text, (10, 90))
        
        # Draw energy bar
        self.energy_bar.draw(self.screen)
        
        # Draw speech bubbles
        self.speech_bubble.draw(self.screen, self.npcs)
        
        # Draw sound status
        sound_status = "Sound: ON" if SOUND_ENABLED else "Sound: OFF"
        sound_text = self.font.render(sound_status, True, BLACK)
        self.screen.blit(sound_text, (SCREEN_WIDTH - sound_text.get_width() - 10, 50))
        
        # Draw dialogue box if active
        if self.game_state == "dialogue":
            self.dialogue_box.draw(self.screen)
        
        # Draw question box if active
        if self.game_state == "question":
            self.question_box.draw(self.screen)
            
        # Draw heart animation if level complete
        if self.game_state == "level_complete":
            heart_image = self.heart_frames[self.heart_frame_index]
            heart_rect = heart_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(heart_image, heart_rect)
            
            # Draw completion message
            complete_text = self.font.render("Level Complete!", True, WHITE)
            complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(complete_text, complete_rect)
            
            continue_text = self.font.render("Press SPACE to continue", True, WHITE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(continue_text, continue_rect)
            
        # Draw game won animation
        if self.game_state == "game_won":
            # Draw falling hearts
            for heart_pos in self.hearts_positions:
                self.screen.blit(self.heart_img, (heart_pos[0], heart_pos[1]))
            
            # Draw game won message
            won_text = self.font.render("Game Won: Erik & Niamh Kiss!", True, RED)
            won_rect = won_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(won_text, won_rect)
            
            continue_text = self.font.render("Press SPACE to continue", True, WHITE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(continue_text, continue_rect)
        
        pygame.display.flip()
        
    def quit(self):
        # Stop music before quitting
        self.sound_manager.stop_background_music()
        pygame.quit()
        sys.exit()

# Main function to run the game
def main():
    game = Game()
    try:
        game.run()
    finally:
        game.quit()

if __name__ == "__main__":
    main()
