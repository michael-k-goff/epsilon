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

    result = {"tiles":maze, "overlay":overlay}
    result["start_x"] = 5
    result["start_y"] = 5
    result["floor"] = 0
    result["tileset"] = "overworld"
    result["location"] = location
    result["navigation"] = {"offscreen":1}
    return result