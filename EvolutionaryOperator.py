import copy
import random

from Ant import Ant

from selections.crossover import crossover
from selections.mutations import random_mutation

'''Эволюционный оператор'''
class EvolutionaryOperator:
    def __init__(self,
                 map,
                 max_iter = 200,
                 max_moves = 900,
                 n_ants = 100,
                 percent_of_survivors = 0.1,
                 percent_of_crossover = 0.25,
                 n_state = 7,
                 ):
        self.max_iter = max_iter
        self.max_moves = max_moves
        self.n_ants = n_ants
        self.percent_of_crossover = percent_of_crossover
        self.n_state = n_state
        self.map = map
        self.best = 0

        self.n_survivors = int(self.n_ants * percent_of_survivors)
        self.map_size = self.map.map_size
        self.population = [Ant(self.map_size, self.n_state) for _ in range(self.n_ants)]

    '''Выполнить селекцию популяции в количества max_iter итераций'''
    def fit(self):
        for _ in range(1, self.max_iter + 1):
            self.find_best()
            self.population = self.selection()
            self.reset_population()

            print(f"Iter {_} | Score {self.best}")
    
    '''Метод сброса всей популяции'''
    def reset_population(self):
        for ant in self.population:
            ant.reset()
    
    '''Метод выполнения селекции: отбираются муравьи с наивысшей приспособленностью,
    применяется метод перерождения муравьёв с применением мутаций и кроссинговера'''
    def selection(self):
        self.population = sorted(self.population, key = lambda ant: ant.suitability, reverse = True)

        self.population = self.population[:self.n_survivors]

        reborn_ants = self.regenerate(self.population)
        
        return self.population + reborn_ants
    
    '''Метод перерождения муравьёв для восполнения популяции, отбираются два муравья и с вероятностью 50 на 50
    применяется кроссинговер (скрещивание) или мутация к муравьям, после чего добавляются в популяцию'''
    def regenerate(self, survivors):
        reborn_ants = []

        while len(reborn_ants) < self.n_ants - self.n_survivors:
            first_ant, second_ant = random.choice(survivors), random.choice(survivors)

            if first_ant == second_ant: continue

            if (random.uniform(0, 1) < self.percent_of_crossover):
                first_ant, second_ant = crossover(first_ant, second_ant)
            else:
                first_ant, second_ant = random_mutation(first_ant, second_ant)

            reborn_ants.append(first_ant)
            reborn_ants.append(second_ant)
        
        return reborn_ants
    
    '''Поиск муравья с наивысшей приспособленностью в популяции'''
    def find_best(self):
        i = 0

        for ant in self.population:
            moves, n_food, _, _ = self.look_food(ant)
            suitability = ant.set_suitability(n_food, moves, self.max_moves)

            if suitability > self.best:
                self.best = suitability
                self.best_ant = copy.deepcopy(ant)
            
            i += 1

    '''Запустить муравья по полю для сбора еды и расчёта его приспособленности'''
    def look_food(self, ant):
        map = copy.deepcopy(self.map)

        handle_action = {
            0 : lambda ant: ant.go_ahead(),
            1 : lambda ant: ant.turn_right(),
            2 : lambda ant: ant.turn_left()
        }

        n_food = 0
        route = [copy.deepcopy(ant.position)]
        count = [0]

        for i in range(1, self.max_moves + 1):
            next_position = ant.next_position()
            cell = map.cells[next_position[0], next_position[1]]

            action = ant.automaton[cell][ant.state]["action"]
            state = ant.automaton[cell][ant.state]["next_state"]

            handle_action[action](ant)

            if (action == 0):
                x, y = ant.position[0], ant.position[1]

                if (map.cells[x, y]):
                    n_food += 1
                
                    map.cells[x, y] = 0

                    if n_food == map.n_food:
                        return i, n_food

            ant.state = state

            route.append(copy.deepcopy(ant.position))
            count.append(n_food)

        ant.reset()
        
        return self.max_moves, n_food, route, count
