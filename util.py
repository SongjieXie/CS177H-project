import random

def infection(ratio):
    s = random.uniform(0, 1)
    if s < ratio:
        return 1
    else:
        return 0
    
def infection_num(x,person):
    if person.count_type() <= 2:
        x += 1
    return x
    
