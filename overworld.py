import random
import math

# Overworld maps

# Similar to the square below, but restricted to a circle inscribed within that square.
def get_n_n_circle(x,y,n):
    xn = n*math.floor(x/n)
    yn = n*math.floor(y/n)
    seed_string = str(xn)+"-"+str(yn)
    random.seed(seed_string)
    is_continent = 0
    if random.uniform(0.,1.) < 0.6:
        x_res = x-xn
        y_res = y-yn
        in_circle = (x_res-n/2)**2+(y_res-n/2)**2 < n**2/4
        if in_circle:
            is_continent = 1
    if is_continent:
        return random.uniform(-3,3)
    return 0

# Determine a continent or ocean.
# All continents or oceans generated are on squares (in,in+n-1) X (jn,jn+n-1) of uniform height.
def get_n_n_height(x,y,n):
    xn = n*math.floor(x/n)
    yn = n*math.floor(y/n)
    seed_string = str(xn)+"-"+str(yn)
    random.seed(seed_string)
    is_continent = 0
    if random.uniform(0.,1.) < 0.6:
        is_continent = 1
    if is_continent:
        return random.uniform(-3,3)
    return 0

# Same as nXn height above, except n=1.
def get_1_1_height(x,y):
    seed_string = str(x)+"-"+str(y)
    random.seed(seed_string)
    is_continent = 0
    if random.uniform(0.,1.) < 0.6:
        is_continent = 1
    if is_continent:
        return random.uniform(-3,3)
    return 0

def get_terrain(h):
    if h <= 0:
        return 'water'
    return 'grass'

def build_map(req_data, app):
    # A bare-bones overworld to get started
    location = {"x":0, "y":0}
    if ("location_x" in req_data):
        location["x"] = req_data["location_x"]
    if ("location_y" in req_data):
        location["y"] = req_data["location_y"]
    # The overworld is assumed to be 12X12 for now, with one floor.
    size_x = 12
    size_y = 12

    start_x = 5
    start_y = 5
    if ("start_x" in req_data):
        start_x = req_data["start_x"]
    if ("start_y" in req_data):
        start_y = req_data["start_y"]
    if "navigation_x" in req_data and "navigation_y" in req_data:
        if req_data["navigation_x"] == 0:
            start_x = size_x-2
            start_y = req_data["navigation_y"]
        elif req_data["navigation_x"] == size_x-1:
            start_x = 1
            start_y = req_data["navigation_y"]
        elif req_data["navigation_y"] == 0:
            start_x = req_data["navigation_x"]
            start_y = size_y-2
        elif req_data["navigation_y"] == size_y-1:
            start_x = req_data["navigation_x"]
            start_y = 1

    height_map = []
    maze = []
    overlay = []

    for i in range(1):
        height_map.append(
            [
                [0 for j in range(size_x)]
                for i in range(size_y)
            ]
        )
        for k in range(size_y):
            for j in range(size_x):
                height = sum([get_n_n_height(location["x"]*size_x+j,location["y"]*size_y+k,2**exp) for exp in range(1)])
                height += sum([get_n_n_circle(location["x"]*size_x+j,location["y"]*size_y+k,2**exp) for exp in range(2,10)])
                height_map[0][k][j] = height
        maze.append(
            [
                [get_terrain(height_map[0][i][j]) for j in range(size_x)]
            for i in range(size_y)]
        )
        overlay.append(
            [
                ['nothing' for j in range(size_x)]
            for i in range(size_y)]            
        )
    overlay[0][3][3] = "tower"

    result = {"tiles":maze, "overlay":overlay}
    result["start_x"] = start_x
    result["start_y"] = start_y
    result["floor"] = 0
    result["tileset"] = "overworld"
    result["location"] = location
    result["navigation"] = {"offscreen":1}
    result["warps"] = [{"x":3,"y":3,"z":0}] # Combine this with the navigation offscreen object eventually
    result["map_type"] = "overworld"
    return result