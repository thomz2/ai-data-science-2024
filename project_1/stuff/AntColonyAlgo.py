from math import floor
import random, numpy as np
try:
    from .Path import Path
except:
    from Path import Path

class AntColony:
    def __init__(self, num_ants=150, num_cities=15, alpha=1, beta=2, evaporation_rate=0.5, pheromone_deposit=1, iterations=500):
        self.num_ants = num_ants
        self.num_cities = num_cities
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromone_deposit = pheromone_deposit
        self.iterations = iterations
        self.pheromone = np.ones((num_cities, num_cities))
        self.distances = np.random.rand(num_cities, num_cities)

    def _select_next_city(self, ant, visited):
        pheromone_values = self.pheromone[ant, :]
        attractiveness = 1 / (self.distances[ant, :] + 1e-8)  # Add a small value to prevent division by zero
        
        # Define as probabilidades apenas para cidades não visitadas
        unvisited_probabilities = np.copy(pheromone_values)
        unvisited_probabilities[list(visited)] = 0  # Set probabilities of visited cities to zero
        
        # Se todas as cidades já foram visitadas, retorna a cidade inicial
        if np.sum(unvisited_probabilities) == 0:
            return 0
        
        # Calcula as probabilidades normalizadas apenas para as cidades não visitadas
        probabilities = (unvisited_probabilities ** self.alpha) * (attractiveness ** self.beta)
        probabilities /= probabilities.sum()  # Normalize probabilities
        
        # Escolhe a próxima cidade baseada nas probabilidades
        next_city = np.random.choice(np.arange(self.num_cities), p=probabilities)
        # while next_city == 0: next_city = np.random.choice(np.arange(self.num_cities))

        return next_city


    # Entendido
    def _update_pheromone(self, ants):
        prev = 0
        pheromone_delta = np.zeros((self.num_cities, self.num_cities))
        for ant in ants:
            for city in ant.route:
                pheromone_delta[city, prev] += self.pheromone_deposit / ant.distance
                prev = city
        pheromone_delta[0, prev] += self.pheromone_deposit / ant.distance

        self.pheromone = (1 - self.evaporation_rate) * self.pheromone + pheromone_delta

    # Entendido
    def _ant_tour(self):
        visited = set()
        visited.add(0)
        current_city = 0 # random.randint(0, self.num_cities - 1)
        route = []
        while len(visited)-1 < self.num_cities - 1:
            next_city = self._select_next_city(current_city, visited) # Tenho que assegurar que isso nunca seja 0
            route.append(next_city)
            visited.add(next_city)
            current_city = next_city
        # route_distance = self._calculate_distance(route)
        return Path(route)

    def run(self):
        best_path = None
        best_distance = float('inf')

        for _ in range(self.iterations):
            ants = [self._ant_tour() for _ in range(self.num_ants)]

            # Encontrar a melhor solução da iteração atual
            iteration_best_path = min(ants, key=lambda x: x.distance)
            iteration_best_distance = iteration_best_path.distance
            print(f"{_}: {iteration_best_path}")

            # Atualizar a melhor solução global, se necessário
            if iteration_best_distance < best_distance:
                best_path = iteration_best_path
                best_distance = iteration_best_distance

            # Atualizar os feromônios
            self._update_pheromone(ants)

        return best_path

antC = AntColony()
print(antC.run())