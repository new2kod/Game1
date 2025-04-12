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
                            "question": "What is my favorite time of the day?",
                            "options": ["Morning", "Lunch", "Later..", "Midnight"],
                            "correct_answers": [2]  # Later.. (index 2)
                        },
                        {
                            "question": "Which herb do I find most fascinating?",
                            "options": ["Basil", "Gelato", "Rosemary", "Thyme"],
                            "correct_answers": [1]  # Gelato (index 1)
                        }
                    ])
                elif npc.name == "Gus":
                    npc.questions.extend([
                        {
                            "question": "Woof! (What's my favorite treat?)",
                            "options": ["Stinky Fish sticks", "Cheese", "Sausage", "Biscuits"],
                            "correct_answers": [0]  # Stinky Fish sticks (index 0)
                        },
                        {
                            "question": "Woof! Woof! (Where do I like to sleep?)",
                            "options": ["The green", "Kitchen", "Niamh's spot", "By the fireplace"],
                            "correct_answers": [2]  # Niamh's spot (index 2)
                        }
                    ])
                elif npc.name == "Nikki":
                    npc.questions.extend([
                        {
                            "question": "What's the latest?",
                            "options": ["Buying a car", "I got some real rare herb", "Im shrinking", "Im opening a pub"],
                            "correct_answers": [1]  # I got some real rare herb (index 1)
                        },
                        {
                            "question": "Who do I think Niamh likes?",
                            "options": ["Paul", "Tony", "Erik", "Keelan"],
                            "correct_answers": [2]  # Erik (index 2)
                        }
                    ])
                elif npc.name == "Paul":
                    npc.questions.extend([
                        {
                            "question": "Which herb price has increased the most?",
                            "options": ["Basil", "Thyme", "Sage", "Gelato"],
                            "correct_answers": [3]  # Gelato (index 3)
                        },
                        {
                            "question": "What kind of house would suit Niamh best?",
                            "options": ["Earthship", "Apartment", "Farmhouse", "Beach house"],
                            "correct_answers": [0]  # Earthship (index 0)
                        }
                    ])
                elif npc.name == "Tony":
                    npc.questions.extend([
                        {
                            "question": "What herb am I trying to grow, thats soon ready?",
                            "options": ["Mint", "Cookies", "Basil", "Parsley"],
                            "correct_answers": [1]  # Cookies (index 1)
                        },
                        {
                            "question": "What dish does Niamh make that I love the most?",
                            "options": ["Herb soup", "Roasted chicken", "Meat and taters", "Pasta"],
                            "correct_answers": [2]  # Meat and taters (index 2)
                        }
                    ])
                elif npc.name == "Keelan":
                    npc.questions.extend([
                        {
                            "question": "Riddle: I am purple and calming, what herb am I?",
                            "options": ["Sage", "Cherry Gelato", "Thyme", "Mint"],
                            "correct_answers": [1]  # Cherry Gelato (index 1)
                        },
                        {
                            "question": "Riddle: Niamh uses me to roll or make tea, for good sleep. What am I?",
                            "options": ["Chamomile", "Zkittles", "Lemon balm", "All of these"],
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
                        "I say..",
                        "Have you heard about the Eurasian Blue Tit? Marvelous little bird I must say.",
                        "Man that hillarious *adjusts imaginary monocle* Ha ha ha!"
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
                        "Hey there! I'm Chris. You know, I almost lost both my ear when a kitchen fell from the sky, but luckily i!",
                        "Today I nearly fell off a cliff, but I only scraped my knee. Things could have been so much worse!",
                        "Like that time a Lion chased me at the Zoo and almost bit both me legs off...",
                        "My house almost burned down yesterday, but only the curtains caught fire.",
                        "I'm so lucky!"
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
                            "options": ["Blue", "Red", "Green", "Snack-Brown"],
                            "correct_answers": [3]  # Snack-Brown
                        }
                    ]
                elif npc.name == "Ivan":
                    npc.dialogues = [
                    "Hey, I'm Ivan. You want to play a game of pool with me?",
                    "And maybe later we even do another thing but I dont know what it is being called..?",
                    "I want to ask you, was my hair O.K? ",
                    "My brother was here so I had to go out. "
                    ]
                    npc.questions = [
                    {
                        "question": "Do you know when the pool tournament start?",
                        "options": ["When Tony says", "When you say", "When Tero comes", "8 o'clock"],
                        "correct_answers": [3]  # 8 o 'clock (index 1)
                    },
                    {
                        "question": "Which ball do you aim for in a trick shot I love?",
                        "options": ["Cue ball", "8-ball", "Stripes", "Solids"],
                        "correct_answers": [1]  # 8-ball (index 1)
                    },
                    {
                        "question": "What's my favorite pool game?",
                        "options": ["Snooker", "9-ball", "8-ball", "Straight pool"],
                        "correct_answers": [2]  # 8-ball (index 2)
                    }
                ]
    
    @staticmethod
    def create_food_items(game):
        """Create food items and add them to the game"""
        food_data = [
            (500, 450, "kebab"),
            (550, 500, "kebab"),

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
            (600, 550, "Home"),
            (900, 350, "Aeropuerto"),
            (150, 450, "Torrequebrada")
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
