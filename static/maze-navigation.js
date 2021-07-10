// Code related to navigating around a maze.

// Keeps track of which keys are pressed
key_status = {}
navigation_data = {
    time_since_last_move: 0,
    time_last_repeat: -1
};

add_navigation = () => {
    let tiles = document.getElementById("map");

    // The loop that handles navigation and timing to insure there aren't too many moves too quickly.
    // It's a bit of a mess now and should be cleaned up.
    repeated = () => {
        let target_position = [map_data.x, map_data.y];
        let date = new Date();
        let current_time = date.getTime();
        if (navigation_data["time_since_last_move"] > 0) {
            let gap = current_time - navigation_data["time_last_repeat"];
            if (gap > 30) {
                gap = 30;
            }
            if (navigation_data["time_last_repeat"] != -1) {
                navigation_data["time_since_last_move"] = navigation_data["time_since_last_move"] - gap;
            }
            navigation_data["time_last_repeat"] = current_time;
            if (navigation_data["time_since_last_move"] > 0) {
                return;
            }        
        }
        // Go through the four arrows
        if (key_status["ArrowLeft"]) {
            target_position[0] = Math.max(0, map_data.x-1);
        }
        else if (key_status["ArrowRight"]) {
            target_position[0] = Math.min(map_data.tiles[map_data.floor][map_data.y].length-1, map_data.x+1);
        }
        else if (key_status["ArrowUp"]) {
            target_position[1] = Math.max(0, map_data.y-1);
        }
        else if (key_status["ArrowDown"]) {
            target_position[1] = Math.min(map_data.tiles[map_data.floor].length-1, map_data.y+1);
        }
        if (map_data.x === target_position[0] && map_data.y === target_position[1]) {
            return;
        }
        target_file = map_data.tiles[map_data.floor][target_position[1]][target_position[0]]
        // Can walk on water for now for the sake of easy map exploration
        if (["floor","stairs_up","stairs_down","grass","water"].includes(target_file)) {
            map_data.x = target_position[0];
            map_data.y = target_position[1];
            navigation_data["time_since_last_move"] = 150;
        }
        else {
            return;
        }

        // Proces stairs
        if (map_data.overlay[map_data.floor][target_position[1]][target_position[0]] == "stairs_up") {
            map_data.floor += 1;
        }
        else if (map_data.overlay[map_data.floor][target_position[1]][target_position[0]] == "stairs_down") {
            map_data.floor -= 1;
        }
        let new_location = {"x":map_data.location.x, "y":map_data.location.y};
        if (map_data.navigation) {
            if (map_data.navigation.offscreen) {
                if (map_data.x == 0) {
                    new_location = {"x":map_data.location.x-1, "y":map_data.location.y}
                }
                else if (map_data.x == map_data.tiles[0].length-1) {
                    new_location = {"x":map_data.location.x+1, "y":map_data.location.y}
                }
                else if (map_data.y == 0) {
                    new_location = {"x":map_data.location.x, "y":map_data.location.y-1}
                }
                else if (map_data.y == map_data.tiles[0][0].length-1) {
                    new_location = {"x":map_data.location.x, "y":map_data.location.y+1}
                }
                if (new_location.x != map_data.location.x || new_location.y != map_data.location.y) {
                    let request_json = build_request_json({
                        "location_x":new_location.x,
                        "location_y":new_location.y,
                        "navigation_x":map_data.x,
                        "navigation_y":map_data.y,
                        "map_type":"overworld"
                    });
                    build_map(request_json);
                }
            }
        }

        // Process warps
        if (map_data.warps) {
            for (var i=0; i<map_data.warps.length; i++) {
                let overworld_preference = document.getElementById('overworld_preference').value;
                if (map_data.warps[i].x == map_data.x && map_data.warps[i].y == map_data.y && map_data.warps[i].z == map_data.floor) {
                    if (map_data.map_type == "overworld") {
                        let request_json = build_request_json({
                            "location_x":new_location.x,
                            "location_y":new_location.y,
                            "navigation_x":map_data.x,
                            "navigation_y":map_data.y,
                            "do_save":0,
                            "map_type":"tower",
                        })
                        build_map(request_json);
                    }
                    else if (map_data.map_type == "tower") {
                        let request_json = build_request_json({
                            "location_x":new_location.x,
                            "location_y":new_location.y,
                            "start_x":3,
                            "start_y":3,
                            "map_type":"overworld",
                            "overworld_preference":overworld_preference
                        })
                        build_map(request_json);
                    }
                }
            }
        }
        // The whole map is remade to update the displayed position. Consider revising this.
        make_map();
        self.setInterval(repeated, 30);
    }
    self.setInterval(repeated, 30);

    document.addEventListener("keyup", event => {
        key_status[event.key] = 0;
    });

    document.addEventListener("keydown", event => {
        // The parameter event is of the type KeyboardEvent
        key_status[event.key] = 1;
        if (tiles.length == 0) {
            return;
        }
        if (event.key==="ArrowUp" || event.key==="ArrowDown" || event.key==="ArrowLeft" || event.key==="ArrowRight") {
            // Go through the four arrows
            if (event.key=="ArrowUp") {
                event.preventDefault();
            }
            if (event.key=="ArrowDown") {
                event.preventDefault();
            }
            if (event.key=="ArrowLeft") {
                event.preventDefault();
            }
            if (event.key=="ArrowRight") {
                event.preventDefault();
            }
        }
    });
}