import random
import os

# Meant to be the general node class for a cell in the grid.
class Node:
    def __init__(self, *args):
        pass
    def display(self):
        pass

class Cell3D(Node):
    def __init__(self, *args):
        self.x = args[0]
        self.y = args[1]
        self.z = args[2]
    def display(self):
        print("Grid cell. X: "+str(self.x)+", Y: "+str(self.y)+", Z: "+str(self.z))

class Edge:
    def __init__(self,start,end,directed=False):
        self.start = start
        self.end = end
        self.directed = directed # Not sure if and how this will be used
    def display(self):
        print("Edge from "+str(self.start)+" to "+str(self.end))

class DungeonGraph:
    def __init__(self, *args): # Should generally not be overridden
        self.initnodes(*args)
        self.initedges(*args)
        self.initincidences(*args)
    def initnodes(self, *args): # Should be overridden in general
        self.num_nodes = 0
    def initedges(self, *args): # Should be overridden in general
        self.edges = []
    # Given nodes and edges, set up which edges are incident to which nodes.
    # Should generally not be overridden
    def initincidences(self, *args):
        self.neighbors = [[] for i in range(self.num_nodes)]
        for i in range(len(self.edges)):
            self.neighbors[self.edges[i].start].append(self.edges[i])
            self.neighbors[self.edges[i].end].append(self.edges[i])

