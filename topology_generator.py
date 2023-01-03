import numpy as np
from itertools import product
from copy import deepcopy

class GraphConstructor(object):
    def __init__(self,path_names,path_seens,edge_history,vertex_history,loose_edges,future_loose_edges,did_something_flag):
        # list of strings
        # e.g. ["AB","AC","BC"]
        self.path_names = path_names

        # 2D array; path_seens[i,j] = path_names[i] has seen path_names[j]
        self.path_seens = path_seens 

        # list of lists of edges, edge is a list of path indices
        self.edge_history = edge_history

        # list of vertices, vertex is a tuplet of edge indices
        self.vertex_history = vertex_history

        # list of remaining edges, along with bools for if they passed
        self.loose_edges = loose_edges

        # list of loose edges in the next layer, along with bools for if they passed
        self.future_loose_edges = future_loose_edges

        # flag to show whether something was done at this layer
        self.did_something_flag = did_something_flag

    def step_construction(self):
        ##### NEXT LAYER #####
        if len(self.loose_edges) == 0:
            new_loose_edges = self.future_loose_edges
            new_future_loose_edges = []

            new_edge_history = deepcopy(self.edge_history)
            new_edge_history.append([])

            new_vertex_history = deepcopy(self.vertex_history)
            new_vertex_history.append([])

            new_constructor = GraphConstructor(
                self.path_names,
                self.path_seens,
                new_edge_history,
                new_vertex_history,
                new_loose_edges,
                new_future_loose_edges,
                False
            )
            return [new_constructor]
        #####

        graph_constructor_list = []

        ##### DO NOTHING #####
        if len(self.loose_edges) > 1 or self.did_something_flag:
            new_future_edge = (self.loose_edges[0][0],True)
            new_edge_history = deepcopy(self.edge_history)
            new_edge_history[-1] += [self.loose_edges[0][0]]
            new_constructor = GraphConstructor(
                self.path_names,
                self.path_seens,
                new_edge_history,
                self.vertex_history,
                self.loose_edges[1:],
                self.future_loose_edges + [new_future_edge],
                self.did_something_flag
            )
            graph_constructor_list.append(new_constructor)
        #####

        ##### SPLIT #####
        if self.can_split():
            paths = self.loose_edges[0][0]
            l = len(paths)
            combinations = product([False,True],repeat=l-1)
            for c in combinations:
                if sum(c) != 0:
                    c = [False]+list(c)
                    left_paths = [paths[i] for i in range(l) if c[i]]
                    right_paths = [paths[i] for i in range(l) if not(c[i])]
                    new_left_edge = (left_paths,False)
                    new_right_edge = (right_paths,False)

                    new_edge_history = deepcopy(self.edge_history)
                    new_edge_history[-1] += [left_paths,right_paths]

                    index_cur = len(self.edge_history[-2]) - len(self.loose_edges)
                    index_left = len(self.edge_history[-1])
                    index_right = index_left + 1

                    new_vertex = ([index_cur],[index_left,index_right])

                    new_vertex_history = deepcopy(self.vertex_history)
                    new_vertex_history[-1].append(new_vertex)

                    new_constructor = GraphConstructor(
                        self.path_names,
                        self.path_seens,
                        new_edge_history,
                        new_vertex_history,
                        self.loose_edges[1:],
                        self.future_loose_edges + [new_left_edge,new_right_edge],
                        True
                    )

                    graph_constructor_list.append(new_constructor)
        #####


        ##### MERGE #####
        for i in range(1,len(self.loose_edges)):
            if self.can_merge(i):
                new_paths = self.loose_edges[0][0] + self.loose_edges[i][0]
                new_edge = (new_paths,False)

                new_edge_history = deepcopy(self.edge_history)
                new_edge_history[-1] += [new_paths]

                index_left = len(self.edge_history[-2]) - len(self.loose_edges)
                index_right = i + index_left
                index_out = len(self.edge_history[-1])

                new_vertex = ([index_left,index_right],index_out)

                new_vertex_history = deepcopy(self.vertex_history)
                new_vertex_history[-1].append(new_vertex)

                new_path_seens = np.copy(self.path_seens)
                for left in self.loose_edges[0][0]:
                    for right in self.loose_edges[i][0]:
                        new_path_seens[left,right] = 1

                new_loose_edges = [self.loose_edges[k] for k in range(len(self.loose_edges)) if (k != 0 and k != i)]

                new_constructor = GraphConstructor(
                        self.path_names,
                        new_path_seens,
                        new_edge_history,
                        new_vertex_history,
                        new_loose_edges,
                        self.future_loose_edges + [new_edge],
                        True
                    )

                graph_constructor_list.append(new_constructor)
        #####

        ##### CONNECT #####
        for i in range(1,len(self.loose_edges)):
            if self.can_connect(i):
                new_loose_edges = [self.loose_edges[k] for k in range(len(self.loose_edges)) if (k != 0 and k != i)]

                new_constructor = GraphConstructor(
                        self.path_names,
                        self.path_seens,
                        self.edge_history,
                        self.vertex_history,
                        new_loose_edges,
                        self.future_loose_edges,
                        True
                    )

                graph_constructor_list.append(new_constructor)
        #####

        return graph_constructor_list
        

    def can_split(self) -> bool:
        "Can the first edge in self.loose_edges be split"
        if self.loose_edges[0][1]:
            return False

        return len(self.loose_edges[0][0]) > 1

    def can_merge(self,loose_index) -> bool:
        "Can the first and `loose_index` edge in self.loose_edges be merged"
        if self.loose_edges[0][1] and self.loose_edges[loose_index][1]:
            return False

        for left_path in self.loose_edges[0][0]:
            for right_path in self.loose_edges[loose_index][0]:
                if self.path_seens[left_path,right_path] or self.path_seens[right_path,left_path]:
                    return False

        return True

    def can_connect(self,loose_index) -> bool:
        "Can the first and `loose_index` edge in self.loose_edges be connected"
        if self.loose_edges[0][1] and self.loose_edges[loose_index][1]:
            return False

        return self.loose_edges[0][0] == self.loose_edges[loose_index][0]

