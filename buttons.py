import pygame, sys
from support import draw_text, scale_image
from settings import WHITE, BUTTON_BASIC_COLOR, BUTTON_ACTIVE_COLOR, BUTTON_SIZE


class Button(pygame.sprite.Sprite):
    def __init__(self, size, x, y, text, font):
        super().__init__()

        # Image:
        self.color_basic = BUTTON_BASIC_COLOR
        self.color_active = BUTTON_ACTIVE_COLOR
        self.position = (x, y)
        self.set_image(False)

        # Text on button:
        self.text = text
        self.font = font

        # Conditions:
        self.clicked = False

    def set_image(self, active):
        if not active:
            self.image = pygame.image.load('content/graphics/ui/button.png').convert_alpha()
        else:
            self.image = pygame.image.load('content/graphics/ui/button_active.png').convert_alpha()
        self.image = scale_image(self.image, BUTTON_SIZE)
        self.rect = self.image.get_rect(center=self.position)

    def draw_content(self, SCREEN):
        draw_text(SCREEN, self.text, self.font, WHITE, self.rect.centerx, self.rect.centery)
        
    def check_click(self):
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check if button active and clicked:
        if self.rect.collidepoint(pos):
            self.set_image(True)

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        else:
            self.set_image(False)
        
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