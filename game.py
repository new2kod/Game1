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
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
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
PLAYER_SPEED = 3

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
        
    def can_interact(self, player):
        # Calculate distance between player and NPC
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        
        return distance <= self.interaction_radius
    
    def get_current_dialogue(self):
        if self.current_dialogue < len(self.dialogues):
            return self.dialogues[self.current_dialogue]
        return None
    
    def advance_dialogue(self):
        self.current_dialogue += 1
        if self.current_dialogue >= len(self.dialogues):
            self.current_dialogue = 0
            return True  # Dialogue completed
        return False
    
    def get_current_question(self):
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None
    
    def advance_question(self):
        self.current_question += 1
        if self.current_question >= len(self.questions):
            self.current_question = 0
            return True  # All questions asked
        return False
        
    def reset_wrong_answers(self):
        self.wrong_answers = 0

class GusMovement:
    """Class to handle Gus's movement around Niamh with different speeds and patterns."""
    def __init__(self, gus_sprite, niamh_sprite):
        self.gus = gus_sprite
        self.niamh = niamh_sprite
        self.angle = 0
        self.distance = 80  # Base distance from Niamh
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
        self.name_font = pygame.font.SysFont(None, 32)
        self.active = False
        self.current_text = ""
        self.current_name = ""
        self.continue_text = "Press SPACE to continue or E to end"
        
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
        
        # Draw name
        name_surface = self.name_font.render(self.current_name, True, BLACK)
        surface.blit(name_surface, (self.rect.x + 10, self.rect.y - 30))
        
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
                text_surface = self.font.render(current_line, True, BLACK)
                surface.blit(text_surface, (x, y))
                y += line_height
                current_line = word + " "
            else:
                current_line = test_line
                
        # Render the last line
        if current_line:
            text_surface = self.font.render(current_line, True, BLACK)
            surface.blit(text_surface, (x, y))
            
        # Draw continue prompt
        continue_surface = self.font.render(self.continue_text, True, BLACK)
        surface.blit(continue_surface, (self.rect.right - continue_surface.get_width() - 10, 
                                       self.rect.bottom - continue_surface.get_height() - 10))

