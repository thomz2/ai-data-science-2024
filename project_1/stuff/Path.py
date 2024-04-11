import numpy as np
import random
from costsList import costsList as distances

class Path:
    def __init__(self, cidades = []):
        self.setRoute(cidades)
        self.distance = self.calc_fitness()

    def setRoute(self, cidades = []):
        if len(cidades) > 0:
            self.route = cidades 
        else:
            self.route = np.arange(1, 15)
            np.random.shuffle(self.route)

    def calc_fitness(self):
        dist = 0
        previous = 0
        for city in self.route:
            dist += distances[city][previous]
            previous = city
        return dist + distances[0][-1]
    
    def mutate(self):
        idx_1 = random.choice(np.arange(0, 14))
        idx_2 = random.choice(np.arange(0, 14))

        while idx_1 == idx_2: idx_2 = random.choice(np.arange(0, 14))

        aux = self.route[idx_2]
        self.route[idx_2] = self.route[idx_1]
        self.route[idx_1] = aux

        self.distance = self.calc_fitness()

    
    def __str__(self) -> str:
        return f"C-[{self.route}] F-[{self.distance}]"
    

# path = Path()

# print(path)
# path.mutate()
# print(path)
    