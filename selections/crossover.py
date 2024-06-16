import copy
import random 

'''Скрестить генотипы (автоматы) двух муравьёв'''
def crossover(first_ant, second_ant):
    ants = [copy.deepcopy(first_ant), copy.deepcopy(second_ant)]

    random.shuffle(ants)
    ind = random.choice([0, 1])

    ant1, ant2 = ants[0], ants[1]

    state = random.randint(1, ant1.n_state)

    ant1.automaton[ind][state]["next_state"] = ant2.automaton[ind][state]["next_state"]
    ant2.automaton[ind][state]["next_state"] = ant1.automaton[ind][state]["next_state"]

    return ant1, ant2
