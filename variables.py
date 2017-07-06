
import pygame

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
light_red = (255, 100,100)
yellow = (255,255,50)
light_yellow = (255,255,150)
green = (0,255,0)
blue = (0,0,255)
light_green = (102,255,102)
grey = (192, 192, 192)
brown = (153, 0, 0)
purple = (128,0,128)
ocean_color = (132,180,228)


FPS = 30
gameWidth = 1900 
gameHeight =1000

widthFactor = gameWidth/1920.0
heightFactor = gameHeight/1000.0
scale = int(widthFactor*gameWidth), int(heightFactor*gameHeight)

player_count = 2
start_troops = 21
player_colors = [blue, red, purple, ocean_color]

pygame.font.init()
font = pygame.font.SysFont("timesnewroman",30)
smallfont = pygame.font.SysFont("timesnewroman",20)
resolution = (gameWidth,gameHeight)



namerica = range(9)
samerica = range(9,13)
africa = range(13,19)
europe = range(19,26)
australia = range(26,30)
asia = range(30,42)


attack_list= {    0 : [1, 5, 39 ],
                  1 : [0, 5, 2, 8],
                  2 : [1, 3, 4, 5, 6, 8],
                  3 : [2,4,8],
                  4 : [2,3,6,7],
                  5 : [0,1,2,6],
                  6 : [2,4,5,7],
                  7 : [4,6,9],
                  8 : [1,2,3,19],
                  9 : [7,10,11],
                  10 : [9,11,12,13],
                  11 : [9,10,12],
                  12 : [10,11],
                  13 : [10,14,15,16],
                  14 : [13,15,24,30],
                  15 : [13,14,16,17,18],
                  16 : [13,15,17],
                  17 : [15,16,18],
                  18 : [15,17],
                  19 : [8,20,21],
                  20 : [19,21,22,23],
                  21 : [19,20,23,25],
                  22 : [20,23,24,13],
                  23 : [20,21,22,24,25,],
                  24 : [13,14,22,23,25,30],
                  25 : [21,23,24,30,33,34],
                  26 : [27,28,32],
                  27 : [26,28,29],
                  28 : [26,27,29],
                  29 : [27,28],
                  30 : [14,24,25,31,33],
                  31 : [30,32,33,35],
                  32 : [26,31,35],
                  33 : [25,30,31,34,35],
                  34 : [25,33,35,36],
                  35 : [31,32,33,34,36,40],
                  36 : [34,35,37,38,40],
                  37 : [36,38,39],
                  38 : [36,37,39,40],
                  39 : [0,37,38,40,41],
                  40 : [35,36,38,39,41],
                  41 : [39,40]}


#map_coordinates = [(0,0) , (383,16), (282,158), (556,151), (275,448), (0,132), (0,356), (0,590), (974,0) ]
#for i in range(len(map_coordinates)):
#    map_coordinates[i] = map_coordinates[i][0] + 1100/2, map_coordinates[i][1] + 600/2
#for i in range(len(map_coordinates)):
#    map_coordinates[i] = (int(map_coordinates[i][0]*(1100.0/4500.0)), int(map_coordinates[i][1]*(600.0/2234.0))) 
#for i in range(len(map_coordinates)):
#    map_coordinates[i] = map_coordinates[i][0] - int( 1100/2* widthFactor), map_coordinates[i][1] - int(600/2 * heightFactor)    


