import pygame, sys
from support import draw_text
from settings import BLACK, BUTTON_BASIC_COLOR, BUTTON_ACTIVE_COLOR


class Button(pygame.sprite.Sprite):
    def __init__(self, size, x, y, text, font):
        super().__init__()

        # Image:
        self.color_basic = BUTTON_BASIC_COLOR
        self.color_active = BUTTON_ACTIVE_COLOR
        self.image = pygame.Surface(size)
        self.image.fill(self.color_basic)
        self.rect = self.image.get_rect(center = (x, y))

        # Text on button:
        self.text = text
        self.font = font

        # Conditions:
        self.clicked = False

    def draw_content(self, SCREEN):
        draw_text(SCREEN, self.text, self.font, BLACK, self.rect.centerx, self.rect.centery)
        
    def check_click(self):
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check if button active and clicked:
        if self.rect.collidepoint(pos):
            self.color = BUTTON_ACTIVE_COLOR
            self.image.fill(self.color)

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        else:
            self.color = (105, 77, 86)
            self.image.fill(self.color)
        
        return action
    
    
class Start_Button(Button):
    def __init__(self, size, x, y, text, font):
        super().__init__(size, x, y, text, font)
        self.type = 'Start'

class Return_Button(Button):
    def __init__(self, size, x, y, text, font):
        super().__init__(size, x, y, text, font)
        self.type = 'Return'

class Menu_Button(Button):
    def __init__(self, size, x, y, text, font):
        super().__init__(size, x, y, text, font)
        self.type = 'Main Menu'

class Respawn(Button):
    def __init__(self, size, x, y, text, font):
        super().__init__(size, x, y, text, font)
        self.type = 'Respawn'
        
class Exit_Button(Button):
    def __init__(self, size, x, y, text, font):
        super().__init__(size, x, y, text, font)
        self.type = 'Exit'