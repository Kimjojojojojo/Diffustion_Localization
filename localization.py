import numpy as np

pi = np.pi
def localization(sensors, leakage_amount,n_0, D, t):
    a = -4 * D * t
    b = a * np.log(4 * pi * D * t / n_0)

    r = [round(np.sqrt(b+a * np.log(leakage_amount[i])),2) for i in range(len(sensors))] #radius of sentered point is sensors
    print('r=',r)
    intersections = find_circle_intersections(sensors[0][0], sensors[0][1], r[0],
                                        sensors[1][0], sensors[1][1], r[1],
                                        sensors[2][0], sensors[2][1], r[2],)
    closest_point = find_closest_to_integer(intersections)

    return closest_point, r

def diffusion_function(sensors, leakage_point, n_0, D, t):
    L = np.zeros(len(sensors))

    distance = calculate_distances(sensors, leakage_point) # distance between leakage point and sensors
    print('distance =',distance)
    L = [n_0/(4*pi*D*t) * np.exp(-1*(distance[i])**2 / (4*D*t)) for i in range(len(sensors))]

    return L

def calculate_distances(sensors, leakage_point):
    distances = []
    for sensor in sensors:
        x1, y1 = sensor
        x2, y2 = leakage_point
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        distances.append(distance)
    return np.array(distances)



def calculate_intersection(x1, y1, r1, x2, y2, r2):
    d = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if d > r1 + r2 or d < abs(r1 - r2) or d == 0:
        return None
    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h = np.sqrt(r1 ** 2 - a ** 2)
    x0 = x1 + a * (x2 - x1) / d
    y0 = y1 + a * (y2 - y1) / d
    intersection1 = np.array([round(x0 + h * (y2 - y1) / d, 2), round(y0 - h * (x2 - x1) / d, 2)])
    intersection2 = np.array([round(x0 - h * (y2 - y1) / d, 2), round(y0 + h * (x2 - x1) / d, 2)])
    return intersection1, intersection2


def find_circle_intersections(x1, y1, r1, x2, y2, r2, x3, y3, r3):
    intersections = {}
    intersections["1-2"] = calculate_intersection(x1, y1, r1, x2, y2, r2)
    intersections["2-3"] = calculate_intersection(x2, y2, r2, x3, y3, r3)
    intersections["3-1"] = calculate_intersection(x3, y3, r3, x1, y1, r1)
    return intersections


def find_closest_to_integer(intersections):
    points = []
    for key, value in intersections.items():
        if value is not None:
            points.extend(value)

    # 내적이 0.1보다 작은 교차점을 찾기
    close_points = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if np.dot(points[i] - points[j], points[i] - points[j]) < 0.1:
                close_points.extend([points[i], points[j]])

    # 가장 정수에 가까운 좌표 찾기
    if close_points:
        min_dist_to_int = float('inf')
        closest_point = None
        for point in close_points:
            dist_to_int = np.abs(point - np.round(point)).sum()
            if dist_to_int < min_dist_to_int:
                min_dist_to_int = dist_to_int
                closest_point = point
        return closest_point
    return None