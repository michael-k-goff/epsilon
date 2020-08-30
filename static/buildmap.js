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