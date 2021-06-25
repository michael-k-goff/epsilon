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