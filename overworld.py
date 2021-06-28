# Overworld maps

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

    maze = []
    overlay = []

    for i in range(1):
        maze.append(
            [
                ['grass' for j in range(size_x)]
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