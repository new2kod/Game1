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
                            "options": ["Stinky Fish Sticks", "Cheese", "Sausage", "Biscuits"],
                            "correct_answers": [0]  # Stinky Fish sticks (index 0)
                        },
                        {
                            "question": "Woof! Woof! (Where do I like to sleep?)",
                            "options": ["The green", "Kitchen", "Niamh's spot", "By the fireplace"],
                            "correct_answers": [2]  # Niamh's spot (index 2)
                        },
                                                {
                            "question": "Kiffes? Where?",
                            "options": ["Face", "Ears", "Bellybutton", "Everywhere"],
                            "correct_answers": [0, 1, 2, 3]  # Yes Kisses!! (index 2)
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
    "I have to say..",
    "Have you heard about the Eurasian Blue Tit? Marvelous little bird I must say.",
    "Oh man thats INSANE",
    "Man that hillarious *adjusts imaginary monocle* Ha ha ha!",
    "I say, my good fellow! Did you know that wombats produce cube-shaped feces? Nature's little builders, what! Ha ha ha!",
    "My esteemed colleague James discovered that a day on Venus is longer than its year! Absolutely extraordinary, wouldn't you agree?",
    "Bro that's wild... I mean, *ahem* Rather fascinating development, old bean! *adjusts imaginare monocle*",
    "Indubitably splendid to make your acquaintance! Have you heard that honey never spoils? Archaeologists found 3000-year-old honey in Egyptian tombs still perfectly edible! Ha ha ha!",
    "Are you aware that flamingos are naturally white? Their diet of brine shrimp and algae turns them pink! Most remarkable pigmentation, what what!",
    "Yo, check this out... *straightens posture* I mean, observe with great interest, my good chap! Octopuses have three hearts! Quite the cardiovascular marvel!",
    "My dear friend James once counted all the ridges on a pickle and reached 107! What a splendidly peculiar afternoon activity! Ha ha ha!",
    "Did you know the shortest war in history lasted only 38 minutes? Between Britain and Zanzibar in 1896! Jolly efficient, if I do say so myself!",
    "Dude, that's crazy... *clears throat* Most distinguished observation, old sport! *twirls imaginary mustache*",
    "I must inform you that butterflies taste with their feet! My entomologist companion verified this extraordinary fact! Ha ha ha!"
                    ]
                    npc.questions = [
{
    "question": "Have you heard about the fascinating wingspan of the Albatross?",
    "options": ["Yes", "No", "Tell me more", "I don't care"],
    "correct_answers": [0, 2]  # Yes or Tell me more
},
{
    "question": "Did you know that skateboarding is an extreme sport?",
    "options": ["Yes", "No", "Fascinating!", "That's wrong"],
    "correct_answers": [0, 2]  # Yes or Fascinating!
},
{
    "question": "Have you heard my joke about the bird who couldn't pay his bill? Ha ha ha!",
    "options": ["Yes", "No", "Tell me", "Birds don't pay bills"],
    "correct_answers": [0, 2]  # Yes or Tell me
},
{
    "question": "My dear friend, are you aware that flamingos can only eat with their heads upside down? Ha ha ha! Quite peculiar, isn't it?",
    "options": ["No way", "Tell me more", "That's preposterous", "My word, how fascinating"],
    "correct_answers": [1, 3]  # Tell me more or My word, how fascinating
},
{
    "question": "My best mate James once told me that a group of pandas is called an 'embarrassment'! Ha ha ha! Jolly good term, wouldn't you agree?",
    "options": ["Absolutely", "That can't be right", "Tell me another collective noun", "James is incorrect"],
    "correct_answers": [0, 2]  # Absolutely or Tell me another collective noun
},
{
    "question": "Have you ever pondered why tea bags have exactly 27 perforations?! Ha ha ha!",
    "options": ["I hadn't noticed", "How fascinating", "That's not true", "I'm a coffee drinker"],
    "correct_answers": [1]  # How fascinating
},
{
    "question": "Did you know that the average person walks the equivalent of three times around the globe in a lifetime? One of my mates calculated it with extraordinary precision! Ha ha ha!",
    "options": ["No, I didn't", "That's quite remarkable", "I walk more than that", "Your mate is mistaken"],
    "correct_answers": [0, 1]  # No, I didn't or That's quite remarkable
},
{
    "question": "Have you heard my joke about the mathematician who was afraid of negative numbers? He would stop at nothing to avoid them! Ha ha ha!",
    "options": ["Yes", "No, do tell", "That's hilarious", "Mathematics isn't funny"],
    "correct_answers": [1, 2]  # No, do tell or That's hilarious
},
{
    "question": "Did you know that my best mate James once counted all the dimples on a golf ball? 336 precisely! Ha ha ha! What a splendid use of an afternoon!",
    "options": ["Remarkable dedication", "What a waste of time", "I don't believe it", "I'd like to meet James"],
    "correct_answers": [0, 3]  # Remarkable dedication or I'd like to meet James
},
{
    "question": "Are you aware that the fingerprints of a koala are so similar to humans that they have confused crime scene investigators? My Australian mate Tony told me this extraordinary fact! Ha ha ha!",
    "options": ["That can't be true", "How fascinating", "I knew that already", "Your mate is pulling your leg"],
    "correct_answers": [1, 2]  # How fascinating or I knew that already
},
{
    "question": "Have you heard about the chap who invented the Frisbee? After his death, he was cremated and made into Frisbees! Ha ha ha! Rather poetic end, wouldn't you say?",
    "options": ["That's morbid", "How delightfully eccentric", "I don't believe you", "Tell me more"],
    "correct_answers": [1, 3]  # How delightfully eccentric or Tell me more
},
{
    "question": "My best mate once told me that the Hawaiian alphabet has only 12 letters! Ha ha ha! Quite efficient, wouldn't you agree?",
    "options": ["Indeed", "That's not enough letters", "Tell me the letters", "Your pal is mistaken"],
    "correct_answers": [0, 2]  # Indeed or Tell me the letters
},
{
    "question": "Did you know that a snail can sleep for three years without eating? My best mate James observed this phenomenon! Ha ha ha! Talk about a good nap!",
    "options": ["Impossible", "How remarkable", "I wish I could do that", "Your mate needs better hobbies"],
    "correct_answers": [1, 2]  # How remarkable or I wish I could do that
},
{
    "question": "Have you heard my joke about the scarecrow who won an award? He was outstanding in his field! Ha ha ha!",
    "options": ["Yes", "No", "That's brilliant", "Scarecrows don't win awards"],
    "correct_answers": [2]  # That's brilliant
},
{
    "question": "My dear friend, are you aware that cows have best friends and become stressed when separated? My mate who owns a dairy farm made this astonishing discovery! Ha ha ha!",
    "options": ["How touching", "Cows don't have feelings", "I'd like to visit this farm", "Your mate is mistaken"],
    "correct_answers": [0, 2]  # How touching or I'd like to visit this farm
},
{
    "question": "Paul told me that the average person will spend six months of their life waiting at red lights? Ha ha ha! Quite the temporal investment!",
    "options": ["What a waste", "That's fascinating", "I avoid traffic lights", "Paul needs to drive faster"],
    "correct_answers": [1, 3]  # That's fascinating, and Paul needs to drive better
},
{
    "question": "Have you heard about the remarkable octopus that can fit through any hole larger than its beak? My best mate James witnessed this extraordinary feat! Ha ha ha!",
    "options": ["Preposterous", "That's amazing", "Tell me more about octopi", "James is exaggerating"],
    "correct_answers": [1, 2]  # That's amazing or Tell me more about octopi
},
{
    "question": "Did you know that if you were to remove all the empty space from the atoms in the human body, you'd be able to fit the entire world's population into an apple? My physicist mate calculated this! Ha ha ha!",
    "options": ["That's impossible", "How extraordinary", "Physics is fascinating", "I don't believe it"],
    "correct_answers": [1, 2]  # How extraordinary or Physics is fascinating
}
                    ]
                elif npc.name == "Chris":
                    npc.dialogues = [
    "Hey there! I'm Chris. You know, I almost lost both my ear when a kitchen fell from the sky, but luckily i!",
    "Today I nearly fell off a cliff, but I only scraped my knee. Things could have been so much worse!",
    "Like that time a Lion chased me at the Zoo and almost bit both me legs off...",
    "My house almost burned down yesterday, but only the curtains caught fire.",
    "I'm so lucky!",
    "Just this morning, a chandelier crashed down right where I was standing... two seconds after I moved! Talk about perfect timing!",
    "My car rolled down a hill yesterday with no brakes, but luckily it stopped just before the cliff edge. Just a small dent in the bumper!",
    "You see this tiny scratch on my arm? That's from when a helicopter blade nearly took my whole arm off! Got away with just a nick!",
    "I was swimming yesterday and almost got caught in a riptide, but I only lost my swimming trunks. Could've been much worse, eh?",
    "Last week I was struck by lightning! Well, not directly—it hit the tree next to me. Just singed my eyebrows a bit. Lucky me!",
    "I accidentally picked up a scorpion thinking it was my phone. Only got stung three times before I realized! Could've been dozens!",
    "The doctor says I've got the most near-miss bicycle accidents he's ever seen. Only broken my arm twice in 57 incidents!",
    "A piano fell from a third-story window while I was walking underneath. Missed me by inches! Just got a bit of dust on my shirt!",
    "My parachute failed to open during my first skydive, but fortunately the emergency chute worked... partially. Just twisted my ankle on landing!",
    "I was cooking with hot oil and the whole pan caught fire! Only burned half my kitchen and singed one eyebrow. Talk about a stroke of good fortune!",
    "Yesterday I was changing a light bulb when the ladder collapsed. Landed right on my sofa! Barely a bruise to show for it!",
    "My mate accidentally fired a nail gun at me during renovation. The nail just went through my shirt sleeve—didn't touch my skin at all! How's that for lucky?",
    "I went hiking in bear country and one chased me for about a mile. Only lost my backpack and one shoe! Could've been my life!",
    "The brakes on my bicycle failed going downhill, but I crashed into a conveniently placed hay bale! Just got a few scratches and a mouthful of straw!",
    "A tree fell on my tent while camping, but I'd just stepped out for a wee! The whole thing was flattened except my pillow. Talk about divine timing!"
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
},
{
    "question": "What's the most dangerous part of an English breakfast?",
    "options": ["Hot beans", "Boiling water" , "Sharp knife for toast", "Sausage choking hazard"],
    "correct_answers": [0, 2, 3]  # Multiple correct answers
},
{
    "question": "You know how I feel about the Spanish Bus Transport?",
    "options": ["They look good?", "Potential death traps?", "Cheap and Efficient?", "Good?"],
    "correct_answers": [1]  # Potential death traps!
},
{
    "question": "What's the riskiest activity at a Spanish beach?",
    "options": ["Swimming", "Building sandcastles", "Eating ice cream", "Seagull attacks"],
    "correct_answers": [0, 3]  # Swimming and Seagull attacks
},
{
    "question": "Which garden tool is most likely to cause a weekend disaster?",
    "options": ["Lawnmower", "Hedge trimmer", "Garden hose", "Rake"],
    "correct_answers": [0, 1, 3]  # Multiple hazards
},
{
    "question": "What's your assessment of umbrella safety?",
    "options": ["Essential rain protection", "Eye-poking hazards", "Lightning attractors", "Fashion accessories"],
    "correct_answers": [1, 2]  # Eye-poking hazards and Lightning attractors
},
{
    "question": "How do you take your tea without risking injury?",
    "options": ["Lukewarm", "With extra milk to cool it", "In a plastic cup", "Using tongs to hold me cup"],
    "correct_answers": [0, 1, 2, 3]  # All are valid safety measures
},
{
    "question": "What's the biggest danger at the beach?",
    "options": ["Flying ball", "Sunburn", "Sharks", "Children"],
    "correct_answers": [0, 1, 2, 3]  # All are potential hazards
},
{
    "question": "Which traditional British pudding poses the greatest threat?",
    "options": ["Spotted Dick", "Sticky Toffee Pudding", "Bread and Butter Pudding", "Christmas Pudding"],
    "correct_answers": [3]  # Christmas Pudding (could be set on fire)
},
{
    "question": "What's the most dangerous room in a typical Spanish home?",
    "options": ["Kitchen", "Bathroom", "Garden shed", "Fuse box"],
    "correct_answers": [0, 1, 2]  # Multiple dangerous rooms
},
{
    "question": "How do you rate the safety of afternoon tea?",
    "options": ["Good", "Burning risk", "Cups are slippery", "Tea stains are permanent"],
    "correct_answers": [1, 2, 3]  # Multiple hazards
}
                    ]
                elif npc.name == "Magda":
                    npc.dialogues = [
                        "Im Magda but it doesnt really matter.",
                        "Dogs feelings hurt when you no pet them. You think this true?",
                          "Sad dogs I see in rain. Why humans not give umbrella to dogs?",
                        "Dogs dream about running, yes? Or they dream about humans? What you think?",
                        "Dogs are smart, they too should get Glovo",
                        "Worried the dogs are, when food delivery late comes. Their sad eyes pierce my soul they do.",
                        "Wait for Glovo we must. Patience the dogs have not when hungry they become.",
                        "Emotions strong in small dogs they have. Big feelings in tiny bodies, yes.",
                        "Uber driver lost again he is. Anxious my little Pookie gets when dinner delayed is.",
                        "Treats in my pocket I keep. For when sad the doggie eyes become during long wait times.",
                        "Delivery app confusing it is. Dogs understand not why food comes not when promised it was.",
                        "Alert my puppies become when phone notification sounds. Hope then disappointment they feel when wrong app it is.",
                        "Rain makes delivery slow it does. Wet paws and sad whimpers result they do.",
                        "Stressed the delivery person must be. Dogs sense this they can when finally arrive they do.",
                        "Map on phone shows driver going wrong direction he is. Explain to dogs I cannot why longer they must wait.",
                        "Order canceled it was! Devastated my furry friends become. Understand app problems they cannot.",
                        "Happy dance the dogs do when doorbell finally rings it does. Forgotten is the waiting when food arrives.",
                        "Tip extra I always do. Appreciate the dogs when delivery person gives them gentle pat.",
                        "Dogs smell food they can before door opens it does. Powerful noses they have, patient hearts they do not.",
                        "Sometimes late night delivery scary it is. Protect me my dogs think they do when stranger with food arrives."
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
},
{
                    "question": "Delivery person late when is, dogs more angry become than humans do?",
                    "options": ["Yes", "No", "Depends on hunger level", "Time means nothing to dogs"],
                    "correct_answers": [0, 2]  # Yes or Depends on hunger level
},
{
                    "question": "Waiting for Glovo makes dogs drool they do?",
                                    "options": ["Always", "Never", "Only if food smells they sense", "Drool unrelated to food it is"],
                    "correct_answers": [0, 2]  # Always or Only if food smells they sense
},
{
                    "question": "Tail wagging means what when delivery arrives it does?",
                    "options": ["Anger", "Extreme happiness", "Confusion", "Exercise they need"],
                    "correct_answers": [1]  # Extreme happiness
},
{
                    "question": "Food delivery apps understand dogs can they?",
                    "options": ["Yes completely", "Words no but pictures yes", "Only bark detection they use", "Interface confusing for dogs it is"],
                    "correct_answers": [3]  # Interface confusing for dogs it is
},
{
                    "question": "Rain makes delivery person late, fair this is for hungry dogs?",
                    "options": ["Fair it is", "Unfair to dogs this is", "Weather controls no one", "Dogs care not about reasons"],
                                    "correct_answers": [2, 3]  # Weather controls no one or Dogs care not about reasons
},
{
                    "question": "Best delivery food for sharing with dogs what is?",
                    "options": ["Spicy noodles", "Salad with dressing", "Plain chicken and rice", "Chocolate cake"],
                    "correct_answers": [2]  # Plain chicken and rice
},
{
                                    "question": "When doorbell rings, dogs jump they do because what feeling?",
                    "options": ["Fear", "Anticipation", "Territorial protection", "Exercise they need"],
    "correct_answers": [1, 2]  # Anticipation or Territorial protection
},
{
    "question": "Dogs understand concept of tipping delivery person they do?",
    "options": ["Yes fully", "No concept of money they have", "Only if treats involved", "Financial systems confuse them"],
    "correct_answers": [1, 3]  # No concept of money they have or Financial systems confuse them
},
{
    "question": "Correct behavior is what when delivery person afraid of dogs is?",
    "options": ["Let dogs jump and play", "Hold dogs back you must", "Tell delivery leave food at door", "Dogs should understand human fear"],
    "correct_answers": [1, 2]  # Hold dogs back you must or Tell delivery leave food at door
},
{
    "question": "Uber Eats or Glovo better for dog-friendly delivery it is?",
    "options": ["Uber Eats faster it is", "Glovo dog treats sometimes brings", "Depends on restaurant not app", "Direct ordering best option is"],
    "correct_answers": [2, 3]  # Depends on restaurant not app or Direct ordering best option is
},
{
    "question": "When food arrives cold it does, dogs disappointed they get?",
    "options": ["No, temperature matters not", "Yes, warm food they prefer", "Only care about smell they do", "Depends on breed of dog"],
    "correct_answers": [0, 2]  # No, temperature matters not or Only care about smell they do
},
{
    "question": "Phone notifications make dogs anxious why they do?",
    "options": ["Sound hurts their ears", "Associate with delivery they do", "Random noises scary are", "Technology dogs mistrust"],
    "correct_answers": [1, 2]  # Associate with delivery they do or Random noises scary are
}
                    ]
                elif npc.name == "Ivan":
                    npc.dialogues = [
    "Hey, I'm Ivan. You want to play a game of pool with me?",
    "And maybe later we even do another thing but I dont know what it is being called..?",
    "I want to ask you, was my hair O.K? ",
    "Im at the beach scooter now, maybe we play pool later?",
    "My brother was here so I had to go out. ",
    "This wind is messing up my hair, but does it look more natural, or what do you think?",
    "I need to cut my hair maybe? No, I don't. I just want to know if it looks good.",
    "Pool tournament will be on Wednessday, you coming, or what do you think?",
    "I spent three hours styling my hair today. Is it too much volume on top?",
    "When wind blows through my hair at beach, everyone looks at me. This is problem, or what do you think?",
    "I have good chance of winning, but only when my hair is perfect.",
    "I want to try new hair style, but worried it won't hold during intense pool matches.",
    "People say Im good at my hair and pool, these are important things, no?",
    "If I win tournament, maybe we roll a community joint, or what do you think?",
    "When I lean over pool table, hair falls in my eyes.",
    "hat do you think?"
                    ]
                    npc.questions = [
                    {
        "question": "Do you know when the pool tournament start?",
        "options": ["When Tony says", "When you say", "When Tero comes", "At 8"],
        "correct_answers": [3]  # At 8 (index 1)
    },
    {
        "question": "In the tournament, Which ball do I shoot to touch the ball, to go touch the ball, other ball, if you know what I mean. Before I go in the wall?",
        "options": ["White", "Red", "Black", "Yellow"],
        "correct_answers": [0]  # White (index 1)
    },
    {
        "question": "What's my job?",
        "options": ["Pool Tournament Referee", "Waiter", "Barber", "Make Ice Cream"],
        "correct_answers": [0]  # Pool Tournament Referee (index 2)
    },
    {
        "question": "Does my hair look better now, or like this? or what do you think?",
        "options": ["In the wind", "Falling forward", "Like that", "Like this"],
        "correct_answers": [0, 1, 2, 3]  # All of them
    },
    {
        "question": "How many hours I spend on my hair each morning?",
        "options": ["30 minutes", "1 hour", "2 hours", "10 minutes"],
        "correct_answers": [1]  # 1 hour
    },
    {
        "question": "When wind blows my hair, what is best response from friends?",
        "options": ["Ignore it", "Compliment it", "Offer a hair tie", "Tell me to cut it"],
        "correct_answers": [1]  # Compliment it
    },
    {
        "question": "What happens if we roll a community joint?",
        "options": ["Roll it", "Ok lets", "Naa", "I'd prefer not"],
        "correct_answers": [0,1 ]  # Roll it & lets go
    },
    {
        "question": "What color is my special tournament hair band?",
        "options": ["Red", "Blue", "Black", "I don't wear hair band"],
        "correct_answers": [0]  # Red
    },
    {
        "question": "How many pool tournaments I have won this year?",
        "options": ["None yet", "Three", "One", "Seven"],
        "correct_answers": [2]  # One
    },
    {
        "question": "What do I do when someone says my hair looks bad?",
        "options": ["Cry in bathroom", "Challenge them to pool game", "Ask for styling advice", "Ignore them completely"],
        "correct_answers": [1]  # Challenge them to pool game
    },
    {
        "question": "Which is worse problem: bad hair day or losing pool game?",
        "options": ["Bad hair day", "Losing pool game", "Both equally bad", "Neither is problem"],
        "correct_answers": [2]  # Both equally bad
    },
    {
        "question": "Where I get my special hair look from?",
        "options": ["The wind", "Products", "Copy my brother", "My mother styles it"],
        "correct_answers": [0]  # The winds styles it
    },
    {
        "question": "What I do with the prize from pool tournament?",
        "options": ["Bake bread", "Roll & smoke it", "Smoke it at home", "Shopping"],
        "correct_answers": [1, 2]  # Both save for hair products and get new pool cue
    },
    {
        "question": "How long I grow my hair before I trim it, or what do you think?",
        "options": ["Never trim", "Every two weeks", "Six months", "When it touches my shoulders"],
        "correct_answers": [0]  # Never trim
    },
    {
        "question": "Best way to keep hair out of eyes when making crucial pool shot, at the tournament?",
        "options": ["Special clip", "Red headband", "Hair spray extra strong", "Quick head flip"],
        "correct_answers": [3]  # Quick head flip
    },
    {
        "question": "Who is my biggest rival in pool tournament this year?",
        "options": ["Tain", "Marcus with the mustache", "Tony", "My brother"],
        "correct_answers": [2]  # Tony
    },
    {
        "question": "If wind messes up my hair before tournament, I just..?",
        "options": ["Brush with water", "hair spray", "Head flip", "Leave"],
        "correct_answers": [2]  # Head flip
    }
                ]
    
    @staticmethod
    def create_food_items(game):
        """Create food items and add them to the game"""
        food_data = [
            (500, 550, "kebab"),
            (550, 650, "kebab"),
            (850, 550, "kebab"),

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
