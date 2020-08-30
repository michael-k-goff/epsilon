fetch("/mapgen", {method:"post"})
    .then(response => response.json())
    .then(response => {
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