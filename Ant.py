import math
import random

class Ant:
    def __init__(self, map_size, n_state):
        self.position = [map_size - 1, 0]
        self.angle = 90
        self.suitability = 0
        self.map_size = map_size
        self.automaton = {0: {}, 1: {}}
        self.n_state = n_state

        self.state = random.randint(1, self.n_state)

        for i in range(1, self.n_state + 1):
            self.automaton[0][i] = {
                "action": random.randint(0, 2),
                "next_state": random.randint(1, self.n_state)
            }
            self.automaton[1][i] = {
                "action": 0,
                "next_state": random.randint(1, self.n_state)                      
            }
    
    '''Сбросить состояние муравья'''
    def reset(self):
        self.position = [self.map_size - 1, 0]
        self.angle = 90
        self.suitability = 0

    '''Идти прямо. Если муравей выходит за границу карты - он появляется на противоположной границе'''
    def go_ahead(self):
        angle_rad = math.radians(self.angle)

        self.position[0] += int(math.cos(angle_rad))
        self.position[1] += int(math.sin(angle_rad))

        self.position = self.borders_collision(self.position)
    
    '''Повернуться вправо'''
    def turn_right(self):
        self.angle = (self.angle + 90) % 360

    '''Повернуться влево'''
    def turn_left(self):
        self.angle = (self.angle - 90) % 360
    
    '''Получить следующую позицию при ходе вперёд'''
    def next_position(self):
        angle_rad = math.radians(self.angle)

        next_position = [int(math.cos(angle_rad)), int(math.sin(angle_rad))]

        next_position[0] += self.position[0]
        next_position[1] += self.position[1]

        next_position = self.borders_collision(next_position)

        return next_position

    '''Проверка на коллизию с границей карты'''
    def borders_collision(self, position):
        if (position[0] < 0): position[0] = self.map_size - 1
        if (position[1] < 0): position[1] = self.map_size - 1

        if (position[0] >= self.map_size): position[0] = 0
        if (position[1] >= self.map_size): position[1] = 0

        return position
    
    '''Установить занчение приспособленности муравью'''
    def set_suitability(self, n_food, moves, max_moves):
        self.suitability = (max_moves - moves) / max_moves + n_food
        return self.suitability
    