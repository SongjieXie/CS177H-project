import pygame as pg


pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')

RUN_COLOR = pg.Color(0,150,50)
PAUSE_COLOR = pg.Color(150, 150, 150)
BLACK = pg.Color(0,0,0)
FONT = pg.font.Font(None, 26)


class InputBox:

    def __init__(self, x, y, w, h, text='3', label= 'Carteen R:', draw_label=True):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

        self.para = float(text)
        self.label_surface = FONT.render(label, True, BLACK)
        self.draw_label = draw_label

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    # self.text = ''
                    self.para = float(self.text)
                    # self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(60, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Draw label
        if self.draw_label:
            screen.blit(self.label_surface, (self.rect.x+5-150, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 1)


    def get_value(self):
        return self.para


class ButtonBox:

    def __init__(self, x, y, w=70, h=70, str1="PAUSE", str2="RUN"):
        self.str1 = str1
        self.str2 = str2
        self.rect = pg.Rect(x, y, w, h)
        self.color = PAUSE_COLOR
        self.txt_surface = FONT.render(self.str1, True, BLACK)
        self.active = False


    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            self.color = RUN_COLOR if self.active else PAUSE_COLOR
            text = self.str2 if self.active else self.str1
            self.txt_surface = FONT.render(text, True, BLACK)
            


    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 0)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+10, self.rect.y+10))


    def get_flag(self):
        return self.active



