import config
import learn

def set_found(unused_addr, is_found):
    config.is_found = is_found
    #print(is_found)

def print_raws(unused_addr, *raws):
    print(len(raws))

def learn_raws(unused_addr, learner, *raws):
    learn.write(raws)
