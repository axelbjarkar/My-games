import pygame
from color_library import BLACK, WHITE

# Þessi klasi birtir skilaboð á skjánum á skjánum
# object byggt sem text = Message((x,x), 'texti', font_size, font--optional)
# notið screen.blit(text.get_render(), text.center() - text.bottom_message()) til að birta texta
# defualt gildin í klasanum eru leturgerð og litur

class Message():
    def __init__(self, screen_size, input_text, font_size, font = 'Arial Black', color = (255,255,255)):
        self.font_arialblack = pygame.font.SysFont(font, font_size)
        self.text = input_text
        self.screen_size = screen_size
        self.text_width, self.text_height = self.font_arialblack.size(self.text)
        self.color = color
        self.x_pos = None
        self.y_pos = None

    # Skilaboð birtast fyrir miðju
    def center(self, input_y=None):
        x_pos = self.screen_size[0]/2 - (self.text_width/2)
        if type(input_y) == int:
            y_pos = input_y
        else:
            y_pos = self.screen_size[1]/2 - (self.text_height/2)
        text_cords = (x_pos, y_pos)
        self.x_pos = x_pos
        self.y_pos = y_pos
        return text_cords

    # Skilaboð birtast neðst á skjánum
    def bottom_message(self):
        x_pos = self.screen_size[0]/2 - (self.text_width/2)
        y_pos = self.screen_size[1]- (self.text_height)
        text_cords = (x_pos, y_pos)
        self.x_pos = x_pos
        self.y_pos = y_pos
        return text_cords
    
    # Skilaboð birtast á sérstöku hniti
    def custom_location(self, screen_x, screen_y):
        x_pos = screen_x - (self.text_width/2)
        y_pos = screen_y - (self.text_height/2)
        text_cords = (x_pos, y_pos)
        self.x_pos = x_pos
        self.y_pos = y_pos
        return text_cords
    
    # Miða við hægri eða vinstri
    def align(self, key, input_y, x_indent=0):
        if key == 'left':
            x_pos = 0 + x_indent
        if key == 'right':
            x_pos = self.screen_size[0] - self.text_width - x_indent
        y_pos = input_y
        text_cords = (x_pos, y_pos)
        self.x_pos = x_pos
        self.y_pos = y_pos
        return text_cords

    # Fær hnit texta á skjá - notist eftir að texti hefur verið staðsettur!
    # Notast í rannsóknavinnu
    def get_cords(self, key=None):
        if key == 'x':
            return self.x_pos
        elif key == 'y':
            return self.y_pos
        else:
            return (self.x_pos, self.y_pos)

    # Rendera skilaboð svo hægt sé að birta þau
    def get_render(self):
        return self.font_arialblack.render(self.text, True, self.color)

class InputBox():
    def __init__(self, screen, x, y, width, height, text = '', active_color = pygame.Color('dodgerblue2'), inactive_color = pygame.Color('lightskyblue3'), using_limit = False):
        # Kassinn sjálfur
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        # Þegar að object-ið er fyrst búið til, er kassinn óvirkur
        self.active = False
        # Litir
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.current_color = self.inactive_color
        # Textinn í kassanum
        self.screen = screen
        self.text = text
        self.temp_text = None
        self.FONT = pygame.font.SysFont(None, height)
        self.text_surface = self.FONT.render(self.text, True, self.current_color)
        self.using_limit = using_limit
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.current_color = self.active_color
            else:
                self.active = False
                self.current_color = self.inactive_color
    
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.temp_text = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.using_limit:
                        if self.text_surface.get_width() >= self.width:
                            None
                        else:
                            self.text += event.unicode
                    else:
                        self.text += event.unicode
        
    def update(self):
        self.text_surface = self.FONT.render(self.text, True, self.current_color)
        width = max(200, self.text_surface.get_width()+10)
        self.rect.width = width
            
    
    def draw(self):
        self.screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(self.screen, self.current_color, self.rect, 2)
    
    def finished(self):
        if self.temp_text:
            return True
        else:
            return False
    
    def get_text(self):
        return self.temp_text