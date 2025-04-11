import pygame

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
DARK_BROWN = (101, 67, 33)
BLONDE = (255, 215, 0)
SKIN_LIGHT = (255, 222, 173)
SKIN_DARK = (139, 69, 19)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
TAN = (210, 180, 140)

def create_pixel_sprite(width, height, pixel_data):
    """Create a sprite from pixel data"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for y, row in enumerate(pixel_data):
        for x, color in enumerate(row):
            if color is not None:  # None means transparent
                surface.set_at((x, y), color)
    return surface

def create_erik_sprite():
    """Create Erik sprite - Blonde slim viking man, black pants"""
    # 16x24 pixel sprite (16 wide, 24 tall)
    pixel_data = [
        # Head (rows 0-7)
        [None, None, None, BLONDE, BLONDE, BLONDE, BLONDE, None, None, None, None, None, None, None, None, None],
        [None, None, BLONDE, BLONDE, BLONDE, BLONDE, BLONDE, BLONDE, None, None, None, None, None, None, None, None],
        [None, BLONDE, BLONDE, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, BLONDE, None, None, None, None, None, None, None, None],
        [None, BLONDE, SKIN_LIGHT, SKIN_LIGHT, BLUE, SKIN_LIGHT, BLUE, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, BLONDE, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, BLONDE, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, RED, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None, None],
        # Body (rows 8-15)
        [None, None, None, BLUE, BLUE, BLUE, BLUE, None, None, None, None, None, None, None, None, None],
        [None, None, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, None, None, None, None, None, None, None, None],
        [None, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, None, None, None, None, None, None, None],
        [None, SKIN_LIGHT, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, SKIN_LIGHT, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, BLUE, BLUE, BLUE, BLUE, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None],
        # Legs (rows 16-23)
        [None, None, None, BLACK, None, None, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLACK, None, None, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLACK, None, None, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLACK, None, None, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLACK, None, None, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLACK, None, None, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, BLACK, BLACK, None, None, BLACK, BLACK, None, None, None, None, None, None, None, None],
        [None, BLACK, BLACK, None, None, None, None, BLACK, BLACK, None, None, None, None, None, None, None],
    ]
    return create_pixel_sprite(16, 24, pixel_data)

def create_niamh_sprite():
    """Create Niamh sprite - Tall, light skinned, dark haired, orange pants, purple shirt"""
    # 16x24 pixel sprite (16 wide, 24 tall)
    pixel_data = [
        # Head (rows 0-7)
        [None, None, None, BLACK, BLACK, BLACK, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, None, None, None, None, None, None, None, None],
        [None, BLACK, BLACK, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, BLACK, None, None, None, None, None, None, None, None],
        [None, BLACK, SKIN_LIGHT, SKIN_LIGHT, BLUE, SKIN_LIGHT, BLUE, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, BLACK, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, BLACK, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, RED, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None, None],
        # Body (rows 8-15)
        [None, None, None, PURPLE, PURPLE, PURPLE, PURPLE, None, None, None, None, None, None, None, None, None],
        [None, None, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, None, None, None, None, None, None, None, None],
        [None, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, None, None, None, None, None, None, None],
        [None, SKIN_LIGHT, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, SKIN_LIGHT, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, PURPLE, PURPLE, PURPLE, PURPLE, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None],
        # Legs (rows 16-23)
        [None, None, None, ORANGE, None, None, ORANGE, None, None, None, None, None, None, None, None, None],
        [None, None, None, ORANGE, None, None, ORANGE, None, None, None, None, None, None, None, None, None],
        [None, None, None, ORANGE, None, None, ORANGE, None, None, None, None, None, None, None, None, None],
        [None, None, None, ORANGE, None, None, ORANGE, None, None, None, None, None, None, None, None, None],
        [None, None, None, ORANGE, None, None, ORANGE, None, None, None, None, None, None, None, None, None],
        [None, None, None, ORANGE, None, None, ORANGE, None, None, None, None, None, None, None, None, None],
        [None, None, ORANGE, ORANGE, None, None, ORANGE, ORANGE, None, None, None, None, None, None, None, None],
        [None, ORANGE, ORANGE, None, None, None, None, ORANGE, ORANGE, None, None, None, None, None, None, None],
    ]
    return create_pixel_sprite(16, 24, pixel_data)

def create_gus_sprite():
    """Create Gus sprite - Brown & black big dog"""
    # 24x16 pixel sprite (24 wide, 16 tall) - dog is horizontal
    pixel_data = [
        [None, None, None, None, None, None, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, BROWN, BROWN, DARK_BROWN, DARK_BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, BROWN, BROWN, DARK_BROWN, BLACK, BLACK, DARK_BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None, None, None, None, None, None],
        [None, BROWN, BROWN, BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None, None, None, None, None],
        [BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None, None, None],
        [BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None, None],
        [BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None],
        [None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None, None],
        [None, None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None],
        [None, None, None, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, None, None],
        [None, None, None, None, DARK_BROWN, DARK_BROWN, None, None, DARK_BROWN, DARK_BROWN, None, None, DARK_BROWN, DARK_BROWN, None, None, DARK_BROWN, DARK_BROWN, None, None, DARK_BROWN, DARK_BROWN, DARK_BROWN, None],
        [None, None, None, None, DARK_BROWN, DARK_BROWN, None, None, DARK_BROWN, DARK_BROWN, None, None, DARK_BROWN, DARK_BROWN, None, None, DARK_BROWN, DARK_BROWN, None, None, DARK_BROWN, DARK_BROWN, DARK_BROWN, None],
        [None, None, None, None, DARK_BROWN, DARK_BROWN, None, None, DARK_BROWN, DARK_BROWN, None, None, DARK_BROWN, DARK_BROWN, None, None, DARK_BROWN, DARK_BROWN, None, None, DARK_BROWN, DARK_BROWN, DARK_BROWN, None],
    ]
    return create_pixel_sprite(24, 16, pixel_data)

def create_nikki_sprite():
    """Create Nikki sprite - blond girl with baggy clothes"""
    # 16x24 pixel sprite (16 wide, 24 tall)
    pixel_data = [
        # Head (rows 0-7)
        [None, None, None, BLONDE, BLONDE, BLONDE, BLONDE, None, None, None, None, None, None, None, None, None],
        [None, None, BLONDE, BLONDE, BLONDE, BLONDE, BLONDE, BLONDE, None, None, None, None, None, None, None, None],
        [None, BLONDE, BLONDE, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, BLONDE, None, None, None, None, None, None, None, None],
        [None, BLONDE, SKIN_LIGHT, SKIN_LIGHT, BLUE, SKIN_LIGHT, BLUE, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, BLONDE, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, BLONDE, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, RED, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None, None],
        # Body (rows 8-15) - baggy clothes
        [None, None, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, None, None, None, None, None, None, None, None],
        [None, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, None, None, None, None, None, None, None],
        [GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, None, None, None, None, None, None],
        [GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, None, None, None, None, None, None],
        [None, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, None, None, None, None, None, None, None],
        [None, None, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, None, None, None, None, None, None, None, None],
        # Legs (rows 16-23)
        [None, None, None, BLUE, None, None, BLUE, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLUE, None, None, BLUE, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLUE, None, None, BLUE, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLUE, None, None, BLUE, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLUE, None, None, BLUE, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLUE, None, None, BLUE, None, None, None, None, None, None, None, None, None],
        [None, None, BLUE, BLUE, None, None, BLUE, BLUE, None, None, None, None, None, None, None, None],
        [None, BLUE, BLUE, None, None, None, None, BLUE, BLUE, None, None, None, None, None, None, None],
    ]
    return create_pixel_sprite(16, 24, pixel_data)

def create_paul_sprite():
    """Create Paul sprite - Skinny light man"""
    # 16x24 pixel sprite (16 wide, 24 tall)
    pixel_data = [
        # Head (rows 0-7)
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, BLUE, SKIN_LIGHT, BLUE, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, RED, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None, None],
        # Body (rows 8-15) - skinny
        [None, None, None, RED, RED, RED, RED, None, None, None, None, None, None, None, None, None],
        [None, None, RED, RED, RED, RED, RED, RED, None, None, None, None, None, None, None, None],
        [None, None, RED, RED, RED, RED, RED, RED, None, None, None, None, None, None, None, None],
        [None, SKIN_LIGHT, RED, RED, RED, RED, RED, RED, SKIN_LIGHT, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, RED, RED, RED, RED, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None],
        # Legs (rows 16-23)
        [None, None, None, BLUE, None, None, BLUE, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLUE, None, None, BLUE, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLUE, None, None, BLUE, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLUE, None, None, BLUE, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLUE, None, None, BLUE, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLUE, None, None, BLUE, None, None, None, None, None, None, None, None, None],
        [None, None, BLUE, BLUE, None, None, BLUE, BLUE, None, None, None, None, None, None, None, None],
        [None, BLUE, BLUE, None, None, None, None, BLUE, BLUE, None, None, None, None, None, None, None],
    ]
    return create_pixel_sprite(16, 24, pixel_data)

def create_tony_sprite():
    """Create Tony sprite - Tall and dark, with dark sunglasses"""
    # 16x24 pixel sprite (16 wide, 24 tall)
    pixel_data = [
        # Head (rows 0-7)
        [None, None, None, BLACK, BLACK, BLACK, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, None, None, None, None, None, None, None, None],
        [None, BLACK, BLACK, SKIN_DARK, SKIN_DARK, SKIN_DARK, SKIN_DARK, BLACK, None, None, None, None, None, None, None, None],
        [None, BLACK, SKIN_DARK, BLACK, BLACK, BLACK, BLACK, SKIN_DARK, None, None, None, None, None, None, None, None],
        [None, BLACK, SKIN_DARK, SKIN_DARK, SKIN_DARK, SKIN_DARK, SKIN_DARK, SKIN_DARK, None, None, None, None, None, None, None, None],
        [None, BLACK, SKIN_DARK, SKIN_DARK, SKIN_DARK, RED, SKIN_DARK, SKIN_DARK, None, None, None, None, None, None, None, None],
        [None, None, SKIN_DARK, SKIN_DARK, SKIN_DARK, SKIN_DARK, SKIN_DARK, None, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_DARK, SKIN_DARK, SKIN_DARK, None, None, None, None, None, None, None, None, None, None],
        # Body (rows 8-15) - tall
        [None, None, None, YELLOW, YELLOW, YELLOW, YELLOW, None, None, None, None, None, None, None, None, None],
        [None, None, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, None, None, None, None, None, None, None, None],
        [None, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, None, None, None, None, None, None, None],
        [None, SKIN_DARK, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, SKIN_DARK, None, None, None, None, None, None, None],
        [None, None, SKIN_DARK, YELLOW, YELLOW, YELLOW, YELLOW, SKIN_DARK, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_DARK, SKIN_DARK, SKIN_DARK, SKIN_DARK, None, None, None, None, None, None, None, None, None],
        # Legs (rows 16-23)
        [None, None, None, BLACK, None, None, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLACK, None, None, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLACK, None, None, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLACK, None, None, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLACK, None, None, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, None, BLACK, None, None, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, BLACK, BLACK, None, None, BLACK, BLACK, None, None, None, None, None, None, None, None],
        [None, BLACK, BLACK, None, None, None, None, BLACK, BLACK, None, None, None, None, None, None, None],
    ]
    return create_pixel_sprite(16, 24, pixel_data)

def create_keelan_sprite():
    """Create Keelan sprite - Herb expert with green clothes"""
    # 16x24 pixel sprite (16 wide, 24 tall)
    pixel_data = [
        # Head (rows 0-7)
        [None, None, None, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None, None, None, None, None],
        [None, None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, BROWN, BROWN, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, BROWN, None, None, None, None, None, None, None, None],
        [None, BROWN, SKIN_LIGHT, SKIN_LIGHT, GREEN, SKIN_LIGHT, GREEN, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, BROWN, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, BROWN, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, RED, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None, None],
        # Body (rows 8-15) - green clothes
        [None, None, None, GREEN, GREEN, GREEN, GREEN, None, None, None, None, None, None, None, None, None],
        [None, None, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, None, None, None, None, None, None, None, None],
        [None, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, None, None, None, None, None, None, None],
        [None, SKIN_LIGHT, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, SKIN_LIGHT, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, GREEN, GREEN, GREEN, GREEN, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None],
        # Legs (rows 16-23)
        [None, None, None, BROWN, None, None, BROWN, None, None, None, None, None, None, None, None, None],
        [None, None, None, BROWN, None, None, BROWN, None, None, None, None, None, None, None, None, None],
        [None, None, None, BROWN, None, None, BROWN, None, None, None, None, None, None, None, None, None],
        [None, None, None, BROWN, None, None, BROWN, None, None, None, None, None, None, None, None, None],
        [None, None, None, BROWN, None, None, BROWN, None, None, None, None, None, None, None, None, None],
        [None, None, None, BROWN, None, None, BROWN, None, None, None, None, None, None, None, None, None],
        [None, None, BROWN, BROWN, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, BROWN, BROWN, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None],
    ]
    return create_pixel_sprite(16, 24, pixel_data)

def create_tain_sprite():
    """Create Tain sprite - Cool dude in baggy pants and tank top, long hair, standing on skateboard"""
    # 16x24 pixel sprite (16 wide, 24 tall)
    pixel_data = [
        # Head (rows 0-7) with long hair
        [None, None, None, BLACK, BLACK, BLACK, BLACK, None, None, None, None, None, None, None, None, None],
        [None, None, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, None, None, None, None, None, None, None, None],
        [None, BLACK, BLACK, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, BLACK, None, None, None, None, None, None, None, None],
        [None, BLACK, SKIN_LIGHT, SKIN_LIGHT, BLUE, SKIN_LIGHT, BLUE, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, BLACK, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, BLACK, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, RED, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [BLACK, BLACK, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, BLACK, BLACK, None, None, None, None, None, None, None],
        [BLACK, BLACK, BLACK, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, BLACK, BLACK, BLACK, None, None, None, None, None, None, None],
        # Body (rows 8-15) - tank top
        [None, None, None, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, None, None, None, None, None, None, None, None, None],
        [None, None, LIGHT_BLUE, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, LIGHT_BLUE, None, None, None, None, None, None, None, None],
        [None, SKIN_LIGHT, LIGHT_BLUE, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, LIGHT_BLUE, SKIN_LIGHT, None, None, None, None, None, None, None],
        [None, SKIN_LIGHT, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, SKIN_LIGHT, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None],
        # Legs (rows 16-23) - baggy pants and skateboard
        [None, None, TAN, TAN, TAN, TAN, TAN, TAN, None, None, None, None, None, None, None, None],
        [None, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, None, None, None, None, None, None, None],
        [None, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, None, None, None, None, None, None, None],
        [None, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, None, None, None, None, None, None, None],
        [None, None, TAN, TAN, TAN, TAN, TAN, TAN, None, None, None, None, None, None, None, None],
        [None, None, None, BLACK, BLACK, BLACK, BLACK, None, None, None, None, None, None, None, None, None],
        [None, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, None, None, None, None, None, None, None],
        [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, None, None, None, None, None, None],
    ]
    return create_pixel_sprite(16, 24, pixel_data)

def create_chris_sprite():
    """Create Chris sprite - Guy with big smile and only one ear"""
    # 16x24 pixel sprite (16 wide, 24 tall)
    pixel_data = [
        # Head (rows 0-7) with only one ear
        [None, None, None, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None, None, None, None, None],
        [None, None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, BROWN, BROWN, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, BROWN, None, None, None, None, None, None, None, None],
        [None, BROWN, SKIN_LIGHT, SKIN_LIGHT, BLUE, SKIN_LIGHT, BLUE, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, BROWN, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None],
        [None, BROWN, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, RED, RED, RED, SKIN_LIGHT, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, RED, RED, RED, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None, None],
        # Body (rows 8-15)
        [None, None, None, PURPLE, PURPLE, PURPLE, PURPLE, None, None, None, None, None, None, None, None, None],
        [None, None, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, None, None, None, None, None, None, None, None],
        [None, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, None, None, None, None, None, None, None],
        [None, SKIN_LIGHT, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, SKIN_LIGHT, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, PURPLE, PURPLE, PURPLE, PURPLE, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None],
        # Legs (rows 16-23)
        [None, None, None, GREEN, None, None, GREEN, None, None, None, None, None, None, None, None, None],
        [None, None, None, GREEN, None, None, GREEN, None, None, None, None, None, None, None, None, None],
        [None, None, None, GREEN, None, None, GREEN, None, None, None, None, None, None, None, None, None],
        [None, None, None, GREEN, None, None, GREEN, None, None, None, None, None, None, None, None, None],
        [None, None, None, GREEN, None, None, GREEN, None, None, None, None, None, None, None, None, None],
        [None, None, None, GREEN, None, None, GREEN, None, None, None, None, None, None, None, None, None],
        [None, None, GREEN, GREEN, None, None, GREEN, GREEN, None, None, None, None, None, None, None, None],
        [None, GREEN, GREEN, None, None, None, None, GREEN, GREEN, None, None, None, None, None, None, None],
    ]
    return create_pixel_sprite(16, 24, pixel_data)

def create_magda_sprite():
    """Create Magda sprite - Very slow girl concerned about dogs and their feelings"""
    # 16x24 pixel sprite (16 wide, 24 tall)
    pixel_data = [
        # Head (rows 0-7)
        [None, None, None, ORANGE, ORANGE, ORANGE, ORANGE, None, None, None, None, None, None, None, None, None],
        [None, None, ORANGE, ORANGE, ORANGE, ORANGE, ORANGE, ORANGE, None, None, None, None, None, None, None, None],
        [None, ORANGE, ORANGE, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, ORANGE, None, None, None, None, None, None, None, None],
        [None, ORANGE, SKIN_LIGHT, SKIN_LIGHT, BLUE, SKIN_LIGHT, BLUE, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, ORANGE, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, ORANGE, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, BLUE, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None, None],
        # Body (rows 8-15)
        [None, None, None, YELLOW, YELLOW, YELLOW, YELLOW, None, None, None, None, None, None, None, None, None],
        [None, None, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, None, None, None, None, None, None, None, None],
        [None, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, None, None, None, None, None, None, None],
        [None, SKIN_LIGHT, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, SKIN_LIGHT, None, None, None, None, None, None, None],
        [None, None, SKIN_LIGHT, YELLOW, YELLOW, YELLOW, YELLOW, SKIN_LIGHT, None, None, None, None, None, None, None, None],
        [None, None, None, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, SKIN_LIGHT, None, None, None, None, None, None, None, None, None],
        # Legs (rows 16-23)
        [None, None, None, PURPLE, None, None, PURPLE, None, None, None, None, None, None, None, None, None],
        [None, None, None, PURPLE, None, None, PURPLE, None, None, None, None, None, None, None, None, None],
        [None, None, None, PURPLE, None, None, PURPLE, None, None, None, None, None, None, None, None, None],
        [None, None, None, PURPLE, None, None, PURPLE, None, None, None, None, None, None, None, None, None],
        [None, None, None, PURPLE, None, None, PURPLE, None, None, None, None, None, None, None, None, None],
        [None, None, None, PURPLE, None, None, PURPLE, None, None, None, None, None, None, None, None, None],
        [None, None, PURPLE, PURPLE, None, None, PURPLE, PURPLE, None, None, None, None, None, None, None, None],
        [None, PURPLE, PURPLE, None, None, None, None, PURPLE, PURPLE, None, None, None, None, None, None, None],
    ]
    return create_pixel_sprite(16, 24, pixel_data)

def create_pizza_sprite():
    """Create Pizza food item"""
    # 16x16 pixel sprite
    pixel_data = [
        [None, None, None, None, None, None, TAN, TAN, TAN, TAN, None, None, None, None, None, None],
        [None, None, None, None, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, None, None, None, None],
        [None, None, None, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, None, None, None],
        [None, None, TAN, TAN, TAN, RED, TAN, TAN, TAN, RED, TAN, TAN, TAN, TAN, None, None],
        [None, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, None],
        [None, TAN, TAN, RED, TAN, TAN, TAN, RED, TAN, TAN, TAN, RED, TAN, TAN, TAN, None],
        [TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN],
        [TAN, TAN, TAN, TAN, TAN, RED, TAN, TAN, TAN, RED, TAN, TAN, TAN, TAN, TAN, TAN],
        [TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN],
        [TAN, TAN, TAN, RED, TAN, TAN, TAN, RED, TAN, TAN, TAN, RED, TAN, TAN, TAN, TAN],
        [None, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, None],
        [None, TAN, TAN, TAN, TAN, RED, TAN, TAN, TAN, RED, TAN, TAN, TAN, TAN, None, None],
        [None, None, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, None, None, None],
        [None, None, None, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, None, None, None, None],
        [None, None, None, None, TAN, TAN, TAN, TAN, TAN, TAN, TAN, None, None, None, None, None],
        [None, None, None, None, None, None, TAN, TAN, TAN, TAN, None, None, None, None, None, None],
    ]
    return create_pixel_sprite(16, 16, pixel_data)

def create_kebab_sprite():
    """Create Kebab food item"""
    # 16x16 pixel sprite
    pixel_data = [
        [None, None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, BROWN, TAN, TAN, BROWN, None, None, None, None, None, None],
        [None, None, None, None, None, BROWN, TAN, RED, GREEN, TAN, BROWN, None, None, None, None, None],
        [None, None, None, None, BROWN, TAN, GREEN, TAN, TAN, RED, TAN, BROWN, None, None, None, None],
        [None, None, None, BROWN, TAN, RED, TAN, GREEN, RED, TAN, GREEN, TAN, BROWN, None, None, None],
        [None, None, BROWN, TAN, GREEN, TAN, RED, TAN, TAN, GREEN, TAN, RED, TAN, BROWN, None, None],
        [None, BROWN, TAN, RED, TAN, GREEN, TAN, RED, GREEN, TAN, RED, TAN, GREEN, TAN, BROWN, None],
        [BROWN, TAN, GREEN, TAN, RED, TAN, GREEN, TAN, TAN, RED, TAN, GREEN, TAN, RED, TAN, BROWN],
        [BROWN, TAN, TAN, GREEN, TAN, RED, TAN, GREEN, RED, TAN, GREEN, TAN, RED, TAN, TAN, BROWN],
        [None, BROWN, TAN, TAN, GREEN, TAN, RED, TAN, TAN, GREEN, TAN, RED, TAN, TAN, BROWN, None],
        [None, None, BROWN, TAN, TAN, GREEN, TAN, RED, GREEN, TAN, GREEN, TAN, TAN, BROWN, None, None],
        [None, None, None, BROWN, TAN, TAN, RED, TAN, TAN, RED, TAN, TAN, BROWN, None, None, None],
        [None, None, None, None, BROWN, TAN, TAN, GREEN, RED, TAN, TAN, BROWN, None, None, None, None],
        [None, None, None, None, None, BROWN, TAN, TAN, TAN, TAN, BROWN, None, None, None, None, None],
        [None, None, None, None, None, None, BROWN, TAN, TAN, BROWN, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None],
    ]
    return create_pixel_sprite(16, 16, pixel_data)

def create_meatball_sprite():
    """Create Meatball food item"""
    # 16x16 pixel sprite
    pixel_data = [
        [None, None, None, None, None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None],
        [None, None, None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None],
        [None, None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None],
        [None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None],
        [None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None],
        [BROWN, BROWN, BROWN, BROWN, BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN],
        [BROWN, BROWN, BROWN, BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, BROWN, BROWN, BROWN, BROWN, BROWN],
        [BROWN, BROWN, BROWN, BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, BROWN, BROWN, BROWN, BROWN, BROWN],
        [BROWN, BROWN, BROWN, BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, BROWN, BROWN, BROWN, BROWN, BROWN],
        [BROWN, BROWN, BROWN, BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, BROWN, BROWN, BROWN, BROWN, BROWN],
        [BROWN, BROWN, BROWN, BROWN, BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, DARK_BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN],
        [None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None],
        [None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None],
        [None, None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None],
        [None, None, None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None],
        [None, None, None, None, None, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, None, None, None, None, None],
    ]
    return create_pixel_sprite(16, 16, pixel_data)

def create_apple_sprite():
    """Create Apple food item"""
    # 16x16 pixel sprite
    pixel_data = [
        [None, None, None, None, None, None, None, GREEN, GREEN, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, GREEN, GREEN, GREEN, GREEN, None, None, None, None, None, None],
        [None, None, None, None, None, None, GREEN, GREEN, GREEN, GREEN, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None],
        [None, None, None, None, RED, RED, RED, RED, RED, RED, RED, RED, None, None, None, None],
        [None, None, None, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, None, None, None],
        [None, None, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, None, None],
        [None, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, None],
        [None, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, None],
        [None, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, None],
        [None, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, None],
        [None, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, None],
        [None, None, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, None, None],
        [None, None, None, RED, RED, RED, RED, RED, RED, RED, RED, RED, RED, None, None, None],
        [None, None, None, None, RED, RED, RED, RED, RED, RED, RED, RED, None, None, None, None],
        [None, None, None, None, None, None, RED, RED, RED, RED, None, None, None, None, None, None],
    ]
    return create_pixel_sprite(16, 16, pixel_data)

def create_sign_sprite():
    """Create directional sign sprite"""
    # 16x16 pixel sprite
    pixel_data = [
        [None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [TAN, TAN, TAN, TAN, TAN, TAN, BROWN, BROWN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN],
        [TAN, TAN, TAN, TAN, TAN, TAN, BROWN, BROWN, TAN, TAN, TAN, TAN, TAN, TAN, TAN, TAN],
        [None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, BROWN, BROWN, None, None, None, None, None, None, None, None],
    ]
    return create_pixel_sprite(16, 16, pixel_data)
