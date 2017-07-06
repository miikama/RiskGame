import pygame
import variables as var
import buttons as but
from pygame.surface import Surface
import time
      
                
class Territory:
    def __init__(self, x, y, number, mask, game):
        self.owner = None  
        self.selected = False 
        self.selected_enemy = False
        self.game = game
        self.display = game.game_display
        self.x = x 
        self.y = y 
        self.soldiers = 0         
        self.territory_number = number
        self.lighted = False
        self.mask = mask
        self.mask_center = self.mask.centroid()        
        self.test_surf = None
        
        self.light_surfaces = []
        self.light_width = int(var.gameWidth/6)
        self.light_height = int(var.gameHeight/3)        
        self.offset = int(self.mask_center[0] - self.light_width/2), int(self.mask_center[1] - self.light_height/2)
        
        
        for color in var.player_colors:
            self.test_surf = Surface((self.light_width, self.light_height), pygame.HWSURFACE )
            self.test_surf.get_rect().center = self.mask.centroid()
            self.test_surf.set_alpha(128)
            self.test_surf.set_colorkey(var.black)                    
            for i in range(self.light_width):
                for j in range(self.light_height):
                    if i + self.offset[0] <0 or j + self.offset[1] < 0:
                        continue 
                    if self.mask.get_at((i + self.offset[0],j + self.offset[1])) != 0:
                        self.test_surf.set_at((i, j), color)
            self.light_surfaces.append(self.test_surf)
        
        
        self.circle = None  
        self.color_buttons = []  
           
        self.color_buttons.append(but.Button(game, self.mask.centroid()[0],
                             self.mask.centroid()[1], str(self.soldiers), "menukuvat/sininenympyra.png" ,
                              int(var.widthFactor*50), int(var.widthFactor* 50), var.smallfont))
        self.color_buttons.append(but.Button(game, self.mask.centroid()[0],
                             self.mask.centroid()[1], str(self.soldiers), "menukuvat/punainenympyra.png" ,
                              int(var.widthFactor*50), int(var.widthFactor* 50), var.smallfont))
        self.color_buttons.append(but.Button(game, self.mask.centroid()[0],
                             self.mask.centroid()[1], str(self.soldiers), "menukuvat/harmaaympyra.png" ,
                              int(var.widthFactor*50), int(var.widthFactor* 50), var.smallfont))
        
        self.circle = self.color_buttons[-1]
        
            
    #draws this territory    
    def draw_territory(self):
        if self.lighted:          
            if self.owner == None:
                self.game.game_display.blit(self.light_surfaces[-1], self.offset)
            else:
                self.game.game_display.blit(self.light_surfaces[self.owner.number], self.offset)                                         
        self.circle.draw()
       
        
    def hover(self):
        pos = pygame.mouse.get_pos()        
        if self.mask.get_at(pos):               
            self.lighted = True            
        else:
            if self.selected or self.selected_enemy: self.lighted = True                
            else: self.lighted = False
            
            
    #defines what happens when clicked, also determines if the click is on the territory
    def click(self):
        pos = pygame.mouse.get_pos()
        offset = (pos[0],pos[1])
        if self.mask.get_at(offset):                                           
            self.game.selectTerritory(self)    
   
    #changes the owner of this territory to a current player
    def swapOwner(self):
        if self.owner != None:
            self.owner.loseTerritory(self)
        self.owner = self.game.players[self.game.turn]
        self.circle = self.color_buttons[self.owner.number]
        self.owner.territories.append(self)
        self.unselectEnemy()
        
              
    def selectEnemy(self):
        self.selected_enemy = True
         
    def unselectEnemy(self):
        self.selected_enemy = False
         
    def selectTerritory(self):
        self.selected = True
        self.lighted = True
        
    def unselectTerritory(self):
        self.selected = False
        self.lighted = False
    
    def addTroops(self, count):
        self.soldiers += self.owner.deploy(count)
        self.circle.update(str(self.soldiers)) 
        
    def takeTroops(self, count):
        self.soldiers -= count
        self.circle.update(str(self.soldiers)) 
        
    def transportFrom(self, territory, number):
        self.soldiers += number
        territory.soldiers -= number
        self.circle.update(str(self.soldiers))
        territory.circle.update(str(territory.soldiers))
    
    def nextTo(self, territory):      
        if self.mask.overlap(territory.mask, (0,0)) != None:
            return True
        else: return False
        
    def attackable(self, territory):
        list = var.attack_list[self.territory_number]        
        if list.count(territory.territory_number)>0:
            return True
        else: return False
        
        
###########################################################################    
 
class Player:
    def __init__(self, game, number): 
        self.territories = []
        self.number = number
        self.troops = var.start_troops
                  
    def gainTroops(self, number):
        self.troops += number
         
    def gainTerritory(self, territory):
        self.territories.append(territory)
    
    def loseTerritory(self, territory):    
        def f(x): return x.territory_number != territory.territory_number        
        self.territories = list(filter(f, self.territories))       
            
    def deploy(self, count):
        if count > self.troops:
            self.troops = 0
            return self.troops
        else:
            self.troops -= count
            return count
        
    def continentTroops(self):
        numbers = [x.territory_number  for x in self.territories]
        numbers.sort(key=None, reverse=False)
        troops = 0
        
        def contain(list):
            for i in list:
                if numbers.count(i)> 0:
                    continue
                else: 
                    return False
            return True    
        
        if contain(var.namerica):
            troops += 5
        if contain(var.samerica):
            troops += 2
        if contain(var.africa):
            troops += 3
        if contain(var.europe):
            troops += 5
        if contain(var.australia):
            troops += 2
        if contain(var.asia):
            troops += 7
        return troops
        
       
            