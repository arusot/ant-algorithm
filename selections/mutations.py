import copy
import random

'''Применить случайную мутацию к муравьям'''
def random_mutation(first_ant, second_ant):
    ants = [copy.deepcopy(first_ant), copy.deepcopy(second_ant)]

    mutations = [lambda ant: random_state(ant),
                 lambda ant: random_action(ant)]

    ant1 = random.choice(mutations)(ants[0])
    ant2 = random.choice(mutations)(ants[1])

    return ant1, ant2

'''Изменить случайное состоние автомата на другое случайное состояние'''
def random_state(entity):
    ant = copy.deepcopy(entity)
    automaton = random.randint(0, 1)
    state = random.randint(1, ant.n_state)
    new_state = random.randint(1, ant.n_state)

    while new_state == ant.automaton[automaton][state]["next_state"]:
        new_state = random.randint(1, ant.n_state)
    
    ant.automaton[automaton][state]["next_state"] = new_state

    return ant

'''Изменить случайное действие автомата на другое случайное действие'''
def random_action(entity):
    ant = copy.deepcopy(entity)
    state = random.randint(1, ant.n_state)
    new_action = random.randint(0, 2)

    while new_action == ant.automaton[0][state]["action"]:
        new_action = random.randint(0, 2)
    
    ant.automaton[0][state]["action"] = new_action
    
    return ant

'''Поменять местами поведение автоматов при наличии или отсутствии еды на клетке'''
def swap_automat(entity):
    ant = copy.deepcopy(entity)

    ant.automaton[0], ant.automaton[1] = ant.automaton.pop(1), ant.automaton.pop(0)

    return ant
