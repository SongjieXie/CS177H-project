import pygame
import os, random, sys
from build_up import MyPoint, camp, dining_hall, class_room, adom_room, drawName
from util import infection_num, count_total_SIR
from mat_plot import plot_line
from input_box import InputBox
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
WIDTH, HEIGHT = 1300, 700
FPS = 50

screen_main = pygame.display.set_mode((WIDTH, HEIGHT),  pygame.DOUBLEBUF)
clock = pygame.time.Clock()
pygame.display.set_caption('GAME')

#=======================================================
type_l = [RED, YELLOW, GREEN]
para_1 = [0.8, 0.5, 0.4, 0.1] 
para_1_labels = ['Adom Ratio', 'Cateen Ratio', 'Classroom Ratio', 'Camp Ratio']
para_2 = [3, 3, 3, 3]

# =============  generate person ==================
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

# ============== Input ===================================
para_1_boxes_l = []
para_2_boxes =None

for i in range(len(para_1)):
    box = InputBox(1100, 100 + 50*i, 70, 32, text=str(para_1[i]), label=para_1_labels[i])
    para_1_boxes_l.append(box)

para_2_boxes = InputBox(1100, 100 + 50*3+70, 70, 32, text=str(3), label='Infection num:')

def Boxing():
    for b in para_1_boxes_l:
        b.update()
    para_2_boxes.update()

    for b in para_1_boxes_l:
        b.draw(screen_main)
    para_2_boxes.draw(screen_main)

    p1 = []
    p2 = []
    for b in para_1_boxes_l:
        p1.append(b.get_value())
        p2.append(para_2_boxes.get_value())
    
    return p1, p2



# ============ action ===================================
#---------------- back adom ------------------------------------------
l_adom_infection_num = [0]*50
def back_adom(frame_num, day_num, ratio_l, infect_num_l):
    for per in person_l:
        per.disp()
        per.load_time(day_num)
    position_l = adom.get_coord()
    if frame_num%200 == 0:
        for  i in range(len(l_adom_infection_num)):
            l_adom_infection_num[i] =0
        for i in  range(len(person_l)):
            per = person_l[i]
            l_adom_infection_num[per.adom] = infection_num(l_adom_infection_num[per.adom], per)
        print(l_adom_infection_num)

    for per in person_l:
        per.back_adom(position_l)
        per.evolve(
            0,
            ratio_l,
            infect_num_l,
            l_adom_infection_num[per.adom],
            transition_time = 3,
            total=3
        )

#----------------- eat --------------------------
dining_infection_num = [0]
def go_to_eat(frame_num, day_num, ratio_l, infect_num_l):
    for per in person_l:
        per.disp()
        per.load_time(day_num)
    #count
    if frame_num%200 == 1:
        for i in range(len(dining_infection_num)):
            dining_infection_num[0] = 0
        for i in  range(len(person_l)):
            per = person_l[i]
            dining_infection_num[0] = infection_num(dining_infection_num[0], per)
        print(dining_infection_num[0]) 
    position = Dining_Hall.get_coord()
    for per in person_l:
        per.go_dining(position)
        per.evolve(
            2,
            ratio_l,
            infect_num_l,
            dining_infection_num[0],
            transition_time = 3,
            total= 150
        )

#---------------- class --------------------
index_list = np.random.randint(0,4, size=150)
l_class_posi = []
l_class_infection_num = [0,0,0,0]
for i in Class_room_l:
    l_class_posi.append(
        i.get_coord()
    )
def go_to_class(frame_num, day_num, ratio_l, infect_num_l):
    for per in person_l:
        per.disp()
        per.load_time(day_num)
    # Count infection num just once!
    if frame_num == 202:
        for i in range(len(l_class_infection_num)):
            l_class_infection_num[i] = 0
        for i in  range(len(person_l)):
            per = person_l[i]
            l_class_infection_num[index_list[i]] = infection_num(l_class_infection_num[index_list[i]], per)
        print(l_class_infection_num)
        
    for i in  range(len(person_l)):
        per = person_l[i]
        posi = l_class_posi[index_list[i]]
        per.go_class(posi)
        per.evolve(
            1,
            ratio_l,
            infect_num_l,
            l_class_infection_num[index_list[i]],
            transition_time = 3,
            total= 40
        )

#----------------- play -----------------------------------
play_infection_num = [0]
def go_to_play(frame_num, day_num, ratio_l, infect_num_l):
    for per in person_l:
        per.disp()
        per.load_time(day_num)
    position = Camp.get_coord()
    #count
    if frame_num%200 ==0:
        for i in range(len(play_infection_num)):
            play_infection_num[i] = 0
        for i in  range(len(person_l)):
            per = person_l[i]
            play_infection_num[0] = infection_num(play_infection_num[0], per)
        print(play_infection_num[0])

    for per in person_l:
        per.go_to_play(position)
        per.evolve(
            3,
            ratio_l,
            infect_num_l,
            play_infection_num[0],
            transition_time = 3,
            total= 150
        )

# ================= main loop =================================
def main_loop(frame_num, day_num, ratio_l, infect_num_l):
    if frame_num >= 0 and frame_num <201:
        back_adom(frame_num, day_num, ratio_l, infect_num_l)
    elif frame_num >200 and frame_num < 401:
        go_to_class(frame_num, day_num, ratio_l, infect_num_l)
    elif frame_num > 400 and frame_num <601:
        go_to_eat(frame_num, day_num, ratio_l, infect_num_l)
    elif frame_num > 600 and frame_num <801:
        go_to_play(frame_num, day_num, ratio_l, infect_num_l)
    elif frame_num > 800 and frame_num <1001:
        back_adom(frame_num, day_num, ratio_l, infect_num_l)
    else:
        print('The day {0} passed'.format(day_num))


#============================================================
frame_num = 0
day_num =0
Mycountor = count_total_SIR()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        for box in para_1_boxes_l:
            box.handle_event(event)
        para_2_boxes.handle_event(event)

    screen_main.fill(WHITE)

    #Draw buildings
    Dining_Hall.disp()
    drawName(Dining_Hall, screen_main)
    for c in Class_room_l:
        c.disp()
        drawName(c, screen_main)
    Camp.disp()
    drawName(Camp, screen_main)
    adom.disp()
    drawName(adom, screen_main)

    # Draw input 
    p1, p2 = Boxing()

    # Activate actions
    main_loop(frame_num, day_num, p1, p2)

    if frame_num > 1000:
        frame_num = 0
        day_num += 1
        print(day_num)

    #Plot counting chart
    Mycountor.update(person_l)
    data = Mycountor()
    raw_data, size = plot_line(data)
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen_main.blit(surf, (20,440))


    pygame.display.update()
    frame_num += 1
    time_passed = clock.tick(FPS)
