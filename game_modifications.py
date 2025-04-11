import pygame
import sys
import math
import random
from food import Food
from sign import Sign
from npc_movement import NPCMovement

class GameModifications:
    """Class to handle all the new game modifications"""
    
    @staticmethod
    def update_npc_questions(game):
        """Add more questions and answers to every sprite based on their original interests"""
        
        # Add more questions for Niamh
        if game.npcs:
            for npc in game.npcs:
                if npc.name == "Niamh":
                    npc.questions.extend([
                        {
                            "question": "What is my favorite time to paint?",
                            "options": ["Morning", "Afternoon", "Sunset", "Midnight"],
                            "correct_answers": [2]  # Sunset (index 2)
                        },
                        {
                            "question": "Which herb do I find most fascinating?",
                            "options": ["Basil", "Lavender", "Rosemary", "Thyme"],
                            "correct_answers": [1]  # Lavender (index 1)
                        }
                    ])
                elif npc.name == "Gus":
                    npc.questions.extend([
                        {
                            "question": "Woof! (What's my favorite treat?)",
                            "options": ["Bacon", "Cheese", "Sausage", "Biscuits"],
                            "correct_answers": [0]  # Bacon (index 0)
                        },
                        {
                            "question": "Woof! Woof! (Where do I like to sleep?)",
                            "options": ["Garden", "Kitchen", "Niamh's bed", "By the fireplace"],
                            "correct_answers": [2]  # Niamh's bed (index 2)
                        }
                    ])
                elif npc.name == "Nikki":
                    npc.questions.extend([
                        {
                            "question": "What's the latest gossip about Niamh?",
                            "options": ["She's moving away", "She found a rare herb", "She's opening a shop", "She's writing a book"],
                            "correct_answers": [1]  # She found a rare herb (index 1)
                        },
                        {
                            "question": "Who do I think Niamh secretly likes?",
                            "options": ["Paul", "Tony", "Erik", "Keelan"],
                            "correct_answers": [2]  # Erik (index 2)
                        }
                    ])
                elif npc.name == "Paul":
                    npc.questions.extend([
                        {
                            "question": "Which herb price has increased the most?",
                            "options": ["Basil", "Thyme", "Sage", "Rosemary"],
                            "correct_answers": [3]  # Rosemary (index 3)
                        },
                        {
                            "question": "What kind of house would suit Niamh best?",
                            "options": ["Cottage", "Apartment", "Farmhouse", "Beach house"],
                            "correct_answers": [0]  # Cottage (index 0)
                        }
                    ])
                elif npc.name == "Tony":
                    npc.questions.extend([
                        {
                            "question": "What herb am I trying to grow that keeps failing?",
                            "options": ["Mint", "Cilantro", "Basil", "Parsley"],
                            "correct_answers": [1]  # Cilantro (index 1)
                        },
                        {
                            "question": "What dish does Niamh make that I love the most?",
                            "options": ["Herb soup", "Roasted chicken", "Herb bread", "Pasta"],
                            "correct_answers": [2]  # Herb bread (index 2)
                        }
                    ])
                elif npc.name == "Keelan":
                    npc.questions.extend([
                        {
                            "question": "Riddle: I am purple and calming, what herb am I?",
                            "options": ["Sage", "Lavender", "Thyme", "Mint"],
                            "correct_answers": [1]  # Lavender (index 1)
                        },
                        {
                            "question": "Riddle: Niamh uses me in her tea for good sleep. What am I?",
                            "options": ["Chamomile", "Mint", "Lemon balm", "All of these"],
                            "correct_answers": [3]  # All of these (index 3)
                        }
                    ])
    
    @staticmethod
    def setup_new_npcs(game):
        """Set up dialogues and questions for the new NPCs: Tain, Chris, and Magda"""
        
        if game.npcs:
            for npc in game.npcs:
                if npc.name == "Tain":
                    npc.dialogues = [
                        "Good day, old chap! I'm Tain. Have you heard about the fascinating migratory patterns of the Arctic Tern?",
                        "Jolly good to see you! Did you know that a skateboard's wheels are made of polyurethane? Quite remarkable, isn't it? Ha ha ha!",
                        "I say, have you heard about the Eurasian Blue Tit? Marvelous little bird! *adjusts imaginary monocle* Ha ha ha!"
                    ]
                    npc.questions = [
                        {
                            "question": "Have you heard about the fascinating wingspan of the Albatross?",
                            "options": ["Yes", "No", "Tell me more", "I don't care"],
                            "correct_answers": [0, 2]  # Yes or Tell me more
                        },
                        {
                            "question": "Did you know that skateboarding originated in California in the 1950s?",
                            "options": ["Yes", "No", "Fascinating!", "That's wrong"],
                            "correct_answers": [0, 2]  # Yes or Fascinating!
                        },
                        {
                            "question": "Have you heard my joke about the bird who couldn't pay his bill? Ha ha ha!",
                            "options": ["Yes", "No", "Tell me", "Birds don't pay bills"],
                            "correct_answers": [0, 2]  # Yes or Tell me
                        }
                    ]
                elif npc.name == "Chris":
                    npc.dialogues = [
                        "Hey there! I'm Chris. You know, I almost lost both my ears in a gardening accident, but luckily only lost one!",
                        "Today I nearly fell off a cliff, but I only scraped my knee. Things could have been so much worse!",
                        "My house almost burned down yesterday, but only the curtains caught fire. I'm so lucky!"
                    ]
                    npc.questions = [
                        {
                            "question": "What do you think of thatched roof houses?",
                            "options": ["They're nice", "Fire hazards", "Traditional", "Expensive"],
                            "correct_answers": [1]  # Fire hazards
                        },
                        {
                            "question": "Which herb is most likely to cause allergic reactions?",
                            "options": ["Basil", "Cilantro", "Mint", "Thyme"],
                            "correct_answers": [1]  # Cilantro
                        },
                        {
                            "question": "What's worse: falling down stairs or slipping in the shower?",
                            "options": ["Stairs", "Shower", "Both are bad", "Neither is bad"],
                            "correct_answers": [0, 1, 2]  # Any of the first three
                        }
                    ]
                elif npc.name == "Magda":
                    npc.dialogues = [
                        "Dogs feelings hurt when you no pet them. You think this true?",
                        "Sad dogs I see in rain. Why humans not give umbrella to dogs?",
                        "Dogs dream about running, yes? Or they dream about humans? What you think?"
                    ]
                    npc.questions = [
                        {
                            "question": "Dogs happy are when belly rubs they get?",
                            "options": ["Yes", "No", "Sometimes", "Dogs don't like belly rubs"],
                            "correct_answers": [0, 2]  # Yes or Sometimes
                        },
                        {
                            "question": "When alone dogs are, they feel abandoned you think?",
                            "options": ["Yes", "No", "Depends on the dog", "Dogs enjoy solitude"],
                            "correct_answers": [0, 2]  # Yes or Depends on the dog
                        },
                        {
                            "question": "Favorite color of dogs what is?",
                            "options": ["Blue", "Red", "Green", "Dogs can't see many colors"],
                            "correct_answers": [3]  # Dogs can't see many colors
                        }
                    ]
    
    @staticmethod
    def create_food_items(game):
        """Create food items and add them to the game"""
        food_data = [
            (200, 200, "pizza"),
            (400, 150, "kebab"),
            (600, 250, "meatball"),
            (800, 300, "apple"),
            (300, 500, "pizza"),
            (500, 600, "kebab"),
            (700, 400, "meatball"),
            (900, 700, "apple")
        ]
        
        # Create food group if it doesn't exist
        if not hasattr(game, 'food_items'):
            game.food_items = pygame.sprite.Group()
        
        # Create food items
        for x, y, food_type in food_data:
            food = Food(x, y, food_type)
            game.food_items.add(food)
            game.all_sprites.add(food)
    
    @staticmethod
    def create_direction_signs(game):
        """Create directional signs and add them to the game"""
        sign_data = [
            (250, 200, "Marina →"),
            (750, 300, "← Cat Allé"),
            (500, 250, "The Club ↑"),
            (400, 550, "Arroyo ↓"),
            (600, 500, "← The Green →")
        ]
        
        # Create signs group if it doesn't exist
        if not hasattr(game, 'signs'):
            game.signs = pygame.sprite.Group()
        
        # Create sign items
        for x, y, direction in sign_data:
            sign = Sign(x, y, direction)
            game.signs.add(sign)
            game.all_sprites.add(sign)
    
    @staticmethod
    def setup_npc_movement(game):
        """Set up movement for NPCs"""
        # Create a dictionary to store movement handlers
        if not hasattr(game, 'npc_movement_handlers'):
            game.npc_movement_handlers = {}
        
        # Set up movement for each NPC except Niamh and Gus
        for npc in game.npcs:
            if npc.name not in ["Niamh", "Gus"]:
                game.npc_movement_handlers[npc.name] = NPCMovement(npc)
    
    @staticmethod
    def update_npc_positions(game):
        """Update NPC positions - place Niamh in the middle of the world"""
        # Find Niamh and Nikki
        niamh_sprite = None
        nikki_sprite = None
        
        for npc in game.npcs:
            if npc.name == "Niamh":
                niamh_sprite = npc
            elif npc.name == "Nikki":
                nikki_sprite = npc
        
        # Swap positions if both are found
        if niamh_sprite and nikki_sprite:
            # Store Nikki's position
            nikki_x = nikki_sprite.rect.x
            nikki_y = nikki_sprite.rect.y
            
            # Move Niamh to center
            niamh_sprite.rect.x = game.screen.get_width() // 2
            niamh_sprite.rect.y = game.screen.get_height() // 2
            
            # Move Nikki to Niamh's old position
            nikki_sprite.rect.x = nikki_x
            nikki_sprite.rect.y = nikki_y
            
            # Update Gus movement to follow Niamh at new position
            if game.gus_movement:
                game.gus_movement.niamh = niamh_sprite
    
    @staticmethod
    def add_game_functions(game):
        """Add new game functions"""
        # Add wrong answer counter attribute to NPC class
        for npc in game.npcs:
            npc.wrong_answers = 0
            
        # Add game won animation attributes
        game.game_won = False
        game.game_won_timer = 0
        game.hearts_positions = []
        
        # Load heart image for animation
        heart_img = pygame.image.load('assets/images/heart_8.png')
        game.heart_img = pygame.transform.scale(heart_img, (32, 32))
        
        # Initialize heart positions for animation
        for _ in range(20):
            game.hearts_positions.append([
                random.randint(0, game.screen.get_width()),
                random.randint(-500, 0),
                random.randint(1, 3)  # Speed
            ])
