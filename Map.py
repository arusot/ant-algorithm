import numpy as np

class Map:
    def __init__(self, path):
        self.cells = np.loadtxt(path, delimiter=' ').astype(int)
        self.map_size = len(self.cells)
        self.n_food = len(np.where(self.cells == 1)[0])
