import pygame

class Sign(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.direction = direction
        self.load_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.font = pygame.font.SysFont(None, 20)
        
    def load_image(self):
        self.image = pygame.image.load('assets/images/sign.png')
        
        # Make sprite twice the size
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (original_width * 2, original_height * 4))
        
    def draw_text(self, surface):
        # Draw the direction text on the sign
        text_surface = self.font.render(self.direction, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
        surface.blit(text_surface, text_rect)