class QuestionBox:
    def __init__(self, width, height):
        self.rect = pygame.Rect(50, 400, width - 100, 200)  # Fixed height of 200 pixels
        self.font = pygame.font.SysFont(None, 28)
        self.name_font = pygame.font.SysFont(None, 32)
        self.active = False
        self.current_question = ""
        self.current_name = ""
        self.options = []
        self.correct_answers = []
        self.selected_option = None
        self.buttons = []
        self.continue_text = "Press E to end interaction"
        
    def set_question(self, question, name, options, correct_answers):
        self.current_question = question
        self.current_name = name
        self.options = options
        self.correct_answers = correct_answers
        self.active = True
        self.selected_option = None
        
        # Create buttons for options
        self.buttons = []
        button_width = 200
        button_height = 40
        button_spacing = 20
        total_width = (button_width * 2) + button_spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        for i, option in enumerate(options):
            row = i // 2
            col = i % 2
            x = start_x + (col * (button_width + button_spacing))
            y = self.rect.bottom + 10 + (row * (button_height + 5))
            
            self.buttons.append({
                'rect': pygame.Rect(x, y, button_width, button_height),
                'text': option,
                'index': i
            })
        
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
        pygame.draw.rect(surface, BLACK, self.rect, 3)
        
        # Draw name
        name_surface = self.name_font.render(self.current_name, True, BLACK)
        surface.blit(name_surface, (self.rect.x + 10, self.rect.y - 30))
        
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
                text_surface = self.font.render(current_line, True, BLACK)
                surface.blit(text_surface, (x, y))
                y += line_height
                current_line = word + " "
            else:
                current_line = test_line
                
        # Render the last line
        if current_line:
            text_surface = self.font.render(current_line, True, BLACK)
            surface.blit(text_surface, (x, y))
            
        # Draw option buttons
        for button in self.buttons:
            color = GRAY
            if self.selected_option == button['index']:
                if button['index'] in self.correct_answers:
                    color = GREEN
                else:
                    color = RED
                    
            pygame.draw.rect(surface, color, button['rect'])
            pygame.draw.rect(surface, BLACK, button['rect'], 2)
            
            option_text = f"{chr(65 + button['index'])}. {button['text']}"
            text_surface = self.font.render(option_text, True, BLACK)
            text_rect = text_surface.get_rect(center=button['rect'].center)
            surface.blit(text_surface, text_rect)
            
        # Draw end interaction prompt
        continue_surface = self.font.render(self.continue_text, True, BLACK)
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
        self.correct_sound.set_volume(0.4)
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
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
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
        
        # Create direction signs
        GameModifications.create_direction_signs(self)
        
        # Set up NPC movement
        GameModifications.setup_npc_movement(self)
        
        # Update NPC positions - place Niamh in the middle
        GameModifications.update_npc_positions(self)
        
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
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "niamh", "Niamh"),
            (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2, "gus", "Gus"),
            (700, 300, "nikki", "Nikki"),
            (950, 450, "paul", "Paul"),
            (75, 300, "tony", "Tony"),
            (750, 650, "keelan", "Keelan"),
            (500, 250, "tain", "Tain"),
            (600, 500, "chris", "Chris"),
            (400, 300, "magda", "Magda")
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
                "HI there, I'm Niamhy! Im a real good painter, and I grow wee..",
                "..I mean, herbs.. ",
                "I also enjoy cooking. Maybe you'd like meatballs for dinner?",
                "I'm usually in a better mood later in the day.",
                "Lets watch en apisode of Kill Tony and I might kiss you later!"
            ]
            npc.questions = [
                {
                    "question": "What's my favorite aout of these? ",
                    "options": ["Singing", "Painting", "Dancing", "Biking"],
                    "correct_answers": [1]  # Painting (index 1)
                },
                {
                    "question": "When am I in the best mood?",
                    "options": ["Early morning", "Before breakfast", "Later in the day", "Midnight"],
                    "correct_answers": [2]  # Later in the day (index 2)
                },
                {
                    "question": "What do I make that's the best?",
                    "options": ["Tweets", "Uber Bookings", "Cooking", "Farts"],
                    "correct_answers": [2]  # Cooking (index 2)
                }
            ]
        elif npc.name == "Gus":
            npc.dialogues = [
                "Woof, Woof! I'm Gus (the good boy!)",
                "Wooh, flepp! Niamhy gives the best kiffesss & belly scrubbies",
                "Woof! Whef, Niamh loves it when I wake her up in the morning!",
            ]
            npc.questions = [
                {
                    "question": "Woof! What am I out looking for?",
                    "options": ["Bones", "Cats", "Toys", "Food"],
                    "correct_answers": [1]  # Cats (index 1)
                },
                {
                    "question": "Woof! Woof! (Who gives the best scratches?)",
                    "options": ["Erik", "Paul", "Niamh", "Tony"],
                    "correct_answers": [2]  # Niamh (index 2)
                },
                {
                    "question": "Woof! (What do I want right now?)",
                    "options": ["A walk", "A nap", "A ball", "To play"],
                    "correct_answers": [2]  # A ball (index 2)
                }
            ]
        elif npc.name == "Nikki":
            npc.dialogues = [
                "Hi, I'm Nikki! Have you heard the latest?",
                "Everyone's talking about Niamh's amazing paintings!",
                "Did you know she's also great with herbs?"
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
                    "options": ["The mayor", "The gossip", "The teacher", "The doctor"],
                    "correct_answers": [1]  # The gossip (index 1)
                }
            ]
        elif npc.name == "Paul":
            npc.dialogues = [
                "Hello there, I'm Paul. Have you seen the prices s lately?",
                "It's outrageous! I dont know what to do..",
                "I guess I'll just do what I always do.."
                "Now where the FUCK DID I PARK ME CAR? "
            ]
            npc.questions = [
                {
                    "question": "Whats bothering me most?",
                    "options": ["Weather", "Herb prices", "Dogs", "Fishing"],
                    "correct_answers": [1]  # Herb prices (index 1)
                },
                {
                    "question": "Where the fuck did I park me car?",
                    "options": ["Me, I did it.", "At home", "Over there", "Just here"],
                    "correct_answers": [1]  # At home (index 3)
                },
                {
                    "question": "Where do I put the lemons?",
                    "options": ["Down", "In a bag", "The trunk", "Back"],
                    "correct_answers": [1]  # In a bag (index 1)
                }
            ]
        elif npc.name == "Tony":
            npc.dialogues = [
                "Hey Mate, I'm Tony. I'm trying to make some cookies,",
                "And get real baked mate, bake a cake mate..",
                "Niamh makes the best cooking and baking though..",
                "I wonder what her secret is for such incredicle cooking.",
                "Man Im high.."
            ]
            npc.questions = [
                {
                    "question": "What was I talking about again?",
                    "options": ["Cookie", "Pitu", "Cake Bake Mate", "Melon"],
                    "correct_answers": [2]  # Herbs (index 2)
                },
                {
                    "question": "What does Niamh make that's the best?",
                    "options": ["Clothes", "Cooking", "Music", "Art"],
                    "correct_answers": [1]  # Cooking (index 1)
                },
                {
                    "question": "Pitu locked me out last night, what should I do?",
                    "options": ["Say no Pitu", "Lock Pitu out", "Sleep on the sofa", "Baricade the door"],
                    "correct_answers": [3]  # Baricade the door (index 1)
                }
            ]
        elif npc.name == "Keelan":
            npc.dialogues = [
                "Greetings, I'm Keelan. I mumbleriddles and you know.. ",
                "Pizza... goes well with herbs.",
                "Did you know the Ovenstoven Mega 2000 can bake whole family at once?",
                "The recordholder in baking most Pizzas is probobly not holdning any pizza right now...",
                "Some herbs are better than other, oh yes, oh yes."
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
                }
            ]
        # New NPCs will have their dialogues and questions set in GameModifications.setup_new_npcs()
    
    def create_obstacles(self):
        # Create obstacles for houses - adjusted for larger screen
        house_data = [
            (150, 250, 60, 50),  # House 1

        ]
        
        for x, y, width, height in house_data:
            obstacle = Obstacle(x, y, width, height)
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)
        
        # Create obstacles for trees - adjusted for larger screen
        tree_positions = [
            (120, 230),
            (220, 280),

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
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        level_text = self.font.render(f"Level: {self.level}", True, BLACK)
        self.screen.blit(level_text, (10, 50))
        
        correct_text = self.font.render(f"Correct Answers: {self.correct_answers}/{self.required_correct_answers}", True, BLACK)
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
            complete_text = self.font.render("Level Complete!", True, BLACK)
            complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(complete_text, complete_rect)
            
            continue_text = self.font.render("Press SPACE to continue", True, BLACK)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(continue_text, continue_rect)
            
        # Draw game won animation
        if self.game_state == "game_won":
            # Draw falling hearts
            for heart_pos in self.hearts_positions:
                self.screen.blit(self.heart_img, (heart_pos[0], heart_pos[1]))
            
            # Draw game won message
            won_text = self.font.render("Game Won: Erik & Niamh Kiss!", True, BLACK)
            won_rect = won_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(won_text, won_rect)
            
            continue_text = self.font.render("Press SPACE to continue", True, BLACK)
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
