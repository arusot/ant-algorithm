import matplotlib.pyplot as plt
from Map import Map

class Animation:
    def __init__(self, matrix, route_path):
        self.matrix  = matrix
        self.route_path = route_path

    def animate(self, pause):
        _, ax = plt.subplots()
        ax.set_xticks(range(len(self.matrix[0])))
        ax.set_yticks(range(len(self.matrix)))

        file = open(self.route_path, "r")
        data = file.read()
        data = data.split("\n")
        data = data[:-1]
        file.close()

        route = []
        for pos in data:
            x, y = pos.split(',')
            route.append([int(x), int(y)])

        n_food = 0
        for i, point in enumerate(route):
            x, y = point
            
            if self.matrix[x, y]:
                n_food += 1
                self.matrix[x, y] = 0
            
            ax.clear()
            ax.imshow(self.matrix, cmap = 'Greys', origin = 'upper')
            ax.plot(y, x, 'ro', markersize = 10)
            ax.set_title(f'Шаг {i + 1} | Еда {n_food}')
            
            plt.pause(pause)

        plt.show()

map = Map('./data/map.txt')
animation = Animation(map.cells, "./data/route.txt")
animation.animate(1e-4)
