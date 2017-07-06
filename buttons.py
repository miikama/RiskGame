import pygame
import variables as var

class Button:
    def __init__(self , game, x, y, text, pic, width, height, buttonfont = var.font, color = var.black):
        self.text = text
        self.font = buttonfont
        self.color = color
        self.text_surface = self.font.render(text, True, self.color)       
        self.display = game.game_display
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pic = pygame.image.load(pic).convert_alpha()
        self.pic = pygame.transform.scale(self.pic, (self.width, self.height))
        self.rect = self.text_surface.get_rect()
        self.picrect = self.pic.get_rect()  
        self.game = game
        
           
    def update(self, text):
        self.text = text
        self.text_surface = self.font.render(text, True, self.color)
        self.rect = self.text_surface.get_rect()
        
    def draw(self):
        self.picrect.center = self.x, self.y
        self.display.blit(self.pic, self.picrect)
        self.rect.center = self.x  , self.y
        self.display.blit(self.text_surface, self.rect)
            
    def click(self):

        pos = pygame.mouse.get_pos()
        if self.x - self.width/2 < pos[0] < self.x + self.width/2:
            if self.y - self.height/2 < pos[1] < self.y + self.height/2:
                if self.text == "Play": self.game.gameLoop()
                if self.text == "End turn": self.game.endTurn()
                if self.text == "Attack": self.game.attack()

                        
 
 
#############################################################################################                  
  
  
class QuestionBox:
    def __init__(self,game, x, y, low, high ):
        self.x = x
        self.y = y
        self.current_number = low
        self.low_bound = low
        self.high_bound = high
        self.game = game
        self.display = game.game_display
        self.height = 60
        self.base_width = 120
        self.arrow_width = 60
        self.leftarrow = pygame.image.load("menukuvat/leftarrow.png").convert_alpha()
        self.leftarrow = pygame.transform.scale(self.leftarrow, (self.arrow_width, self.height -2))
        
        self.rightarrow = pygame.image.load("menukuvat/rightarrow.png").convert_alpha()
        self.rightarrow = pygame.transform.scale(self.rightarrow, (self.arrow_width, self.height-2))
        self.base = Button(game, x, y, str(self.low_bound), "menukuvat/questionbase.png", self.base_width, self.height)
        self.leftmask = pygame.mask.from_surface(self.leftarrow, 100)
        self.rightmask = pygame.mask.from_surface(self.rightarrow,100)
        
    def ask(self, low, high):
        self.high_bound = high
        self.low_bound = low
        if self.high_bound == self.low_bound:
            return self.low_bound
        self.current_number = low
        self.base.update(str(self.current_number))
        while 1: 
            self.game.game_display.blit(self.game.areas, (0,0)) 
           
            for i in self.game.territories:                 
                i.draw_territory()
          
            for i in self.game.buttons:
                i.draw()
            self.draw() 

                          
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        self.click()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.current_number        
            
        
    def draw(self):
        self.base.draw()
        leftrect = self.leftarrow.get_rect()
        rightrect = self.rightarrow.get_rect()
        leftrect.center = self.x - int(self.base_width/2 + self.arrow_width/2) -1, self.y
        rightrect.center = self.x + int(self.base_width/2 + self.arrow_width/2) +1, self.y
        self.display.blit(self.rightarrow, rightrect)
        self.display.blit(self.leftarrow, leftrect)
        pygame.display.update()        
    
    def click(self):
        pos = pygame.mouse.get_pos()  
        
        left_edge = self.x - int(self.base_width/2) - self.arrow_width              
        right_edge = self.x + int(self.base_width/2)
        top = self.y - int(self.height/2)
        left_offset = int(pos[0] - left_edge), pos[1] - top
        right_offset = int(pos[0] - right_edge), pos[1] - top  
        
        if self.leftarrow.get_rect().collidepoint(left_offset):
            if self.leftmask.get_at(left_offset):
                self.reduce()
        if self.rightarrow.get_rect().collidepoint(right_offset):
            if self.rightmask.get_at(right_offset):  
                self.increment()

    def reduce(self):
        self.current_number = self.current_number -1
        if self.current_number < self.low_bound: self.current_number = self.low_bound
        self.base.update(str(self.current_number))
                                 
    def increment(self):
        self.current_number += 1
        if self.current_number > self.high_bound: self.current_number = self.high_bound
        self.base.update(str(self.current_number))
        
        
        
        
      
      
