import pygame
import os, random, sys
from build_up import MyPoint, camp, dining_hall, class_room, adom_room
from util import infection_num
import numpy as np

pygame.init()

# Basic Color
BLACK = pygame.Color(0,0,0)#0,0,0
WHITE = pygame.Color(255,255, 255)#255,255,255
RED = pygame.Color(255, 0, 0)#255, 0, 0
GREEN = pygame.Color(0,140, 0)#0, 255, 0
BLUE = pygame.Color(0,0, 255)#0, 0, 255
YELLOW = pygame.Color(255, 200, 0)
GREY = pygame.Color(150,150, 150)

BASICFONT = pygame.font.SysFont('SIMYOU.TTF', 28)

# WIDTH, HEIGHT = 1000, 480
WIDTH, HEIGHT = 1400, 700
FPS = 50

screen_main = pygame.display.set_mode((WIDTH, HEIGHT),  pygame.DOUBLEBUF)
clock = pygame.time.Clock()
pygame.display.set_caption('GAME')
#=======================================================
type_l = [RED, YELLOW, GREEN]
ratio_l = [0.8, 0.5, 0.4, 0.1] 
infect_num_l = [3, 3, 3, 3]
#======================================================
def drawName(building):
    score_Surf = BASICFONT.render('{0}'.format(building.name()), True, GREY)
    score_Rect = score_Surf.get_rect()
    score_Rect.midtop = (building.main_position())

    screen_main.blit(score_Surf, score_Rect)

#========================================================


#  =============  generate person ==================
person_l = []

for i in range(150):
    if i%30 == 0:
        coord = (random.randint(1,1000), random.randint(2, 480))
        person_l.append(
            MyPoint( i//3,0, screen_main, coord, 2 , type_l)
        )
    else:
        coord = (random.randint(1,1000), random.randint(2, 480))
        person_l.append(
            MyPoint( i//3,2, screen_main, coord, 2 , type_l)
        )        

# ========= build =================================
Camp = camp(screen_main, (750,90), (180,300))

Dining_Hall = dining_hall(screen_main, (500, 240), 60)

Class_room_l = []
for i in range(2):
    Class_room_l.append(
        class_room(screen_main, (340,60+i*240),(75, 120))
    )
    Class_room_l.append(
        class_room(screen_main, (580,60+i*240),(75, 120))
    )

adom = adom_room(screen_main, (20,40), 40)
# ============ build ====================================

# ============ action ===================================
#---------------- back adom ------------------------------------------
def back_adom():
    for per in person_l:
        per.disp()
    position_l = adom.get_coord()
    for per in person_l:
        per.back_adom(position_l)

#----------------- eat --------------------------
def go_to_eat():
    for per in person_l:
        per.disp()
    position = Dining_Hall.get_coord()
    for per in person_l:
        per.go_dining(position)

#---------------- class --------------------
index_list = np.random.randint(0,4, size=150)
l_class_posi = []
l_class_infection_num = [0,0,0,0]
for i in Class_room_l:
    l_class_posi.append(
        i.get_coord()
    )
def go_to_class(frame_num):
    for per in person_l:
        per.disp()
    if frame_num == 202:
        print('Count!')
        for i in  range(len(person_l)):
            per = person_l[i]
            l_class_infection_num[index_list[i]] = infection_num(l_class_infection_num[index_list[i]], per)
        
    for i in  range(len(person_l)):
        per = person_l[i]
        posi = l_class_posi[index_list[i]]
        per.go_class(posi)
        per.evolve(
            1,
            ratio_l,
            infect_num_l,
            l_class_infection_num[index_list[i]]
        )

#----------------- play -----------------------------------
def go_to_play():
    for per in person_l:
        per.disp()
    position = Camp.get_coord()
    for per in person_l:
        per.go_to_play(position)


#============================================================
frame_num = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen_main.fill(WHITE)

    Dining_Hall.disp()
    drawName(Dining_Hall)
    for c in Class_room_l:
        c.disp()
        drawName(c)
    Camp.disp()
    drawName(Camp)
    adom.disp()
    drawName(adom)

    if frame_num > 0 and frame_num <201:
        back_adom()
    elif frame_num >200 and frame_num < 401:
        go_to_class(frame_num)
    elif frame_num > 400 and frame_num <601:
        go_to_eat()
    elif frame_num > 600 and frame_num <801:
        go_to_play()
    elif frame_num > 800 and frame_num <1000:
        back_adom()
    else:
        frame_num = 0


    pygame.display.update()
    frame_num += 1
    time_passed = clock.tick(FPS)
