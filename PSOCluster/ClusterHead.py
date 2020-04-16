import random
import Setup.SimulationSetup as setup


class ClusterHead:

    def __init__(self,  id, c_lon=79.056, c_lat=21.129):
        self.latitude = c_lat + random.randint(2, 7)*0.0001 + random.randint(2, 4)*0.00001 + random.randint(1, 9)*0.000001
        self.longitude = c_lon + random.randint(6, 9)*0.0001 + random.randint(0, 7)*0.00001 + random.randint(1, 7)*0.000001
        self.children = []
        self.id = id

    def get_position(self):
        return [self.latitude, self.longitude]

    def get_id(self):
        return self.id

    def get_distance(self, prediction):
        return setup.get_distance(prediction.get_longitude(), prediction.get_latitude(), self.get_position()[1], self.get_position()[0])

    def add_child(self, prediction):
        self.children.append(prediction)

    def update_position(self):
        N = len(self.children)

        if N > 0:
            new_lat = 0
            new_lon = 0
            for child in self.children:
                new_lat += child.get_latitude()
                new_lon += child.get_longitude()

            new_lat /= N
            new_lon /= N
            delta = setup.get_distance(new_lon, new_lat, self.longitude, self.latitude)
            self.latitude = new_lat
            self.longitude = new_lon
            return delta

        else:
            return 0

    def get_child_count(self):
        return len(self.children)

    def get_nearest_enemy_dist(self, enemies):
        min_dist = 300
        for enemy in enemies:
            dist = setup.get_distance(self.longitude, self.latitude, enemy.get_longitude(), enemy.get_latitude())
            if dist < min_dist:
                min_dist = dist

        return min_dist

    def reset(self):
        self.children = []