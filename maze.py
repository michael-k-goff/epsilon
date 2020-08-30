import random

# Base size of maze. Returned size is expanded to 2m-1 rows and 2n-1 columns
# To avoid some trivial base cases, assume m >= 2 and n >= 2
m = 10
n = 10

def build_maze():
    # Initial set of cells. Initially only (0,0) is added
    # 0 means not processed yet, 1 means in the queue, 2 means added
    cells = [
        [0 for j in range(n)]
    for i in range(m)]
    cells[0][0] = 2
    cells[0][1] = 1
    cells[1][0] = 1

    openable = [[0,1],[1,0]]
    num_openable = 2

     # Initialize the full maze
    maze = [
        ['wall' for j in range(2*n-1)]
    for i in range(2*m-1)]
    for i in range(m):
        for j in range(n):
            maze[2*i][2*j] = 'floor'

    for i in range(m*n-1):
        # Pick a cell to open next
        cell_num_to_open = random.randrange(num_openable)
        y = openable[cell_num_to_open][0]
        x = openable[cell_num_to_open][1]

        # Clear the cell out of the to-do list
        num_openable -= 1
        openable[cell_num_to_open] = openable[num_openable]
        cells[y][x] = 2

        # Get neighbors of the cell being opened and separate them by those
        # that have and have not been opened so far
        neighbors = []
        prev_neighbors = []
        if y>0:
            neighbors.append([y-1,x])
        if y<m-1:
            neighbors.append([y+1,x])
        if x>0:
            neighbors.append([y,x-1])
        if x<n-1:
            neighbors.append([y,x+1])
        for ii in range(len(neighbors)):
            if cells[neighbors[ii][0]][neighbors[ii][1]] == 2:
                prev_neighbors.append(neighbors[ii])
            elif cells[neighbors[ii][0]][neighbors[ii][1]] == 0:
                cells[neighbors[ii][0]][neighbors[ii][1]] = 1
                if len(openable) > num_openable:
                    openable[num_openable] = [ neighbors[ii][0], neighbors[ii][1] ]
                else:
                    openable.append( [neighbors[ii][0], neighbors[ii][1]] )
                num_openable += 1
        
        # Decide which of the previous neighbors will connect with the current cell
        # Should be at least 1 previous neighbor. Otherwise its a bug.
        prev_neighbor = random.randrange(len(prev_neighbors))
        py = prev_neighbors[prev_neighbor][0]
        px = prev_neighbors[prev_neighbor][1]
        if (px == x+1):
            maze[2*y][2*x+1] = 'floor'
        if (px == x-1):
            maze[2*y][2*x-1] = 'floor'
        if (py == y+1):
            maze[2*y+1][2*x] = 'floor'
        if (py == y-1):
            maze[2*y-1][2*x] = 'floor'

    return {"tiles":maze}