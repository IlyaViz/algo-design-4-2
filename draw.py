from matplotlib import pyplot as plt
from main import generate_cities
from algorithm import ANT

if __name__ == "__main__":
    graph = generate_cities()
    problem = ANT(graph)
    problem.solve()
    iterations = [step[0] for step in problem.log]
    min_distance = [step[1] for step in problem.log]

    plt.plot(iterations, min_distance)
    plt.xlabel("Iterations")
    plt.ylabel("Min distance")
    plt.show()