# For a general 3D dungeon
class Grid3D(DungeonGraph):
    def initnodes(self, *args):
        m, n, z = args[0], args[1], args[2]
        self.num_nodes = m*n*z
        self.nodes = [Cell3D(i//(n*z),(i%(n*z))//z, i%z) for i in range(m*n*z)]
    def initedges(self, *args):
        m, n, z = args[0], args[1], args[2]
        self.edges = []
        for i in range(m):
            for j in range(n):
                for k in range(z-1):
                    self.edges.append(Edge(i*n*z + j*z + k, i*n*z + j*z + k+1))
        for i in range(m):
            for j in range(n-1):
                for k in range(z):
                    self.edges.append(Edge(i*n*z + j*z + k, i*n*z + (j+1)*z + k))
        for i in range(m-1):
            for j in range(n):
                for k in range(z):
                    self.edges.append(Edge(i*n*z + j*z + k, (i+1)*n*z + j*z + k))

weight_classes = {
    "none": {
        "Included":0,
        "Excluded":0,
        "Unavailable":0,
        "Long":1, # Would extend a corridor
        "Short":1 # Would not extend a corridor
    },
    "long": {
        "Included":0,
        "Excluded":0,
        "Unavailable":0,
        "Long":5, # Would extend a corridor
        "Short":1 # Would not extend a corridor
    },
    "short": {
        "Included":0,
        "Excluded":0,
        "Unavailable":0,
        "Long":1, # Would extend a corridor
        "Short":5 # Would not extend a corridor
    }
}

class PartialGraph(DungeonGraph):
    # Set some variables at the start of the edge adding
    def set_variables(self, corridor_preference):
        self.corridor_preference = corridor_preference
        self.weights = {w:[] for w in weight_classes[corridor_preference]}
        self.weights_lengths = {w:0 for w in weight_classes[corridor_preference]}

    # Sample an edge that can be added to graph 
    def edge_sample(self):
        full_weight = sum([weight_classes[self.corridor_preference][key]*self.weights_lengths[key] for key in weight_classes[self.corridor_preference]])
        sampler = random.uniform(0,full_weight)
        weight_class = "Unavailable" # Should always be overwritten; otherwise it's a bug
        for key in weight_classes[self.corridor_preference]:
            if weight_classes[self.corridor_preference][key]*self.weights_lengths[key] > 0:
                weight_class = key
            if sampler < weight_classes[self.corridor_preference][key]*self.weights_lengths[key]:
                break
            sampler -= weight_classes[self.corridor_preference][key]*self.weights_lengths[key]
        edge_choice = self.weights[weight_class][int(sampler//weight_classes[self.corridor_preference][weight_class])]
        if (self.edges[edge_choice].status != weight_class):
            print("Mismatch found in edge sampling: should be "+weight_class+" and is "+self.edges[edge_choice].status)
            self.validate()
        return edge_choice

    # Assign a new weight class to an edge, updating all indices as needed
    def update_class(self, edge_num, new_class):
        # Old edge data
        old_class = self.edges[edge_num].status
        old_pos = self.edges[edge_num].status_index

        # Update old weight class
        self.weights_lengths[old_class] -= 1
        self.weights[old_class][old_pos] = self.weights[old_class][self.weights_lengths[old_class]]
        self.edges[self.weights[old_class][old_pos]].status_index = old_pos

        # Update new weight class
        self.weights_lengths[new_class] += 1
        if (len(self.weights[new_class]) < self.weights_lengths[new_class]):
            self.weights[new_class].append(edge_num)
        else:
            self.weights[new_class][self.weights_lengths[new_class]-1]=edge_num
        
        # Set new edge data
        self.edges[edge_num].status = new_class
        self.edges[edge_num].status_index = self.weights_lengths[new_class]-1

    def assign_edge(self, edge_num):
        # Figure out which endpoint is the new one.
        endpoints = [self.edges[edge_num].start, self.edges[edge_num].end]
        new_node = endpoints[1]
        for i in range(len(self.neighbors[endpoints[1]])):
            if self.neighbors[endpoints[1]][i].status == "Included":
                new_node = endpoints[0]
        # Include the new edge
        self.update_class(edge_num, "Included")
        # Assign new classes to edges adjacent to the new node
        for i in range(len(self.neighbors[new_node])):
            e = self.neighbors[new_node][i]
            if e.status not in ["Included","Excluded","Unavailable"]:
                self.update_class(e.index, "Excluded")
            if self.neighbors[new_node][i].status == "Unavailable":
                self.update_class(e.index, self.get_edge_class(e.index))
    
    # Meant to be overridden by the class defining specifically the graph.
    def get_edge_class(self, edge_num):
        pass
    
    def display_status(self):
        for key in weight_classes[self.corridor_preference]:
            print(key+": "+str(self.weights[key][:self.weights_lengths[key]]))

    def validate(self):
        for key in weight_classes[self.corridor_preference]:
            for i in range(self.weights_lengths[key]):
                e = self.edges[self.weights[key][i]]
                if e.status != key:
                    print("Mismatch found in validation")

class PartialGrid3D(Grid3D, PartialGraph):
    def __init__(self, m,n,z, corridor_preference):
        super(PartialGrid3D, self).__init__(m,n,z)
        self.set_variables(corridor_preference)
        # Establish initial edge class allocation
        for i in range(len(self.edges)):
            self.edges[i].status = "Unavailable"
            if self.edges[i].start == 0 or self.edges[i].end == 0:
                self.edges[i].status = "Short"
            self.weights[self.edges[i].status].append(i)
            self.edges[i].status_index = self.weights_lengths[self.edges[i].status]
            self.weights_lengths[self.edges[i].status] += 1
            # Need index so we can identify by neighbor
            self.edges[i].index = i

    # Determine which edge class should be assigned to an edge
    # Will update in the 3D case later.
    def get_edge_class(self, edge_num):
        endpoints = [self.edges[edge_num].start, self.edges[edge_num].end]
        for i in range(len(self.neighbors[endpoints[0]])):
            outer_edge = self.neighbors[endpoints[0]][i]
            if outer_edge.status == "Included":
                outer_node = outer_edge.start
                if outer_node == endpoints[0]:
                    outer_node = outer_edge.end
                if self.nodes[outer_node].x == self.nodes[endpoints[1]].x:
                    return "Long"
                if self.nodes[outer_node].y == self.nodes[endpoints[1]].y:
                    return "Long"
        for i in range(len(self.neighbors[endpoints[1]])):
            outer_edge = self.neighbors[endpoints[1]][i]
            if outer_edge.status == "Included":
                outer_node = outer_edge.start
                if outer_node == endpoints[1]:
                    outer_node = outer_edge.end
                if self.nodes[outer_node].x == self.nodes[endpoints[0]].x:
                    return "Long"
                if self.nodes[outer_node].y == self.nodes[endpoints[0]].y:
                    return "Long"
        return "Short"
        
def validate_input(req_data):
    m = req_data["x"]
    n = req_data["y"]
    z = req_data["z"]
    # Validation of m and n should occur before form submission, but some is here too.
    # To avoid some trivial base cases, assume m >= 2 and n >= 2
    if not m.isnumeric():
        m = 5
    else:
        m = int(m)
        m = max(2,min(50,m))
    if not n.isnumeric():
        n = 5
    else:
        n = int(n)
        n = max(2,min(50,n))
    if not z.isnumeric():
        z = 1
    else:
        z = int(z)
        z = max(1,min(50,z))
    return m, n, req_data["do_save"], int(req_data["room_size"]), req_data["corridor_preference"], z

# Build a full 3D maze
def build_level3D(m, n, corridor_preference, room_size, max_floor):
    g = PartialGrid3D(m,n,max_floor, corridor_preference)
    for i in range(m*n*max_floor-1):
        g.assign_edge(g.edge_sample())
        #g.validate()
    
    # Initialize the full maze
    maze = []
    for i in range(max_floor):
        maze.append(
            [
                ['wall' for j in range((room_size+1)*n-1)]
            for i in range((room_size+1)*m-1)]
        )

    for i in range(m):
        for j in range(n):
            for ii in range(room_size):
                for jj in range(room_size):
                    for k in range(max_floor):
                        maze[k][(room_size+1)*i+ii][(room_size+1)*j+jj] = 'floor'
    
    # Knock out walls based on the grid defined above
    for i in range(len(g.edges)):
        if g.edges[i].status == "Included":
            node1 = g.nodes[g.edges[i].start]
            node2 = g.nodes[g.edges[i].end]
            offset = (min(node1.z, node2.z)%2)*(room_size-1)
            if node1.x == node2.x and node1.y != node2.y:
                for j in range(room_size):
                    maze[node1.z][(room_size+1)*node1.x+j][(room_size+1)*max(node1.y,node2.y)-1] = 'floor'
            elif node1.y == node2.y and node1.x != node2.x:
                for j in range(room_size):
                    maze[node1.z][(room_size+1)*max(node1.x,node2.x)-1][(room_size+1)*node1.y+j] = 'floor'
            elif node2.z > node1.z:
                maze[node1.z][(room_size+1)*node1.x+offset][(room_size+1)*node1.y+offset] = "stairs_up"
                maze[node2.z][(room_size+1)*node1.x+offset][(room_size+1)*node1.y+offset] = "stairs_down"
            elif node2.z < node1.z:
                maze[node1.z][(room_size+1)*node1.x+offset][(room_size+1)*node1.y+offset] = "stairs_down"
                maze[node2.z][(room_size+1)*node1.x+offset][(room_size+1)*node1.y+offset] = "stairs_up"
    return maze

# Build the full maze, with multiple levels (if selected)
def build_maze3D(req_data, app):
    m, n, do_save, room_size, corridor_preference, z = validate_input(req_data)
    maze = build_level3D(m,n,corridor_preference,room_size,z)
    
    # Process results
    result = {"tiles":maze}
    result["start_x"] = len(result["tiles"][0])-1
    result["start_y"] = 0
    result["floor"] = 0
    if (do_save):
        path = app.instance_path+"/saved_maps"
        map_filename = "map"+str(len(os.listdir(path)))+".json"
        print(map_filename)

        file1 = open(path+"/"+map_filename, "w")
        file1.write(str(result))
        file1.close()
    return result
