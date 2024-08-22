import pygame
class textbutton:
    def __init__(self, x, y, width, height, text, onclick = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.onclick = onclick
        self.fillcolors = {
            "normal":pygame.Color(255,255,255),
            "hover":pygame.Color(120,120,120),
            "pressed":pygame.Color(0,0,0),
        }
        self.textcolors = {
            "normal": pygame.Color(0,0,0),
            "hover": pygame.Color(0,0,0),
            "pressed": pygame.Color(250, 250, 250),
        }
        self.pressed = False
        self.buttonsurface = pygame.Surface((self.width, self.height))
        self.buttonrect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = pygame.font.SysFont("comic sans ms", 24 )
        self.textsurface = self.font.render(self.text, True, self.textcolors["normal"])

    def update(self, screen):
        mousepos = pygame.mouse.get_pos()
        self.buttonsurface.fill(self.fillcolors ['normal'])
        if self.buttonrect.collidepoint(mousepos):
            self.buttonsurface.fill(self.fillcolors ['hover'])
            if pygame.mouse.get_pressed()[0]:
                self.buttonsurface.fill(self.fillcolors['pressed'])
                if not self.pressed:
                    self.onclick()
            else:
                self.pressed = False
        self.buttonsurface.blit(self.textsurface,(self.buttonrect.width/2-self.textsurface.get_rect().width/2,self.buttonrect.height/2-self.textsurface.get_rect().height/2))
        screen.blit(self.buttonsurface,self.buttonrect)


    ## Written by evan