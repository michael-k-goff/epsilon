map_data = {}

generate_map = () => {
    // Clear out the old tiles
    let tiles = document.getElementById("map");
    while (tiles.firstChild) {
        tiles.removeChild(tiles.firstChild);
    }

    // Build and fire off the POST request
    let x = document.getElementById('x').value;
    let y = document.getElementById('y').value;
    fetch(
        "/mapgen", {
            method:"post",
            body: JSON.stringify({"x":x, "y":y}),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
        }
    )
    .then(response => response.json())
    .then(response => {

        // Build the map in the map div.
        let tiles = document.getElementById("map");
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