import networkx
import random
from algorithm import ANT

CITIES = 100
MIN_DISTANCE = 5
MAX_DISTANCE = 50

def generate_cities():
    graph = networkx.Graph()

    for x in range(CITIES):
        graph.add_node(x)

    for x in range(CITIES):
        for y in range(x+1, CITIES):
                graph.add_edge(x, y, length=random.randint(MIN_DISTANCE, MAX_DISTANCE))

    return graph

if __name__ == "__main__":
    cities = generate_cities()
    problem = ANT(cities)
    problem.solve()
    path = problem.best_path
    distance = problem.best_distance

    for edge in cities.edges(data=True):
        print(f"Distance from {edge[0]} to {edge[1]} is ({edge[2]['length']})")
    
    print(f"\nSOLUTION (min distance = {distance})")
    print(f"Start with {path[0]}")

    for index in range(len(path)-1):
        print(f"Go from {path[index]} to {path[index+1]}, distance is ({cities[path[index]][path[index+1]]['length']})")
