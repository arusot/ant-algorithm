import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Gif:
    def __init__(self, map, route, food):
        self.map = map
        self.map_size = self.map.map_size
        self.route = route
        self.food = food
    
    def create_gif(self, path):
        def update(frame):
            ax.clear()
            matrix = self.map.cells

            if frame < len(self.route):
                x, y = self.route[frame]
                matrix[x][y] = 3

                x1, y1 = self.route[frame + 1]
                matrix[x1][y1] = 2
            
            ax.imshow(matrix, cmap = 'gray', interpolation = 'nearest',
                      extent = [0, self.map_size, 0, self.map_size])
            ax.set_title(f"Step {frame + 1} | Food {self.food[frame]}")
            ax.xaxis.set_tick_params(labelbottom = False)
            ax.yaxis.set_tick_params(labelleft = False)

            plt.xticks(range(self.map_size + 1))
            plt.yticks(range(self.map_size + 1))
            plt.grid(color = 'gray', linestyle = '-', linewidth = 0.3)
            
            ax.axis('on')

        fig, ax = plt.subplots()
        animation = FuncAnimation(fig, update, frames = len(self.route) - 1, blit = False, repeat = False)
        animation.save(path, writer = 'pillow', fps = 10)
