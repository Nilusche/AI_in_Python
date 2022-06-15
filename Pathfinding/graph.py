from cmath import inf
from copy import deepcopy
from queue import PriorityQueue
from prettytable import PrettyTable
from Queue import *
from utils import * 

class Node:

    def __init__(self, name):
        self.parent = 0
        self.name = name
        self.edges = []
        self.value = 0
    def __str__(self):
        return str(self.name)

    def __eq__(self, other):
        return self.name == other.name 
    
    def __gt__(self, other):
        return self.value >= other.value
    
    def __get_item__(self):
        return self.value

    def __hash__(self):
        return id(self)

class Edge:

    def __init__(self, edge):
        self.start = edge[0]
        self.end = edge[1]
        self.value = edge[2]


class Graph:

    def __init__(self, node_list, edges):
        self.num_of_nodes = len(node_list)
        self.nodes = []
        for name in node_list:
            self.nodes.append(Node(name))

        for e in edges:
            e = (getNode(e[0],self.nodes), getNode(e[1], self.nodes), e[2])        

            self.nodes[next((i for i,v in enumerate(self.nodes) if v.name == e[0].name), -1)].edges.append(Edge(e))
            self.nodes[next((i for i,v in enumerate(self.nodes) if v.name == e[1].name), -1)].edges.append(Edge((e[1], e[0], e[2])))

    def __get_node_value(self, nodename):
        for i in self.nodes:
            if i.name == nodename:
                return i.value
    def __set_node_value(self, nodename, value):
        for i in self.nodes:
            if i.name == nodename:
                i.value = value

    def print(self):
        node_list = self.nodes
        
        t = PrettyTable(['  '] +[i.name for i in node_list])
        for node in node_list:
            edge_values = ['X'] * len(node_list)
            for edge in node.edges:
                edge_values[ next((i for i,e in enumerate(node_list) if e.name == edge.end.name) , -1)] = edge.value           
            t.add_row([node.name] + edge_values)
        print(t)

    #Utility function: find node
    def __find(self, nodename):
        for i in self.nodes:
            if i.name == nodename:
                return i
    #Utility function: Array of visited nodes            
    def __make_visited_array(self):
        visited = {}
        for i in self.nodes:
            if i.name not in visited:
                visited[i.name] = False

        return visited
    
    #Utility function: Map of Nodepaths
    def __make_path_array(self):
        path = {}
        for i in self.nodes:
            if i.name not in path:
                path[i.name] = []
        return path

    #Utility  function: Printing Node with Edge
    def __print_node_with_edge(self, node:Node):
        edges = ""
        for i in node.edges:
            edges += i.end.name + "["+str(i.value)+ "] "
        print(node.name, ": ", edges)

    #Backtrack path
    def __backtrack_path(self, current_vertex, came_from):
        tmp = [] 
        sum = 0
        tmp.append(current_vertex.name)
        while current_vertex in came_from:  
            for edge in current_vertex.edges:
                if edge.end.name == came_from[current_vertex].name:
                    sum+=edge.value   
            current_vertex = came_from[current_vertex]
             
            tmp.append(current_vertex.name)
            
        tmp.reverse()
        return sum, tmp

    #Breadth first search
    def bfs(self,start, end):
        print("Running BFS: from ", start, " to ", end)
        queue = Queue("FIFO")
        accumulated_cost=0 
        visited = self.__make_visited_array()
        traversal_path = []
        came_from ={}
        #push starting vertex into queue and visit it
        queue.push(self.__find(start))    

        while not queue.is_empty():
            #Safe vertex into path
            current_vertex = queue.pop() 
            visited[current_vertex.name] = True
            traversal_path.append(current_vertex.name)
            accumulated_cost+= current_vertex.value

            self.__print_node_with_edge(current_vertex)
            #If destination vertex has been found
            if current_vertex.name == end:
                path_cost, backtrackpath = self.__backtrack_path(current_vertex,came_from)
                break
            
            #print("Visited :", current_vertex.name)

            for adjacent_node in current_vertex.edges:
                if visited[adjacent_node.end.name] == False:
                    adjacent_node.end.value = adjacent_node.value
                    queue.push(adjacent_node.end)
                    came_from[adjacent_node.end] =current_vertex
                    if adjacent_node.end.name == end:
                        break
                
        print("Accumulated Cost: " ,accumulated_cost)
        print("Traversal Path: ", traversal_path)
        print("Path Cost:" , path_cost)
        print("Path: ", backtrackpath)
    
    #Depth first search
    def dfs(self, start, end):
        print("Running DFS: from ", start, " to ", end)
        queue = Queue("LIFO")
        accumulated_cost=0
        visited = self.__make_visited_array()
        traversal_path = []
        came_from = {}
        #push starting vertex into queue and visit it
        queue.push(self.__find(start))

        while not queue.is_empty():
            #Safe vertex into path
            current_vertex = queue.pop() 
            visited[current_vertex.name] = True
            traversal_path.append(current_vertex.name)
            accumulated_cost+= current_vertex.value
            self.__print_node_with_edge(current_vertex)

            #If destination vertex has been found
            if current_vertex.name == end:
                path_cost, backtrackpath = self.__backtrack_path(current_vertex,came_from)
                break
            
            for adjacent_node in current_vertex.edges:
                if visited[adjacent_node.end.name] == False:
                    adjacent_node.end.value = adjacent_node.value
                    queue.push(adjacent_node.end)
                    came_from[adjacent_node.end] =current_vertex
                    if adjacent_node.end.name == end:
                        break
        
        

        print("Accumulated Cost: " ,accumulated_cost)
        print("Traversal Path: ", traversal_path)
        print("Path Cost:" , path_cost)
        print("Path: ", backtrackpath)

    #Uniform cost search (Dijkstra variation)
    def ucs(self, start, end):
        print("Running UCS: from ", start, " to ", end)
        path = self.__make_path_array()
        queue = Queue("PRIO", False)
        visited = self.__make_visited_array()
        #Set all initial distances to infinity except for the starting node
        for i in self.nodes:
            if i.name ==start:
                i.value = 0 
            else:
                i.value = float("inf")

        #Initial start distance initialization, Path initialization
        queue.push(self.__find(start))
        path[start] = [self.__find(start)]
        
        while not queue.is_empty():
            current = queue.pop()
            #If Goal has been reached then return Solution state
            if current.name == end:
                break;
            #Explore current node
            visited[current.name] = True

            for child in current.edges:
                childnode = self.__find(child.end.name);
                if visited[childnode.name] == False:
                    queue.push(childnode)
                    if self.__get_node_value(childnode.name)> self.__get_node_value(current.name) + child.value:
                        self.__set_node_value(childnode.name, self.__get_node_value(current.name) + child.value)
                        path[childnode.name] = deepcopy(path[current.name])
                        path[childnode.name].append(childnode)



        #Printing Path
        path = { k:v for k,v in path.items() if v is not None}
        p ="Path: "
        for j in path[end]:
                p+= j.name +" -> "
        print(p.rstrip(" ->"))
        print("Cost: ", self.__get_node_value(end))

        
        
        
           



