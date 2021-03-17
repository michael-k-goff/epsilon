// Code related to navigating around a maze.

add_navigation = () => {
    let tiles = document.getElementById("map");

    document.addEventListener("keydown", event => {
        // The parameter event is of the type KeyboardEvent
        if (tiles.length == 0) {
            return;
        }
        if (event.key==="ArrowUp" || event.key==="ArrowDown" || event.key==="ArrowLeft" || event.key==="ArrowRight") {
            let target_position = [map_data.x, map_data.y];
            // Go through the four arrows
            if (event.key=="ArrowUp") {
                target_position[0] = Math.max(0, map_data.x-1);
                event.preventDefault();
            }
            if (event.key=="ArrowDown") {
                target_position[0] = Math.min(map_data.tiles[map_data.floor].length-1, map_data.x+1);
                event.preventDefault();
            }
            if (event.key=="ArrowLeft") {
                target_position[1] = Math.max(0, map_data.y-1);
                event.preventDefault();
            }
            if (event.key=="ArrowRight") {
                target_position[1] = Math.min(map_data.tiles[map_data.floor][map_data.x].length-1, map_data.y+1);
                event.preventDefault();
            }
            if (map_data.x === target_position[0] && map_data.y === target_position[1]) {
                return;
            }
            if (["floor","stairs_up","stairs_down"].includes(map_data.tiles[map_data.floor][target_position[0]][target_position[1]])) {
                map_data.x = target_position[0];
                map_data.y = target_position[1];
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
        }
    });
}