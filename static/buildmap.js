map_data = {};

make_image_node = (image) => {
    var node = document.createElement("img");
    node.setAttribute('src','static/'+image+'.png');
    return node;
}

make_map = () => {
    // Clear out the old tiles
    let tiles = document.getElementById("map");
    while (tiles.firstChild) {
        tiles.removeChild(tiles.firstChild);
    }

    for (let i=0; i<map_data.tiles[map_data.floor].length; i++) {
        let tile_row = document.createElement('div');
        tile_row.setAttribute('class', 'tile_row');
        for (let j=0; j<map_data.tiles[map_data.floor][i].length; j++) {
            let tile = document.createElement('div');
            if (i === map_data.x && j === map_data.y) {
                tile.innerHTML = "<span class='map-text'>?</span>";
            }
            tile_type = map_data.tiles[map_data.floor][i][j];
            overlay_type = map_data.overlay[map_data.floor][i][j];
            if (overlay_type === "stairs_up") {
                tile.appendChild(make_image_node("stone_stairs_up"));
            }
            if (overlay_type === "stairs_down") {
                tile.appendChild(make_image_node("stone_stairs_down"));
            }
            if (overlay_type === "treasure") {
                tile.appendChild(make_image_node("chest"));
            }
            tile.setAttribute('class', 'tile '+tile_type+' '+overlay_type);
            tile_row.appendChild(tile);
        }
        tiles.appendChild(tile_row);
    }
}

generate_map = (do_save) => {
    // Validate input
    if (!validateForm()) {
        return;
    }

    let x = document.getElementById('x').value;
    let y = document.getElementById('y').value;
    let z = document.getElementById('z').value;
    let room_size = document.getElementById('room_size').value;
    let corridor_preference = document.getElementById('corridor_preference').value;
    let shape = document.getElementById('dungeon_shape').value;
    
    let request_json = {
        method:"post",
        body: JSON.stringify({
            "x":x,
            "y":y,
            "z":z,
            "do_save":do_save,
            "room_size":room_size,
            "corridor_preference":corridor_preference,
            "shape":shape
        }),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }

    if (do_save) {
        fetch("/mapgen", request_json)
        return;
    }

    // Build and fire off the POST request
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
        make_map();
        if (map_data.num_generations == 1) {
            add_navigation();
        }
    })
}

// Based on code at https://stackoverflow.com/questions/3665115/how-to-create-a-file-in-memory-for-user-to-download-but-not-through-server
map_download = () => {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(map_data)));
    element.setAttribute('download', "map_data.txt");
  
    element.style.display = 'none';
    document.body.appendChild(element);
  
    element.click();
  
    document.body.removeChild(element);
}

validateForm = () => {
    let x = document.getElementById('x').value;
    let y = document.getElementById('y').value;
    let z = document.getElementById('z').value;
    let room_size = parseInt(document.getElementById('room_size').value);
    if (isNaN(x) || isNaN(y) || isNaN(z)) {
        alert("Numbers are required for Rows, Columns, and Number of Floors.");
        return false;
    }
    if (parseInt(x) < 2 || parseInt(x)>50 || parseInt(y) < 2 || parseInt(y) > 50) {
        alert("Must have between 2 and 50 (inclusive) rows and columns.");
        return false;
    }
    if (parseInt(z) < 1 || parseInt(z)>50) {
        alert("Must have between 1 and 50 (inclusive) floors.");
        return false;
    }
    if (parseInt(z) > 1 && room_size === 1) {
        alert("If there are multiple floors, the room size must be at least 2.");
        return false;
    }
    return true;
}