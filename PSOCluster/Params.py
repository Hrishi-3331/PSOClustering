import random
import math
import Setup.SimulationSetup as Setup
# v(t+1) = w*v(t) + c1*r1(t)*(y(t)−x(t)) + c2*r2(t)*(y(t)−x(t))

W = 0.6
c1 = 0.5
c2 = 0.8


class Displacement:

    def __init__(self,  id, c_lon=79.056, c_lat=21.129):
        self.id = id
        self.x_lat = c_lat + random.randint(2, 7)*0.0001 + random.randint(2, 4)*0.00001 + random.randint(1, 9)*0.000001
        self.x_lon = c_lon + random.randint(6, 9)*0.0001 + random.randint(0, 7)*0.00001 + random.randint(1, 7)*0.000001
        self.fitness = 0

    def evaluate_fitness(self):
        return self.fitness

    def update(self, velocity):
        self.x_lat = self.x_lat + velocity.v_lat
        self.x_lon = self.x_lon + velocity.v_lon

    def get_id(self):
        return self.id

    def update_fitness(self, param):
        self.fitness = param

    def get_nearest_enemy(self, enemies):
        nearest_dist = 300
        for enemy in enemies:
            temp = Setup.get_distance(self.x_lon, self.x_lat, enemy.longitude, enemy.latitude)
            if temp < nearest_dist:
                nearest_dist = temp
        return nearest_dist


class BestDisplacement:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude


class Velocity:

    def __init__(self,  id):
        self.id = id
        self.v_lat = random.choice((-1, 1)) * (random.randint(0, 1)*0.0001 + random.randint(2, 3)*0.00001 + random.randint(1, 9)*0.000001)
        self.v_lon = random.choice((-1, 1)) * (random.randint(0, 1)*0.0001 + random.randint(0, 4)*0.00001 + random.randint(1, 7)*0.000001)

    def update(self, displacement, local_best_position, global_best_position):
        self.v_lat = W*self.v_lat + c1*(local_best_position.x_lat - displacement.x_lat) + c2*(global_best_position.get_latitude() - displacement.x_lat)
        self.v_lon = W*self.v_lon + c1*(local_best_position.x_lon - displacement.x_lon) + c2*(global_best_position.get_longitude() - displacement.x_lon)


class Neighbour:

    def __init__(self, dist, prediction):
        self.dist = dist
        self.prediction = prediction


class Solution:

    def __init__(self, prediction):
        self.latitude = prediction.get_latitude()
        self.longitude = prediction.get_longitude()
        self.nearest_displacement = None
        self.fitness = 300

    def update_fitness(self, displacement):
        temp = Setup.get_distance(self.longitude, self.latitude, displacement.x_lon, displacement.x_lat)
        if temp < self.fitness:
            self.fitness = temp
            self.set_nearest(displacement)

    def set_nearest(self, displacement):
        self.nearest_displacement = displacement.get_id()