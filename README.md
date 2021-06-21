# epsilon

Project Epsilon is a maze generator.

#### To Run:

1. If necessary, install [Flask](https://pypi.org/project/Flask/).
2. If necessary, install [jinja2](https://jinja.palletsprojects.com/en/3.0.x/).
3. Navigate to the project folder on the command line.
4. Type `export FLASK_APP=main.py`.
5. Type `flask run`.
6. Navigate the browser to `localhost:5000`. Tested in Chrome.

It may be necessary to set up a virtual environment.

#### Usage:

Through the browser, you can select the numbers of rows, columns, floors, room size, and set preferences for shape of the dungeon and the lengths of hallways or the quantity of stairs.

The number of rows and columns must be an integer between 2 and 50 (inclusive), and the number of floors must be between 1 and 50 (inclusive).

If there are 2 or more floors, then the room size must be at least 2. This is to allow enough space to put upstairs, downstairs, and a treasure chest in a given room if necessary.

Once `Generate Map` is invoked, the player (represented by `?`) can be moved with the `Up`, `Down`, `Left`, `Right` keys. Navigation up or down stairs happens automatically. The objective is to navigate to the treasure chest.

The default settings may have too many stairs for the user's taste. If so, select `Prefer Few Stairs` under the `Corridors` menu.

The `Save Map` option stores the map in a file server-side in a JSON format.

The `Download Map` lets the user download a map client-side in a JSON format.

#### How It Works:

Project Epsilon implements a variant of [Prim's Algorithm](https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm) to generate mazes. It works as follows.

Initialize the maze with all possible walls included and only a starting cell marked as open. As possible edges to add, mark all edges that are adjacent to the starting cell. Until all cells are included, pick a random edge that might be included to actually be included, mark both endpoints of edge as included, and mark all edges adjacent to those endpoints are unincludable, except those edges that have already been included.

The `Corridor` option allows the user to select how the random generation will be biased. The option, in particular, governs how a "random edge" noted above is chosen.

The complexity for maze generation is `O(n)`, where `n` is the number of cells (equal to the number of rows times columns times floors for a box-shaped maze) if the number of weight classes is considered constant. If not, then the complexity is `O(nc)`, where `n` is the number of cells and `c` is the number of weight classes.

#### Image Credits:

The stairs and treasure chest icon are provided by [Dungeon Crawl Stone Soup](https://opengameart.org/content/dungeon-crawl-32x32-tiles), available on [OpenGameArt](https://opengameart.org/).