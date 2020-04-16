import math
import Objects.prediction as Prediction
import PSOCluster.Params as Parameter


def get_clusters(predictions, enemies):
    clusters = []
    N = len(predictions)
    K = int(math.sqrt(N))

    displacements = []
    velocities = []
    previous_fitness = []
    current_fitness = []

    for i in range(0, 9):
        displacements.append(Parameter.Displacement(i))
        velocities.append(Parameter.Velocity(i))
        previous_fitness.append(0)
        current_fitness.append(0)

    solution_set = []
    for prediction in predictions:
        solution_set.append(Parameter.Solution(prediction))

    for solution in solution_set:
        for displacement in displacements:
            solution.update_fitness(displacement)

    local_best_positions = displacements

    for i in range(0, 50):

        previous_fitness = current_fitness
        current_fitness = []

        for displacement in displacements:
            count = 0
            fitness = 0
            for solution in solution_set:
                if solution.nearest_displacement == displacement.get_id():
                    count += 1
                    fitness += solution.fitness
            if count > 0:
                displacement.update_fitness(fitness/count)
            else:
                displacement.update_fitness(300)
            current_fitness.append(fitness)

        for i in range(0, len(current_fitness)):
            if current_fitness[i] < previous_fitness[i]:
                local_best_positions[i] = displacements[i]

        global_best_positions = []
        for displacement in displacements:
            lat = 0
            lon = 0
            count = 0
            for solution in solution_set:
                if solution.nearest_displacement == displacement.get_id():
                    lat += solution.latitude
                    lon += solution.longitude
                    count += 1
            if count > 0:
                global_best_positions.append(Parameter.BestDisplacement(lat/count, lon/count))
            else:
                global_best_positions.append(Parameter.BestDisplacement(displacement.x_lat, displacement.x_lon))

        index0 = 0
        for velocity in velocities:
            velocity.update(displacements[index0], local_best_positions[index0], global_best_positions[index0])
            index0 += 1

        index1 = 0
        for displacement in displacements:
            displacement.update(velocities[index1])
            index1 += 1

    for displacement in displacements:
        print("For cluster " + str(displacement.id) + " fitness value is " + str(displacement.evaluate_fitness()) + " Nearest enemy is at distance " + str(displacement.get_nearest_enemy(enemies)))

    for displacement in displacements:
        if displacement.evaluate_fitness() < 20:
            clusters.append(Prediction.Prediction(displacement.x_lon, displacement.x_lat))

    return clusters
