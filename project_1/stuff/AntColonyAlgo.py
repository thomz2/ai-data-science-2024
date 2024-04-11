from math import floor
import random, numpy as np
from .Path import Path

class AntColony:
    def __init__(self, num_ants, num_cities, alpha=1, beta=2, evaporation_rate=0.5, pheromone_deposit=1, iterations=1000):
        self.num_ants = num_ants
        self.num_cities = num_cities
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromone_deposit = pheromone_deposit
        self.iterations = iterations

        # Initialize pheromone matrix
        self.pheromone = np.ones((num_cities, num_cities))

        # Initialize distance matrix (assuming cities are represented by coordinates)
        self.distances = np.random.rand(num_cities, num_cities)

    def _select_next_city(self, ant, visited):
        pheromone_values = self.pheromone[ant.current_city, :]
        attractiveness = 1 / (self.distances[ant.current_city, :] + 1e-8)  # Add a small value to prevent division by zero
        probabilities = (pheromone_values ** self.alpha) * (attractiveness ** self.beta)
        probabilities[list(visited)] = 0  # Set probabilities of visited cities to zero
        probabilities /= probabilities.sum()  # Normalize probabilities
        next_city = np.random.choice(np.arange(self.num_cities), p=probabilities)
        return next_city

    def _update_pheromone(self, ants):
        pheromone_delta = np.zeros((self.num_cities, self.num_cities))
        for ant in ants:
            for i in range(self.num_cities - 1):
                current_city, next_city = ant.route[i], ant.route[i + 1]
                pheromone_delta[current_city, next_city] += self.pheromone_deposit / ant.distance
        self.pheromone = (1 - self.evaporation_rate) * self.pheromone + pheromone_delta

    def _ant_tour(self):
        visited = set()
        current_city = random.randint(0, self.num_cities - 1)
        route = [current_city]
        while len(visited) < self.num_cities - 1:
            next_city = self._select_next_city(current_city, visited)
            route.append(next_city)
            visited.add(next_city)
            current_city = next_city
        route_distance = self._calculate_distance(route)
        return AntPath(route, route_distance)

    def _calculate_distance(self, route):
        distance = 0
        for i in range(len(route) - 1):
            distance += self.distances[route[i], route[i + 1]]
        return distance

    def run(self):
        best_path = None
        best_distance = float('inf')

        for _ in range(self.iterations):
            ants = [self._ant_tour() for _ in range(self.num_ants)]

            # Encontrar a melhor solução da iteração atual
            iteration_best_path = min(ants, key=lambda x: x.distance)
            iteration_best_distance = iteration_best_path.distance

            # Atualizar a melhor solução global, se necessário
            if iteration_best_distance < best_distance:
                best_path = iteration_best_path
                best_distance = iteration_best_distance

            # Atualizar os feromônios
            self._update_pheromone(ants)

        return best_path
