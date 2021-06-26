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
        if (key_status["ArrowUp"]) {
            target_position[0] = Math.max(0, map_data.x-1);
        }
        else if (key_status["ArrowDown"]) {
            target_position[0] = Math.min(map_data.tiles[map_data.floor].length-1, map_data.x+1);
        }
        else if (key_status["ArrowLeft"]) {
            target_position[1] = Math.max(0, map_data.y-1);
        }
        else if (key_status["ArrowRight"]) {
            target_position[1] = Math.min(map_data.tiles[map_data.floor][map_data.x].length-1, map_data.y+1);
        }
        if (map_data.x === target_position[0] && map_data.y === target_position[1]) {
            return;
        }
        target_file = map_data.tiles[map_data.floor][target_position[0]][target_position[1]]
        if (["floor","stairs_up","stairs_down","grass"].includes(target_file)) {
            map_data.x = target_position[0];
            map_data.y = target_position[1];
            navigation_data["time_since_last_move"] = 150;
        }
        else {
            return;
        }

        // Proces stairs
        if (map_data.overlay[map_data.floor][target_position[0]][target_position[1]] == "stairs_up") {
            map_data.floor += 1;
        }
        else if (map_data.overlay[map_data.floor][target_position[0]][target_position[1]] == "stairs_down") {
            map_data.floor -= 1;
        }
        if (map_data.navigation) {
            if (map_data.navigation.offscreen) {
                let new_location = {"x":map_data.location.x, "y":map_data.location.y};
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
                    let request_json = {
                        method:"post",
                        body: JSON.stringify({
                            "location_x":new_location.x,
                            "location_y":new_location.y
                        }),
                        cache: "no-cache",
                        headers: new Headers({
                            "content-type": "application/json"
                        })
                    }
                    // Separate function here because this code is largely duplicated
                    fetch(
                        "/mapgen", request_json
                    )
                    .then(response => response.json())
                    .then(response => {
                        // Clear out the old tiles
                        let tiles = document.getElementById("map");
                        while (tiles.firstChild) {
                            tiles.removeChild(tiles.firstChild);
                        }

                        // Build the map in the map div.
                        map_data.tiles = response.tiles;
                        map_data.overlay = response.overlay;
                        map_data.x = response.start_x;
                        map_data.y = response.start_y;
                        map_data.floor = response.floor;
                        map_data.num_generations = "num_generations" in map_data ? map_data.num_generations+1 : 1;
                        map_data.location = "location" in response ? response.location : {};
                        map_data.navigation = "navigation" in response ? response.navigation : {};
                        make_map();
                        if (map_data.num_generations == 1) {
                            add_navigation();
                        }
                    })
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