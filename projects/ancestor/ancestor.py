class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        if v1 not in self.vertices:
            self.add_vertex(v1)

        if v2 not in self.vertices:
            self.add_vertex(v2)

        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        return self.vertices[vertex_id]

class AncestorTree():

    def __init__(self, node, depth = 0, parent_trees = None):
        self.node = node
        self.depth = depth
        if parent_trees is None:
            self.parent_trees = []
        else:
            self.parent_trees = parent_trees

    def add_node(self, parent_node, child_node):
        if self.parent_trees != []:
            max_depth = max({t.depth for t in self.parent_trees})
        else:
            max_depth = 0

        if child_node == self.node:
            if self.parent_trees == []:
                self.parent_trees.append(AncestorTree(parent_node))
                self.depth += 1
                return True, True

            if parent_node not in [t.node for t in self.parent_trees]:
                self.parent_trees.append(AncestorTree(parent_node))
                return True, False

        if self.parent_trees == []:
            return False, False

        for t in self.parent_trees:
            added_Q, depth_inc, = t.add_node(parent_node, child_node)
            if added_Q:
                if depth_inc and t.depth > max_depth:
                    self.depth += 1
                return added_Q, depth_inc

        return False, False

    def deepest_nodes(self):
        if self.parent_trees == []:
            return {self.node}

        max_depth = max({t.depth for t in self.parent_trees})

        return {n for t in self.parent_trees
                  for n in t.deepest_nodes()
                  if t.depth == max_depth}




def earliest_ancestor(ancestors, starting_node):
    a_graph = Graph()
    for p, c in ancestors:
        a_graph.add_edge(c, p)

    if a_graph.get_neighbors(starting_node) == set():
        return -1

    a_tree = AncestorTree(starting_node)
    stack = [starting_node]

    while stack != []:
        node = stack.pop()
        new_nodes = list(a_graph.get_neighbors(node))
        stack += new_nodes
        for n in new_nodes:
            a_tree.add_node(n, node)

    return min(a_tree.deepest_nodes())