# 4 vertices
test = GraphConstructor(
    ["AB","AC","AD","BC","BD","CD"],
    np.array([[1,1,1,1,1,0],[1,1,1,1,0,1],[1,1,1,0,1,1],[1,1,0,1,1,1],[1,0,1,1,1,1],[0,1,1,1,1,1]]),
    [[[0,1,2],[0,3,4],[1,3,5],[2,4,5]],[]],
    [[]],
    [([0,1,2],False),([0,3,4],False),([1,3,5],False),([2,4,5],False)],
    [],
    False
)

# 3 vertices
"""test = GraphConstructor(
    ["AB","AC","BC"],
    np.array([[1,1,1],[1,1,1],[1,1,1]]),
    [[[0,1],[0,2],[1,2]],[]],
    [[]],
    [([0,1],False),([0,2],False),([1,2],False)],
    [],
    False
)"""

test_list = [test]
out_list = []
count = 0
print("")
while count<1e8 and len(test_list)>0:
    count += 1
    print ("\033[A                             \033[A")
    print(f"{count}\t|\t{len(test_list)}\t|\t{len(out_list)}")
    cur = test_list.pop()
    if len(cur.loose_edges)==0 and len(cur.future_loose_edges)==0:
        out_list.append(cur)
    else:
        #print(i,"|",len(test_list))
        #print(cur.loose_edges)
        new_graphs = cur.step_construction()
        #for c in new_graphs:
            #print(f"\t{c.loose_edges}")
            #print(f"\t{c.future_loose_edges}")
            #print("__")
        test_list += new_graphs

print(len(out_list))
print(out_list[0].edge_history)
print(out_list[0].vertex_history)

with open("new_network_save.txt","w") as f:
    for n in out_list:
        f.write(f"{n.edge_history}|{n.vertex_history}\n")