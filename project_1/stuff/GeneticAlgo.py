from math import floor
import random, numpy
from .Path import Path

class GeneticAlgo:
    def __init__(self, pop_size, mut_rate = 0.1, generations = 1000):
        self.pop_size = pop_size
        self.mut_rate = mut_rate
        self.generations = generations
        self.mutations = 0

        self.population = []
        for i in range(pop_size):
            self.population.append(Path())
        self.population.sort(key= lambda x: x.distance)

    def crossover(self, father, mother):
        divPoint = floor( len(father.route) * random.random())

        sonRoute = list(father.route[:divPoint])

        for city in mother.route:
            if city not in sonRoute:
                sonRoute.append(city)

        son = Path(sonRoute)

        if random.random() < self.mut_rate:
            self.mutations += 1
            son.mutate()

        return son  

    def generate(self):
        best_paths = []  # Lista para armazenar o melhor caminho de cada geração

        for _ in range(self.generations):

            elite_size = int(self.pop_size * 0.2)  
            elites = self.population[:elite_size]

            new_population = elites[:]

            while len(new_population) < self.pop_size:
                father = random.choice(elites)
                mother = random.choice(elites)
                son = self.crossover(father, mother)
                new_population.append(son)

            self.population = new_population

            self.population.sort(key=lambda x: x.distance)

            best_paths.append(self.population[0])

        best_path = min(best_paths, key=lambda x: x.distance)
        return [best_path, best_paths]



# test = GeneticAlgo(pop_size= 500, mut_rate= 0.6, generations = 1000)
# generations = test.generate()[1]

# for i in range(len(generations)):
#     print(f"{i}: {generations[i]}")
    
# print(test.mutations)