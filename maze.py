import random
import os

from werkzeug.datastructures import is_immutable

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
    def as_string(self):
        return "("+str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"
    # The key for the node that should appear in the dictionary of nodes
    def dict_key(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z)

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
        if not hasattr(self, "start_vertex_num"):
            self.start_vertex_num = 0 # Should generally be overwritten
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

def box(x,y,z,m,n,zz):
    return True

def taper(x,y,z,m,n,zz):
    distance_from_edge = min(x,y,m-1-y,n-1-x)
    max_cutoff = min((m-1)//2, (n-1)//2)
    return distance_from_edge >= max_cutoff * z/(zz-1)

def round(x,y,z,m,n,zz):
    return (m//2-y)**2/(m//2)**2 + (n//2-x)**2/(n//2)**2 <= 1

def get_starting_point(preferences):
    if (preferences["shape"]=="box"):
        return {"x":preferences["n"]//2, "y":preferences["m"]-1, "z":0}
    if (preferences["shape"]=="taper"):
        return {"x":preferences["n"]//2, "y":preferences["m"]-1, "z":0}
    if (preferences["shape"]=="round"):
        return {"x":preferences["n"]//2, "y":preferences["m"]-1, "z":0}
    return {"x":0,"y":0,"z":0} # Shouldn't hit this line.

# A non-rectangular 3D grid.
class GeneralGrid3D(DungeonGraph):
    def initnodes(self, *args):
        m, n, zz, node_function, = args[0]["m"], args[0]["n"], args[0]["z"], args[0]["node_function"]
        start_point = args[0]["start_point"]
        self.start_point = start_point
        self.num_nodes = 0
        self.node_function = node_function
        self.edge_dict = {} # A dictionary that makes it easy to look up edges by x,y,z coordinates
        self.nodes = []
        for i in range(m*n*zz):
            y,x,z = i//(n*zz),(i%(n*zz))//zz, i%zz
            if (self.node_present(x,y,z,m,n,zz)):
                self.num_nodes += 1
                self.nodes.append(Cell3D(x,y,z))
            dict_string = str(x)+","+str(y)+","+str(z)
            self.edge_dict[dict_string] = self.num_nodes - 1
        
        node_string = str(start_point["x"])+","+str(start_point["y"])+","+str(start_point["z"])
        self.start_point = start_point
        self.start_vertex_num = self.edge_dict[node_string]
    def node_present(self,x,y,z, m, n, zz):
        if (x<0 or x>=n or y<0 or y>=m or z<0 or z>=zz):
            return False
        return self.node_function(x,y,z,m,n,zz)
    def initedges(self, *args):
        m, n, zz = args[0]["m"], args[0]["n"], args[0]["z"]
        self.edges = []
        for i in range(self.num_nodes):
            x,y,z = self.nodes[i].x, self.nodes[i].y, self.nodes[i].z
            start_node = self.edge_dict[",".join([str(x),str(y),str(z)])]
            pn = [[x-1,y,z],[x+1,y,z],[x,y-1,z],[x,y+1,z],[x,y,z-1],[x,y,z+1]] # Possible neighbors, if they exist
            for j in range(len(pn)):
                if (self.node_present(pn[j][0],pn[j][1],pn[j][2],m,n,zz)):
                    end_node = self.edge_dict[",".join([str(pn[j][0]),str(pn[j][1]),str(pn[j][2])])]
                    if end_node > start_node:
                        self.edges.append(Edge(start_node, end_node))

weight_classes = {
    "none": {
        "Included":0,
        "Excluded":0,
        "Unavailable":0,
        "Long":1, # Would extend a corridor
        "Short":1, # Would not extend a corridor
        "Stairs":1
    },
    "long": {
        "Included":0,
        "Excluded":0,
        "Unavailable":0,
        "Long":5, # Would extend a corridor
        "Short":1, # Would not extend a corridor
        "Stairs":3
    },
    "short": {
        "Included":0,
        "Excluded":0,
        "Unavailable":0,
        "Long":1, # Would extend a corridor
        "Short":5, # Would not extend a corridor
        "Stairs":3
    },
    "few_stairs": {
        "Included":0,
        "Excluded":0,
        "Unavailable":0,
        "Long":5, # Would extend a corridor
        "Short":5, # Would not extend a corridor
        "Stairs":1
    }
}

class PartialGraph(DungeonGraph):
    # Set some variables at the start of the edge adding
    def set_variables(self, corridor_preference):
        self.corridor_preference = corridor_preference
        self.weights = {w:[] for w in weight_classes[corridor_preference]}
        self.weights_lengths = {w:0 for w in weight_classes[corridor_preference]}

    def set_distance(self):
        self.distances = [-1 for i in range(self.num_nodes)] # Distances from the starting point
        self.distances[self.start_vertex_num] = 0
        
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
            #print("Mismatch found in edge sampling: should be "+weight_class+" and is "+self.edges[edge_choice].status)
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
        old_node, new_node = endpoints[0], endpoints[1]
        for i in range(len(self.neighbors[endpoints[1]])):
            if self.neighbors[endpoints[1]][i].status == "Included" or endpoints[1] == self.start_vertex_num:
                new_node, old_node = endpoints[0], endpoints[1]
        # Include the new edge
        self.update_class(edge_num, "Included")
        # Assign new classes to edges adjacent to the new node
        for i in range(len(self.neighbors[new_node])):
            e = self.neighbors[new_node][i]
            if e.status not in ["Included","Excluded","Unavailable"]:
                self.update_class(e.index, "Excluded")
            if self.neighbors[new_node][i].status == "Unavailable":
                self.update_class(e.index, self.get_edge_class(e.index))
            self.distances[new_node] = self.distances[old_node] + 1
    
    # Meant to be overridden by the class defining specifically the graph.
    def get_edge_class(self, edge_num):
        pass
    
    def display_status(self):
        for key in weight_classes[self.corridor_preference]:
            print(key+": "+str(self.weights[key][:self.weights_lengths[key]]))
            pass

    def validate(self):
        for key in weight_classes[self.corridor_preference]:
            for i in range(self.weights_lengths[key]):
                e = self.edges[self.weights[key][i]]
                if e.status != key:
                    print("Mismatch found in validation")
                    pass

class PartialGrid3D(GeneralGrid3D, PartialGraph):
    def __init__(self, preferences):
        start_point = get_starting_point(preferences)
        preferences["node_function"] = {
            "box":box,
            "taper":taper,
            "round":round
        }[preferences["shape"]]
        preferences["start_point"] = start_point
        super(PartialGrid3D, self).__init__(preferences)

        self.set_variables(preferences["corridor_preference"])
        # Establish initial edge class allocation
        for i in range(len(self.edges)):
            self.edges[i].status = "Unavailable"
            if self.edges[i].start == self.start_vertex_num or self.edges[i].end == self.start_vertex_num:
                start_vertex = self.nodes[self.edges[i].start]
                end_vertex = self.nodes[self.edges[i].end]
                if (start_vertex.z != end_vertex.z):
                    self.edges[i].status = "Stairs"
                else:
                    self.edges[i].status = "Short"
            self.weights[self.edges[i].status].append(i)
            self.edges[i].status_index = self.weights_lengths[self.edges[i].status]
            self.weights_lengths[self.edges[i].status] += 1
            # Need index so we can identify by neighbor
            self.edges[i].index = i

    # Determine which edge class should be assigned to an edge
    def get_edge_class(self, edge_num):
        endpoints = [self.edges[edge_num].start, self.edges[edge_num].end]
        if self.nodes[endpoints[0]].z != self.nodes[endpoints[1]].z:
            return "Stairs"
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

    def get_treasure(self):
        farthest_nodes = []
        farthest_distance = 0
        for i in range(self.num_nodes):
            if self.distances[i] > farthest_distance:
                farthest_nodes = []
                farthest_distance = self.distances[i]
            if self.distances[i] == farthest_distance:
                farthest_nodes.append(i)
        random_node = self.nodes[farthest_nodes[int(random.uniform(0,len(farthest_nodes)))]]
        return {"x":random_node.x, "y":random_node.y, "z":random_node.z}
        
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
    return {
        "m":m,
        "n":n,
        "z":z,
        "do_save":req_data["do_save"],
        "room_size":req_data["room_size"],
        "corridor_preference":req_data["corridor_preference"],
        "shape":req_data["shape"]
    }

# Build a full 3D maze
def build_level3D(preferences):
    g = PartialGrid3D(preferences)
    g.set_distance()
    for i in range(g.num_nodes-1):
        g.assign_edge(g.edge_sample())
    treasure = g.get_treasure()
    max_floor = int(preferences["z"])
    room_size = int(preferences["room_size"])
    m,n = int(preferences["m"]), int(preferences["n"])
    
    # Initialize the full maze
    maze = []
    overlay = []
    start_point = {
        "x":g.start_point["x"]*(room_size+1),
        "y":g.start_point["y"]*(room_size+1)+1,
        "z":g.start_point["z"]
    }
    for i in range(max_floor):
        vertical_size = (room_size+1)*m
        maze.append(
            [
                ['outside' for j in range((room_size+1)*n-1)]
            for i in range(vertical_size)]
        )
        overlay.append(
            [
                ['nothing' for j in range((room_size+1)*n-1)]
            for i in range(vertical_size)]            
        )

    for i in range(m):
        for j in range(n):
            for ii in range(room_size):
                for jj in range(room_size):
                    for k in range(max_floor):
                        if (g.node_present(j,i,k,m,n,max_floor)):
                            maze[k][(room_size+1)*i+ii][(room_size+1)*j+jj] = 'floor'
                        else:
                            maze[k][(room_size+1)*i+ii][(room_size+1)*j+jj] = 'outside'
    
    # Knock out walls based on the grid defined above
    for i in range(len(g.edges)):
        if g.edges[i].status == "Included":
            node1 = g.nodes[g.edges[i].start]
            node2 = g.nodes[g.edges[i].end]
            offset = (min(node1.z, node2.z)%2)*(room_size-1)
            if node1.x == node2.x and node1.y != node2.y:
                for j in range(room_size):
                    maze[node1.z][(room_size+1)*max(node1.y,node2.y)-1][(room_size+1)*node1.x+j] = 'floor'
            elif node1.y == node2.y and node1.x != node2.x:
                for j in range(room_size):
                    maze[node1.z][(room_size+1)*node1.y+j][(room_size+1)*max(node1.x,node2.x)-1] = 'floor'
            elif node2.z > node1.z:
                maze[node1.z][(room_size+1)*node1.y+offset][(room_size+1)*node1.x+offset] = 'floor'
                maze[node2.z][(room_size+1)*node1.y+offset][(room_size+1)*node1.x+offset] = 'floor'
                overlay[node1.z][(room_size+1)*node1.y+offset][(room_size+1)*node1.x+offset] = "stairs_up"
                overlay[node2.z][(room_size+1)*node1.y+offset][(room_size+1)*node1.x+offset] = "stairs_down"
            elif node2.z < node1.z:
                maze[node1.z][(room_size+1)*node1.y+offset][(room_size+1)*node1.x+offset] = 'floor'
                maze[node2.z][(room_size+1)*node1.y+offset][(room_size+1)*node1.x+offset] = 'floor'
                overlay[node1.z][(room_size+1)*node1.y+offset][(room_size+1)*node1.x+offset] = "stairs_down"
                overlay[node2.z][(room_size+1)*node1.y+offset][(room_size+1)*node1.x+offset] = "stairs_up"
        else:
            node1 = g.nodes[g.edges[i].start]
            node2 = g.nodes[g.edges[i].end]
            if node1.x == node2.x and node1.y != node2.y:
                for j in range(room_size):
                    maze[node1.z][(room_size+1)*max(node1.y,node2.y)-1][(room_size+1)*node1.x+j] = 'wall'
            elif node1.y == node2.y and node1.x != node2.x:
                for j in range(room_size):
                    maze[node1.z][(room_size+1)*node1.y+j][(room_size+1)*max(node1.x,node2.x)-1] = 'wall'

    # Make the corners walls if necessary
    for i in range(m-1):
        for j in range(n-1):
            for k in range(max_floor):
                if g.node_present(j,i,k,m,n,max_floor) and g.node_present(j,i+1,k,m,n,max_floor) and g.node_present(j+1,i,k,m,n,max_floor) and g.node_present(j+1,i+1,k,m,n,max_floor):
                    maze[k][(room_size+1)*(i+1)-1][(room_size+1)*(j+1)-1] = 'wall'
    
    # Set the bottom of the tower to be an exit. Probably to be made more general later
    warps = []
    for i in range(len(maze[0][0])):
        if preferences["shape"] != "round":
            maze[0][len(maze[0])-1][i] = 'wall'
    for i in range(room_size):
        maze[0][len(maze[0])-1][i+(room_size+1)*g.start_point["x"]] = 'grass'
        warps.append({"x":i+(room_size+1)*g.start_point["x"],"y":len(maze[0])-1,"z":0})
    
    treasure_x = (room_size+1)*treasure["x"]
    treasure_y = (room_size+1)*treasure["y"]
    if (room_size > 1):
        treasure_x += 1
    overlay[treasure["z"]][treasure_y][treasure_x] = "treasure"
    return {"maze":maze, "overlay":overlay, "start_point":start_point, "warps":warps}

# Build the full maze, with multiple levels (if selected)
def build_maze3D(req_data, app):
    preferences = validate_input(req_data)
    do_save = preferences["do_save"]
    seed_string = str(req_data["location_x"])+"-"+str(req_data["location_y"])
    random.seed(seed_string)
    maze_data = build_level3D(preferences)
    
    # Process results
    result = {"tiles":maze_data["maze"], "overlay":maze_data["overlay"]}
    result["start_x"] = maze_data["start_point"]["x"]
    result["start_y"] = maze_data["start_point"]["y"]
    result["floor"] = maze_data["start_point"]["z"]
    result["warps"] = maze_data["warps"]
    result["location"] = {"x":req_data["location_x"],"y":req_data["location_y"]}
    result["map_type"] = "tower"
    if (do_save):
        path = app.instance_path+"/saved_maps"
        map_filename = "map"+str(len(os.listdir(path)))+".json"

        file1 = open(path+"/"+map_filename, "w")
        file1.write(str(result))
        file1.close()
    return result
