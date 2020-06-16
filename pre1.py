import pygame
import os, random, sys
from build_up import MyPoint, camp, dining_hall, class_room, adom_room, drawName
from util import infection_num, count_total_SIR, init_infect, recorder
from mat_plot import plot_line, plot_hist
from input_box import InputBox, ButtonBox
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
para_1_labels = ['Dormitory:', 'Canteen:', 'Classroom:', 'Playground:']
para_2 = [2, 3, 3, 3]
para_3_labels = ['Incfection:', 'Incuation:']
para_3 = [2,3]

# =============  generate person ==================
def generate_persons():
    person_l = []
    for i in range(150):
        if i%30 == 0:
            coord = (random.randint(1,1000), random.randint(2, 480))
            person_l.append(
                MyPoint( i//3,2, screen_main, coord, 2 , type_l)
            )
        else:
            coord = (random.randint(1,1000), random.randint(2, 480))
            person_l.append(
                MyPoint( i//3,2, screen_main, coord, 2 , type_l)
            )  
    return person_l      

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
para_2_boxes_l = []
button_box = None
para_3_boxes_l = []
reset_button_box = None

button_box = ButtonBox(1200, 400)
reset_button_box = ButtonBox(1200, 300, str1='RESET', str2='RESET')

for i in range(len(para_1)):
    box = InputBox(1100, 100 + 50*i, 70, 32, text=str(para_1[i]), label=para_1_labels[i])
    para_1_boxes_l.append(box)
    box2 = InputBox(1100+80, 100 + 50*i, 70, 32, text=str(para_2[i]), label=para_1_labels[i], draw_label=False)
    para_2_boxes_l.append(box2)

for i in range(len(para_3)):
    box3 = InputBox(1100, 350 + 50*i, 70, 32, text=str(para_3[i]), label=para_3_labels[i])
    para_3_boxes_l.append(box3)


def Boxing():

    for b in para_1_boxes_l:
        b.update()
    for b in para_2_boxes_l:
        b.update()
    for b in para_3_boxes_l:
        b.update()

    for b in para_1_boxes_l:
        b.draw(screen_main)
    for b in para_2_boxes_l:
        b.draw(screen_main)
    for b in para_3_boxes_l:
        b.draw(screen_main)

    button_box.draw(screen_main)
    reset_button_box.draw(screen_main)

    p1 = []
    p2 = []
    p3 = []
    for b in para_1_boxes_l:
        p1.append(b.get_value())
    for b in para_2_boxes_l:
        p2.append(b.get_value())
    for b in para_3_boxes_l:
        p3.append(b.get_value())
    
    return p1, p2, p3



# ============ action ===================================
#---------------- back adom ------------------------------------------
l_adom_infection_num = [0]*50
l_adom_infection_num2 = [0]*50
def back_adom(frame_num, day_num, ratio_l, infect_num_l, person_l):
    for per in person_l:
        per.disp()
        per.load_time(day_num)
    position_l = adom.get_coord()
    if frame_num%200 == 2:
        for  i in range(len(l_adom_infection_num)):
            l_adom_infection_num[i] =0
        for i in  range(len(person_l)):
            per = person_l[i]
            l_adom_infection_num[per.adom] = infection_num(l_adom_infection_num[per.adom], per)
        # print(l_adom_infection_num)
    for  i in range(len(l_adom_infection_num2)):
        l_adom_infection_num2[i] =0
    for i in  range(len(person_l)):
        per = person_l[i]
        l_adom_infection_num2[per.adom] = infection_num(l_adom_infection_num2[per.adom], per)

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
    return sum(l_adom_infection_num2)

#----------------- eat --------------------------
dining_infection_num = [0]
dining_infection_num2 = [0]
def go_to_eat(frame_num, day_num, ratio_l, infect_num_l, person_l):
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
    for i in range(len(dining_infection_num2)):
        dining_infection_num2[0] = 0
    for i in  range(len(person_l)):
        per = person_l[i]
        dining_infection_num2[0] = infection_num(dining_infection_num2[0], per)

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
    return dining_infection_num2[0]
    

#---------------- class --------------------
index_list = np.random.randint(0,4, size=150)
l_class_posi = []
l_class_infection_num = [0,0,0,0]
l_class_infection_num2 = [0,0,0,0]
for i in Class_room_l:
    l_class_posi.append(
        i.get_coord()
    )
def go_to_class(frame_num, day_num, ratio_l, infect_num_l, person_l):
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
        
    for i in range(len(l_class_infection_num2)):
        l_class_infection_num2[i] = 0
    for i in  range(len(person_l)):
        per = person_l[i]
        l_class_infection_num2[index_list[i]] = infection_num(l_class_infection_num2[index_list[i]], per)

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
    return sum(l_class_infection_num2)

#----------------- play -----------------------------------
play_infection_num = [0]
play_infection_num2 = [0]
def go_to_play(frame_num, day_num, ratio_l, infect_num_l, person_l):
    for per in person_l:
        per.disp()
        per.load_time(day_num)
    position = Camp.get_coord()
    #count
    if frame_num%200 ==2:
        for i in range(len(play_infection_num)):
            play_infection_num[i] = 0
        for i in  range(len(person_l)):
            per = person_l[i]
            play_infection_num[0] = infection_num(play_infection_num[0], per)
        print(play_infection_num[0])
    for i in range(len(play_infection_num2)):
        play_infection_num2[i] = 0
    for i in  range(len(person_l)):
        per = person_l[i]
        play_infection_num2[0] = infection_num(play_infection_num2[0], per)

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
    return play_infection_num2[0]

# ================= main loop =================================
def main_loop(frame_num, day_num, ratio_l, infect_num_l, person_l, new_num, data2):
    if frame_num >= 0 and frame_num <201:
        num = back_adom(frame_num, day_num, ratio_l, infect_num_l, person_l)
        data2[0] += num-new_num
    elif frame_num >200 and frame_num < 401:
        num = go_to_class(frame_num, day_num, ratio_l, infect_num_l, person_l)
        data2[1] += num-new_num
    elif frame_num > 400 and frame_num <601:
        num = go_to_eat(frame_num, day_num, ratio_l, infect_num_l, person_l)
        data2[2] += num-new_num
    elif frame_num > 600 and frame_num <801:
        num = go_to_play(frame_num, day_num, ratio_l, infect_num_l, person_l)
        data2[3] += num-new_num
    elif frame_num > 800 and frame_num <1001:
        num = back_adom(frame_num, day_num, ratio_l, infect_num_l, person_l)
        data2[0] += num-new_num
    else:
        print('The day {0} passed'.format(day_num))

    return num


#============================================================
frame_num = 0
frame_num_countor = 0
day_num =0
Mycountor = count_total_SIR()
Run_flag = False
data2 = [0,0,0,0]
init_num = 0
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        for box in para_1_boxes_l:
            box.handle_event(event)
        for box in para_2_boxes_l:
            box.handle_event(event)
        for box in para_3_boxes_l:
            box.handle_event(event)
        button_box.handle_event(event)
        reset_button_box.handle_event(event)

        Run_flag = button_box.get_flag()
        Reset_flag = reset_button_box.get_flag()


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
    p1, p2, p3= Boxing()

    # Activate actions
    if Run_flag:
        if frame_num_countor == 0:
            reco = recorder()
            reco.write_params(p1, p2, p3 )
            person_l = generate_persons()
            init_infect(person_l, int(p3[0]), int(p3[1]))
            init_num = sum([int(p3[0]), int(p3[1])])
        init_num = main_loop(frame_num, day_num, p1, p2, person_l, init_num, data2)
        Mycountor.update(person_l)
        reco.write_frame(day_num, frame_num, Mycountor(), data2)
        frame_num += 1
        frame_num_countor += 1

    if frame_num > 1000:
        frame_num = 0
        day_num += 1
        print(day_num)

    # Reset
    if Reset_flag:
        reco.close_file()
        frame_num_countor = 0
        frame_num = 0
        Mycountor.reset()
        data2 = [0,0,0,0]
    Reset_flag = False

    #Plot counting chart
    
    data = Mycountor()
    raw_data, size = plot_line(frame_num_countor, data)
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen_main.blit(surf, (20,440))


    raw_data2, size2 = plot_hist(data2)
    surf = pygame.image.fromstring(raw_data2, size2, "RGB")
    screen_main.blit(surf, (420,440))
    ########
    pygame.display.update()
    time_passed = clock.tick(FPS)
