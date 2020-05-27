import random

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

    
    def __call__(self):
        return self.count_list

