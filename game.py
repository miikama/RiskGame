
import pygame
import os
import random
import variables as var
import buttons as but
import areas
import time as t

pygame.init()


time = pygame.time.Clock()

 
         
class Game:
    def __init__(self, player_count):
        self.turn = 0
        self.players = []
        self.game_display = pygame.display.set_mode(var.resolution, pygame.HWSURFACE)
        pygame.display.set_caption("Risk")        
        for i in range(player_count):
            self.players.append(areas.Player(self, i)) 
        
        menu_back = pygame.image.load("menukuvat/menumap.png").convert()
        self.menu_back = pygame.transform.scale(menu_back, (var.gameWidth, var.gameHeight))
        self.game_display.blit(self.menu_back, (0,0))
        
        pygame.mixer.music.load("music/emergence_menu.wav")
        pygame.mixer.music.play(loops=-1)
        
        load_progress = 0
        load_button = but.Button(self, int(var.gameWidth/2), int(var.gameHeight/2),
                                 "Loading " + str(load_progress) + " %",
                                 "menukuvat/nonvisible.png", 150,60, color=(100,150,100))
        
        
        t1 = t.time()
        load_button.draw()
        pygame.display.update()
        
        #some state variables
        file_names = []                   
        self.territories = []
        #first the names of the pictures and then load the pictures
        file_names.extend(["karttapalat/" + name for name in os.listdir("karttapalat/")])  
        for i in range(len(file_names)):
            picture = pygame.image.load("karttapalat/" + file_names[i].split("/")[-1]).convert_alpha()
            picture = pygame.transform.scale(picture, (var.gameWidth, var.gameHeight)) 
            mask = pygame.mask.from_surface(picture, 127)      
            self.territories.append(areas.Territory(0,0, i, mask, self))
            if (self.territories[-1].territory_number +1) % 10 == 0:
                load_progress += 25
                load_button.update("Loading " + str(load_progress) + " %")
                self.game_display.blit(self.menu_back, (0,0))                
                load_button.draw()
                pygame.display.update(load_button.rect)   

        print(t.time() - t1)        
                   
        self.selected_territory = None  
        self.selected_enemy = None
        self.start_phase = True  
        self.reinforcement_phase = False     
    
    #makes the argument territory selected and all others unselected
    def selectTerritory(self, territory):
        
        if self.start_phase:
            if territory.owner == None or territory.owner == self.players[self.turn]:
                self.territories[territory.territory_number].selectTerritory()
                self.selected_territory = territory
                for i in self.territories:
                    if i.territory_number == territory.territory_number:
                        continue
                    else:
                        i.unselectTerritory()
        
        elif self.reinforcement_phase:            
            if territory.owner == self.players[self.turn]:
                self.territories[territory.territory_number].selectTerritory()
                self.selected_territory = territory
                for i in self.territories:
                    if i.territory_number == territory.territory_number:
                        continue
                    else:
                        i.unselectTerritory()               
                max_troops = self.players[self.turn].troops
                
                
                added_troops = self.questions.ask(0, max_troops)
                self.selected_territory.addTroops(added_troops)  
                if self.players[self.turn].troops == 0:
                    self.reinforcement_phase = False              
                
             
        else:
            if territory.owner.number == self.turn:    
                self.territories[territory.territory_number].selectTerritory()
                self.selected_territory = territory
                for i in self.territories:
                    if i.owner.number == self.turn:
                        if i.territory_number == territory.territory_number:
                            continue
                        else:
                            i.unselectTerritory()
            else:
                self.territories[territory.territory_number].selectEnemy()
                self.selected_enemy = territory 
                for i in self.territories:
                    if i.owner.number != self.turn:
                        if i.territory_number == territory.territory_number:
                            continue
                        else:
                            i.unselectEnemy()
                  
        
    def endTurn(self):
        if self.freeTerritories():
            if self.selected_territory != None:
                self.selected_territory.swapOwner()
                self.selected_territory.addTroops(1)
                self.selected_territory = None
                self.selected_enemy = None
                self.turn = (self.turn +  1) % len(self.players)        
                self.whose_turn_button.update("Player " +  str(self.turn +1) )
        elif self.start_phase:           
            if self.selected_territory != None:
                self.selected_territory.addTroops(1)
            
                if self.troopsUndeplyed() == 0:
                    self.start_phase = False
                    
                self.selected_territory = None
                self.selected_enemy = None

                for i in self.territories:
                    i.unselectTerritory()
                    i.unselectEnemy()
                    
                self.turn = (self.turn +  1) % len(self.players)        
                self.whose_turn_button.update("Player " +  str(self.turn +1) )
                
                if self.start_phase == False:
                    self.reinforcement_phase = True
                    self.beginTurn()
        else:  
            self.randomDeploy()
            self.turn = (self.turn +  1) % len(self.players)        
            self.whose_turn_button.update("Player " +  str(self.turn +1) )
            self.reinforcement_phase = True
            self.selected_territory = None
            self.selected_enemy = None
            for i in self.territories:
                i.unselectTerritory()
                i.unselectEnemy()                
            self.beginTurn()   

    #@return true if there exists a territory without a owner, False otherwise    
    def freeTerritories(self):
        for i in self.territories:
            if i.owner == None:
                return True       
        return False
    
    #adds attack button to buttons called @endturn
    def toggleAttack(self, visible):
        def f(x): return x.text != "Attack"        
        self.buttons= list(filter(f, self.buttons))
        if visible: 
            self.buttons.append(self.attack_button)
    
    def attackVisible(self):
        if self.selected_enemy != None and self.selected_territory != None:
            if self.selected_territory.attackable(self.selected_enemy):
                return True
        return False
    
    #Amount of troops not deployed
    def troopsUndeplyed(self):
        count = 0
        for i in self.players:
            count += i.troops
        return count
    
    #called once the turn ends and is used to deploy all the undeployed troops evenly
    def randomDeploy(self):
        troops_todeploy = self.players[self.turn].troops
        i = 0
        while troops_todeploy != 0:
            if self.territories[i].owner == self.players[self.turn]:
                self.territories[i].addTroops(1)
                troops_todeploy -= 1
            i = (i+1) % len(self.territories)
    
    def attack(self):
  
   
        if self.selected_territory != None and self.selected_enemy != None:
            if self.selected_territory.soldiers > 1 and self.selected_territory.attackable(self.selected_enemy):            
                attacking_troops = self.selected_territory.soldiers -1
                defending_troops = self.selected_enemy.soldiers
                defending_numbers = []
                attacking_numbers = []
                
                while True:
                    defending_numbers = list(range(defending_troops)[:2])
                    attacking_numbers = list(range(attacking_troops)[:3])
                    for i in range(len(defending_numbers)): defending_numbers[i] = random.randint(1,6)
                    for i in range(len(attacking_numbers)): attacking_numbers[i] = random.randint(1,6)
                    defending_numbers.sort()
                    attacking_numbers.sort()
                    
                    if defending_numbers.pop() >= attacking_numbers.pop():
                        attacking_troops -= 1
                        self.selected_territory.takeTroops(1)
                    else:
                        defending_troops -= 1
                        self.selected_enemy.takeTroops(1)
                    if defending_troops == 0:
                        self.selected_enemy.swapOwner()
                        self.selected_enemy.transportFrom(self.selected_territory, 1)
                        transported_troops = self.questions.ask(0, attacking_troops -1, )
                        self.selected_enemy.transportFrom(self.selected_territory, transported_troops)
                        break
                    if attacking_troops == 0:
                        break
                    if len(attacking_numbers) == 0 or len(defending_numbers) == 0:
                        continue
                    if defending_numbers.pop() >= attacking_numbers.pop():
                        attacking_troops -= 1
                        self.selected_territory.takeTroops(1)
                    else:
                        defending_troops -= 1
                        self.selected_enemy.takeTroops(1)
                    if defending_troops == 0:
                        self.selected_enemy.swapOwner()
                        self.selected_enemy.transportFrom(self.selected_territory, 1)
                        transported_troops = self.questions.ask(0, attacking_troops -1, )
                        self.selected_enemy.transportFrom(self.selected_territory, transported_troops)                        
                        break
                    if attacking_troops == 0:
                        break
    
        
                
    
    def isVictory(self):
        if not self.start_phase:
            owner = self.territories[0].owner.number
            for i in self.territories:
                if i.owner.number != owner:
                    return None
            self.displayVictory()
        
    
    def displayVictory(self):
        winner = self.territories[0].owner
        quit_notice = but.Button(self, int(var.gameWidth/2), int(var.gameHeight/2), 
                                "Player " + str(winner.number + 1) + " wins!",
                                "menukuvat/nonvisible.png", 150, 60)
        quit_notice.draw()
        pygame.display.update()
        
        while 1:
            for event in pygame.event.get():                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()           
                
    #for testing to fill the territories
    def playStart(self):
        j = 0
        for i in self.territories:
            self.turn = j
            self.selected_territory = i
            self.selected_territory.swapOwner()
            self.selected_territory.addTroops(1)#self.selected_territory.territory_number )
            j = (j+1) % len(self.players)
        self.selected_territory = None
        self.turn = j
        self.whose_turn_button.update("Player " +  str(self.turn +1) )
                      
        
    def menu(self):
        in_menu = True
        
        
        
        buttons = but.Button(self, int(var.gameWidth/2), int(var.gameHeight/2),"Play",  "menukuvat/menubutton.png", 120, 60)
        self.game_display.blit(self.menu_back, (0,0))
        buttons.draw()
        pygame.display.update()
        
        
        
        while in_menu:
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()   
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        buttons.click()
                        
            buttons.draw()
            
        
        
            pygame.display.update()
            time.tick(var.FPS)
    
    #called at the end of ending turn for the next player. 
    #Counts how many troops a player receives and add them to the player soldiers
    def beginTurn(self):
    
        self.reinforcement_phase = True
        gained_troops = int(len(self.players[self.turn].territories)/3)
        if gained_troops < 3:
            gained_troops = 3
        
        continent = self.players[self.turn].continentTroops()
        gained_troops += continent  
              
        self.players[self.turn].gainTroops(gained_troops)
        
        
    def gameLoop(self): 
        
        pygame.mixer.music.fadeout(2000)
        
        #making the buttons and a button list        
        self.whose_turn_button = but.Button(self, int(var.gameWidth/2), 30, "Player " +  str(self.turn +1) ,  "menukuvat/ylapaneeli.png", 300, 60)
        self.next_turn_button = but.Button(self, int(var.gameWidth-80), int(var.gameHeight - 50),  "End turn" ,  "menukuvat/menubutton.png", 120, 60)
        self.attack_button = but.Button(self, int(var.gameWidth-220), int(var.gameHeight-50), "Attack", "menukuvat/menubutton.png", 120,60)
        self.deployable_button = but.Button(self, 120, int(var.gameHeight-50), "Troops left: " + str(0), "menukuvat/menubutton.png", 200, 60)
        self.buttons = [self.whose_turn_button, self.next_turn_button, self.deployable_button]
        
        self.questions = but.QuestionBox(self, var.gameWidth/2, var.gameHeight-50, 0, 5)
            
        self.game_display.fill(var.ocean_color)
        areas = pygame.image.load("menukuvat/areas.png").convert_alpha()
        self.areas = pygame.transform.scale(areas, (var.gameWidth, var.gameHeight)) 
        self.game_display.blit(self.areas, (0,0))
            
        
        self.playStart()
      
       
        while 1:
            
            #checking to see if the game ends
            self.isVictory()
            self.game_display.fill(var.ocean_color)
            self.game_display.blit(self.areas, (0,0)) 

            #checking clicks on the buttons and other events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        for i in self.buttons:
                            i.click()
                        for i in self.territories:
                            i.click() 
                            
              
                 
            for i in self.territories: 
                i.hover()                
                i.draw_territory()
               
                
            if self.attackVisible():
                self.toggleAttack(True)
            else: self.toggleAttack(False) 
                
            self.deployable_button.update("Troops left: " + str(self.players[self.turn].troops))
            for i in self.buttons:
                i.draw()
               
                
            pygame.display.update()
            time.tick(var.FPS)
            
        



#creating the game object and starting the game with two players
mygame = Game(2)
mygame.menu()





