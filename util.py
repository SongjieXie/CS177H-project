import random
import os
from datetime import datetime

def infection(ratio):
    s = random.uniform(0, 1)
    if s < ratio:
        return 1
    else:
        return 0
    
def infection_num(x,person):
    if person.count_type() < 2:
        x += 1
    return x



def init_infect(person_l, num_I, num_C):
    index_l = list(range(len(person_l)))
    I_index_l = random.sample(index_l, num_I)
    for i in I_index_l:
        index_l.remove(i)
    C_index_l = random.sample(index_l, num_C)

    for j in I_index_l:
        per = person_l[j]
        per.change_type(0)
    
    for j in C_index_l:
        per = person_l[j]
        per.change_type(1)


class count_total_SIR():

    def __init__(self):
        super().__init__()
        self.count_list = [[],[],[]]
        self.num_0 = 0
        self.num_1 = 0
        self.num_2 = 0

    def update(self, person_l):
        for p in person_l:
            if p.count_type() == 0:
                self.num_0 += 1
            elif p.count_type() == 1:
                self.num_1 += 1
            elif p.count_type() == 2:
                self.num_2 +=1
            else:
                print('Unkown Type!!!  PANIC!!')
        self.count_list[0].append(self.num_0)
        self.count_list[1].append(self.num_1)
        self.count_list[2].append(self.num_2)
        self.num_0 = 0
        self.num_1 = 0
        self.num_2 = 0

    def reset(self):
        self.count_list = [[],[],[]]
        self.num_0 = 0
        self.num_1 = 0
        self.num_2 = 0


    
    def __call__(self):
        return self.count_list


class recorder():
    def __init__(self, path_to_save=None, path='./doc'):
        super().__init__()
        if not path_to_save:
            date = str(datetime.now()).split()[0]
            dirl = os.listdir(path)
            name = ''
            for i in range(100):
                name_tmp = date+'_num_'+str(i)+'.txt'
                if name_tmp not in dirl:
                    name = name_tmp
                    break

        self.name = os.path.join(path, name)
        self.f = open(self.name, 'w')
        self._initialize()

        self.counting = 0

    def _initialize(self):
        head = 'Recording document:\nDate: '+str(datetime.now())+'\n'+'Params:\n'
        self.f.write(head)
    
    def write_params(self, p1, p2, p3):
        self.f.write(str(p1)+'\n')
        self.f.write(str(p2)+'\n')
        self.f.write(str(p3)+'\n')
    
    def write_frame(self,day_num, frame_num, SIR_l, posi):
        self.counting += 1
        string_1 = 'S:'+str(SIR_l[0][-1])+ ' ' + 'I:'+ str(SIR_l[1][-1])+' ' + 'N:' + str(SIR_l[2][-1]) + ' '
        string_2 = 'Dorm:'+str(posi[0])+ ' ' +'Class:'+str(posi[1])+ ' ' + 'Canteen:' +str(posi[2])+ ' ' + 'Play:'+str(posi[3]) + ' '
        spot = ''
        if frame_num >= 0 and frame_num <201:
            spot = 'Dorm'
        elif frame_num >200 and frame_num < 401:
            spot = 'Class'
        elif frame_num > 400 and frame_num <601:
            spot = 'Canteen'
        elif frame_num > 600 and frame_num <801:
            spot = 'Play'
        elif frame_num > 800 and frame_num <1001:
            spot =  'Dorm'
        string = '['+str(self.counting)+'] '+ 'Day('+str(day_num)+') ' +'<'+ spot + '> '+ string_1+ string_2 +'\n'
        self.f.write(string) 
    
    def close_file(self):
        self.f.close()
    



    

        
        


if __name__ == '__main__':
    date = str(datetime.now()).split()[0]
    print(date, type(date))
