import pygame
import os, random, sys, math

sign = lambda x: 1 if x >0 else (-1 if x<0 else 0)



class MyPoint():
    def __init__(self, adom, type_of, screen, coord , size, color, width=0):
        self.screen = screen

        self.adom = adom
        self.type_of = 0

        self.x = int(coord[0])
        self.y = int(coord[1])
        self.step_x = 0
        self.step_y = 0

        self.size = size
        self.color = color
        self.width = width
    
    def disp(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.size, self.width)

    def _ramble(self, shape, position, size, r=10):
        if shape == 'circle':
            step_x =  random.randint(-r, r)
            step_y =  random.randint(-r, r)
            if math.sqrt((self.x-position[0])**2 + (self.y-position[1])**2) <= size:
                self.x += step_x
                self.y += step_y
            else:
                self.x -= step_x
                self.y -= step_y
        elif shape == 'rect':
            step_x =  random.randint(-r, r)
            step_y =  random.randint(-r, r)
            if abs(self.x-position[0]) < size[0]:
                self.x += step_x
            else:
                self.x -= step_x

            if abs(self.y-position[0]) < size[1]:
                self.y += step_y
            else:
                self.y -= step_y
        else:
            print('Unsurpported')

    def back_adom(self, posi_l, s=10):
        position = posi_l[int(self.adom)]
        step = random.randint(0,s)
        target_r = int(4*(position[2]/5))
        if position[0]-target_r<= self.x <= position[0]+target_r and position[1]-target_r<= self.y <= position[1]+target_r:
            self._ramble('rect', position, (position[2], position[2]), r=3)
        else:
            self.step_x = sign(position[0]-self.x)*step
            self.step_y = sign(position[1]-self.y)*step
            self.x += self.step_x
            self.y += self.step_y

        

    def go_dining(self, position, s=10):
        step = random.randint(0,s)
        target_r = int(4*(position[2]/5))
        if math.sqrt((self.x-position[0])**2+(self.y-position[1])**2) <= target_r:
        # if position[0]-target_r<= self.x <= position[0]+target_r and position[1]-target_r<= self.y <= position[1]+target_r:
            self._ramble('circle', position, position[2])
        else:
            self.step_x = sign(position[0]-self.x)*step
            self.step_y = sign(position[1]-self.y)*step
            self.x += self.step_x
            self.y += self.step_y

    def go_class(self, position, s=12):
        step = random.randint(0,s)
        target_r_1 = int(4*(position[2]/5))
        target_r_2 = int(4*(position[3]/5))
        if position[0]-target_r_1<= self.x <= position[0]+target_r_1 and position[1]-target_r_2<= self.y <= position[1]+target_r_2:
            self._ramble('rect', position, (position[2], position[3]))
        else:
            self.step_x = sign(position[0]-self.x)*step
            self.step_y = sign(position[1]-self.y)*step
            self.x += self.step_x
            self.y += self.step_y

    def go_to_play(self, position, s= 10):
        step = random.randint(0,s)
        target_r_1 = int(4*(position[2]/5))
        target_r_2 = int(4*(position[3]/5))
        if position[0]-target_r_1<= self.x <= position[0]+target_r_1 and position[1]-target_r_2<= self.y <= position[1]+target_r_2:
            self._ramble('rect', position, (position[2], position[3]))
        else:
            self.step_x = sign(position[0]-self.x)*step
            self.step_y = sign(position[1]-self.y)*step
            self.x += self.step_x
            self.y += self.step_y

class camp():
    def __init__(self, screen, coord, size, color= (150, 200, 100), width=2):
        super().__init__()
        self.screen = screen
        self.x = int(coord[0])
        self.y = int(coord[1])
        self.size1 = size[0]
        self.size2 = size[1]
        self.color =color
        self.width = width
    
    def disp(self):
        r = pygame.Rect(self.x, self.y, self.size1, self.size2)
        pygame.draw.rect(self.screen, self.color, r, self.width)  
        pygame.draw.circle(self.screen, self.color, (int(self.x+self.size1/2), self.y), int(self.size1/2), self.width) 
        pygame.draw.circle(self.screen, self.color, (int(self.x+self.size1/2), int(self.y+self.size2)), int(self.size1/2), self.width)

    def get_coord(self):
        return (int(self.x+self.size1/2), int(self.y+self.size2/2), int(self.size1/2), int(self.size2/2))
         



class dining_hall():
    def __init__(self,screen, coord, size, color= (100, 150, 150), width=2):
        super().__init__()
        self.screen = screen
        self.x = int(coord[0])
        self.y = int(coord[1])
        self.size = size
        self.color =color
        self.width = width

    def disp(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.size, self.width)
    
    def get_coord(self):
        return (self.x,self.y, self.size)
    


class class_room():
    def __init__(self, screen, coord, size, color= (150, 100, 100), width=2):
        super().__init__()
        self.screen = screen
        self.x = int(coord[0])
        self.y = int(coord[1])
        self.size1 = size[0]
        self.size2 = size[1]
        self.color =color
        self.width = width

    def disp(self):
        r = pygame.Rect(self.x, self.y, self.size1, self.size2)
        pygame.draw.rect(self.screen, self.color, r, self.width)
    
    def get_coord(self):
        return (int(self.x+self.size1/2), int(self.y+self.size2/2), int(self.size1/2), int(self.size2/2))   

class adom_room():
    def __init__(self, screen, coord, size, color= (0, 0, 0), width=1):
        super().__init__()
        self.screen = screen
        self.x = int(coord[0])
        self.y = int(coord[1])
        self.size = size
        self.color =color
        self.width = width

    def disp(self):
        r_l = []
        for r in range(5):
            for c in range(10):
                r_l.append(
                    pygame.Rect(self.x+r*self.size, self.y+c*self.size, self.size, self.size)
                )  
        for re in r_l:
            pygame.draw.rect(self.screen, self.color, re, self.width) 

    def get_coord(self):
        coord_l = []
        for r in range(5):
            for c in range(10):
                coord_l.append(
                    (self.x+r*self.size+ int(self.size/2), self.y+c*self.size + int(self.size/2) , int(self.size/2))
                )  
        return coord_l      