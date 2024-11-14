import numpy as np
import sys
import random
from networkx import Graph

class ANT:
    A = 2
    B = 4
    P = 0.4
    M = 30
    INIT_PHEROMONE = 0.1
    MIN_PHEROMONE = INIT_PHEROMONE/1000
    ITERS = 10

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.cities = len(graph.nodes)
        self.lmin = self.greedy_value()

    def solve(self):
        self.best_distance = sys.maxsize
        self.best_path = []
        self.log = []

        # Init pheromone
        for first, second, data in self.graph.edges(data=True):
            data["pheromone"] = self.INIT_PHEROMONE

        for iter in range(self.ITERS):
            print(f"Left {self.ITERS - iter} iterations")

            # Cycle
            random_vertices = random.sample(list(self.graph.nodes), len(self.graph.nodes))
            self.ants = [ant for ant in range(self.M)]
            self.positions = {ant: random_vertices[index] for index, ant in enumerate(self.ants)}
            self.visited = {ant: [self.positions[ant]] for ant in self.ants}
            self.current_distances = {ant: 0 for ant in self.ants}

            for iteration in range(self.cities):
                for ant in self.ants:
                    current_city = self.positions[ant]
                    next_city = self.get_next_city(ant, self.positions[ant])

                    self.current_distances[ant] += self.graph[current_city][next_city]["length"]
                    self.positions[ant] = next_city
                    self.visited[ant].append(next_city)
                    
                    self.graph[current_city][next_city]["pheromone"] += self.lmin / self.current_distances[ant]
            # End cycle

            # Evoparation
            for first, second, data in self.graph.edges(data=True):
                data["pheromone"] *= (1-self.P)
            # End evoparation

            distance, path = self.get_best_current()

            if distance < self.best_distance:
                self.best_distance = distance
                self.best_path = path

            self.log.append((iter, self.best_distance))
    
    def get_best_current(self):
        ant_distances = self.current_distances.items()
        best_ant_distance = max(ant_distances, key = lambda ant_distance: ant_distance[1])

        best_ant = best_ant_distance[0]
        best_distance = best_ant_distance[1]

        return best_distance, self.visited[best_ant]

    def get_next_city(self, ant, current_city):
        allowed_neighbours = []

        if len(self.visited[ant]) == self.cities:
            allowed_neighbours = [self.visited[ant][0]]
        else:
            for neighbour in self.graph[current_city]:
                if neighbour not in self.visited[ant]:
                    allowed_neighbours.append(neighbour)
    
        probabilities = [self.get_edge_chance(current_city, neighbour, allowed_neighbours) for neighbour in allowed_neighbours]
        
        return np.random.choice(allowed_neighbours, p=probabilities)

    def get_edge_chance(self, current_city, next_city, allowed_neighbours):
        def get_edge_formula_value(edge):
            return edge["pheromone"]**self.A*(1/edge["length"])**self.B

        numerator = get_edge_formula_value(self.graph[current_city][next_city])
        denominator = 0

        for neighbour in allowed_neighbours:
            denominator += get_edge_formula_value(self.graph[current_city][neighbour])

        if denominator == 0:
            for first, second, data in self.graph.edges(data=True):
                data["pheromone"] += self.INIT_PHEROMONE
            
            return self.get_edge_chance(current_city, next_city, allowed_neighbours)

        return numerator / denominator
    
    def greedy_value(self):
        distance = 0
        cities = list(self.graph.nodes)
        current_city = cities[0]
        visited = [current_city]

        for iter in range(self.cities):
            if iter == self.cities - 1:
                visited.pop(0)
            
            next_city = None
            min_distance = float('inf')

            for neighbor in self.graph[current_city]:
                if neighbor not in visited:
                    distance = self.graph[current_city][neighbor]["length"]

                    if distance < min_distance:
                        min_distance = distance
                        next_city = neighbor

            if next_city is None:
                break

            distance += min_distance
            current_city = next_city

            visited.append(current_city)

        distance += self.graph[current_city][visited[0]]["length"]

        return distance
