import random
from Setup import Calculations, SimulationSetup as Setup
import json as json
from Objects.prediction import Prediction
import PSOCluster.ClusterSetup as PSOSetup
import time

riffle_range = 300
ns = int(input('Enter number of soldiers :'))
ne = int(input('Enter number of enemies :'))
N = int(input('Enter number of frames to be analyzed :'))

soldiers = Setup.generate_soldiers(ns)
enemies = Setup.generate_enemies(ne)
set_points = []

start_time = time.time()
for z in range(0, N):
    predictions = []
    for x in range(0, 10):
        i = 0
        done = []
        el = len(enemies)
        sl = len(soldiers)
        while i < el:
            index = random.randint(0, sl - 1)
            rep = False

            for p in done:
                if p == index:
                    rep = True
                    break

            if not rep:
                soldiers[index].set_target(enemies[i])
                done.append(index)
                i = i + 1

        for soldier in soldiers:
            if soldier.get_target() is None:
                soldier.set_target(enemies[random.randint(0, el - 1)])

        # Obtaining azimuth :
        for soldier in soldiers:
            angle = Setup.calculate_true_angle(soldier) + random.choice((-1, 1))*0.03491
            azimuth = angle
            soldier.set_azimuth(azimuth)

        # Start simulation
        i = 0
        n = len(soldiers)
        while i < n:
            soldier1 = soldiers[i]
            [x1, y1] = Setup.get_coordinates(soldier1)
            w1 = soldier1.get_azimuth()
            p = i + 1
            while p < n:
                soldier2 = soldiers[p]
                [x2, y2] = Setup.get_coordinates(soldier2)
                w2 = soldier2.get_azimuth()
                res = Calculations.get_enemy_location(x1, y1, x2, y2, w1, w2)
                location = Calculations.inverse_mercator(res[0], res[1])
                if res[0] > max(x1, x2):
                    d = Setup.get_distance(location[1], location[0], soldier1.get_longitude(), soldier1.get_latitude())
                    if d < 300:
                        temp = Prediction(location[1], location[0])
                        predictions.append(temp)
                p = p + 1
            i = i + 1

    prediction_result = PSOSetup.get_clusters(predictions, enemies)
    print("\n\n")

    features = []
    i = 0
    for enemy in enemies:
        temp = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    enemy.get_longitude(),
                    enemy.get_latitude()
                ]
            },
            "properties": {
                "title": 'Enemy' + str(i),
                "icon": "monument"
            }
        }
        features.append(temp)
        i = i + 1

    enemy_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('./plots/enemies.geojson', 'w') as outfile:
        json.dump(enemy_data, outfile)

    features = []
    i = 0
    for soldier in soldiers:
        temp = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    soldier.get_longitude(),
                    soldier.get_latitude()
                ]
            },
            "properties": {
                "title": 'Soldier' + str(i),
                "icon": "monument"
            }
        }
        features.append(temp)
        i = i + 1

    soldier_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('./plots/soldiers.geojson', 'w') as outfile:
        json.dump(soldier_data, outfile)

    features = []
    i = 0
    for prediction in prediction_result:
        for soldier in soldiers:
            if Setup.get_distance(prediction.get_longitude(), prediction.get_latitude(), soldier.get_longitude(),
                                  soldier.get_latitude()) < 10:
                prediction_result.remove(prediction)
                break

    for prediction in prediction_result:
        temp = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    prediction.get_longitude(),
                    prediction.get_latitude()
                ]
            },
            "properties": {
                "title": 'Prediction' + str(i),
                "icon": "monument",
            }
        }
        features.append(temp)
        i = i + 1

    prediction_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('./plots/predictions' + str(z) + '.geojson', 'w') as outfile:
        json.dump(prediction_data, outfile)

    features = []
    for soldier in soldiers:
        coordinates = [
            [soldier.get_longitude(), soldier.get_latitude()],
            [soldier.get_target().get_longitude(), soldier.get_target().get_latitude()]
        ]
        feature = {
            'type': 'Feature',
            'geometry': {
                "type": "LineString",
                "coordinates": coordinates
            }
        }
        features.append(feature)

    shoot_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('./plots/shoots' + str(z) + '.geojson', 'w') as outfile:
        json.dump(shoot_data, outfile)

end_time = time.time()
print(f"Simulation complete in {end_time - start_time} seconds")
