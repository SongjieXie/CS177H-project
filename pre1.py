import pygame
import os, random, sys
from build_up import MyPoint, camp, dining_hall, class_room, adom_room
import numpy as np

# Basic Color
BLACK = 0,0,0
WHITE = 255,255,255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255

# WIDTH, HEIGHT = 1000, 480
WIDTH, HEIGHT = 1400, 700
FPS = 50

screen_main = pygame.display.set_mode((WIDTH, HEIGHT),  pygame.DOUBLEBUF)
clock = pygame.time.Clock()
pygame.display.set_caption('GAME')



#=======================================================

#========================================================


#  =============  generate person ==================
person_l = []

for i in range(150):
    coord = (random.randint(1,1000), random.randint(2, 480))
    person_l.append(
        MyPoint( i//3, 1, screen_main, coord, 2 , (255, 0, 0))
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

#----------------------------------------------------------

#----------------- eat --------------------------
def go_to_eat():
    for per in person_l:
        per.disp()
    position = Dining_Hall.get_coord()
    for per in person_l:
        per.go_dining(position)
#----------------------------------

#---------------- class --------------------
index_list = np.random.randint(0,4, size=150)
l_class_posi = [] 
for i in Class_room_l:
    l_class_posi.append(
        i.get_coord()
    )
def go_to_class():
    for per in person_l:
        per.disp()
    for i in  range(len(person_l)):
        per = person_l[i]
        posi = l_class_posi[index_list[i]]
        per.go_class(posi)
#------------------------------------------------------------

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
    for c in Class_room_l:
        c.disp()

    Camp.disp()
    adom.disp()

    if frame_num > 0 and frame_num <201:
        back_adom()
    elif frame_num >200 and frame_num < 401:
        go_to_class()
    elif frame_num > 400 and frame_num <601:
        go_to_eat()
    elif frame_num > 600 and frame_num <801:
        go_to_play()
    elif frame_num > 800 and frame_num <1000:
        back_adom()
    else:
        frame_num = 0

    # back_adom()

    pygame.display.update()
    frame_num += 1
    time_passed = clock.tick(FPS)
    print(frame_num)
