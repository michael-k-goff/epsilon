map_data = {}

generate_map = (do_save) => {
    // Validate input
    if (!validateForm()) {
        return;
    }

    let x = document.getElementById('x').value;
    let y = document.getElementById('y').value;
    let room_size = document.getElementById('room_size').value;
    
    let request_json = {
        method:"post",
        body: JSON.stringify({
            "x":x,
            "y":y,
            "do_save":do_save,
            "room_size":room_size
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
        for (let i=0; i<response.tiles.length; i++) {
            let tile_row = document.createElement('div');
            tile_row.setAttribute('class', 'tile_row');
            for (let j=0; j<response.tiles[i].length; j++) {
                let tile = document.createElement('div');
                tile.setAttribute('class', 'tile '+response.tiles[i][j]);
                tile_row.appendChild(tile);
            }
            tiles.appendChild(tile_row);
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
    if (isNaN(x) || isNaN(y)) {
        alert("Numbers are required for Rows and Columns");
        return false;
    }
    if (parseInt(x) < 2 || parseInt(x)>50 || parseInt(y) < 2 || parseInt(y) > 50) {
        alert("Must have between 2 and 50 (inclusive) rows and columns");
        return false;
    }
    return true;
}