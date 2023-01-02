class Graph:
    def __init__(self, graph_dict=None, is_oriented: bool = False):
        self.is_oriented = is_oriented
        self.graph_dict = graph_dict

    @property
    def is_oriented(self) -> bool:
        return self.__is_oriented

    @is_oriented.setter
    def is_oriented(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("is_oriented must be bool")
        self.__is_oriented = value

    @property
    def graph_dict(self):
        return self.__graph_dict

    @graph_dict.setter
    def graph_dict(self, graph_dict):
        if graph_dict is None:
            graph_dict = {}
        if not isinstance(graph_dict, dict):
            raise TypeError("graph_dict must be dict")
        self.__graph_dict = graph_dict

    def vertices(self):
        return list(self.__graph_dict.keys())

    def edges(self):
        return self.__generate_edges()

    def __generate_edges(self) -> list:
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def add_vertex(self, vertex):
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def count_vertex(self):
        return len(self.__graph_dict)

    def count_edges(self):
        if self.is_oriented:
            return len(self.__generate_edges())
        else:
            return len(self.__generate_edges()) // 2

    def add_edge(self, edge):
        if len(edge) != 2:
            raise ValueError("An edge must be a tuple of two elements")
        if edge[0] == edge[1]:
            raise ValueError("An edge cannot connect a vertex with itself")
        self.add_vertex(edge[0])
        self.add_vertex(edge[1])
        if self.__is_oriented:
            if edge[1] not in self.__graph_dict[edge[0]]:
                self.__graph_dict[edge[0]].append(edge[1])
        else:
            if edge[1] not in self.__graph_dict[edge[0]]:
                self.__graph_dict[edge[0]].append(edge[1])
            if edge[0] not in self.__graph_dict[edge[1]]:
                self.__graph_dict[edge[1]].append(edge[0])

    def random_change_oriented(self):
        global random
        if "random" not in globals():
            import random
        self.__is_oriented = random.choice([True, False])

    def random_create_graph(self, count_vertex: int = 10, chance: float = .25):
        global random
        if "random" not in globals():
            import random
        self.__graph_dict = {}
        for vertex in range(1, count_vertex + 1):
            self.add_vertex(vertex)
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict:
                if vertex != neighbour and random.random() < chance:
                    self.add_edge((vertex, neighbour))

    def __str__(self):
        return f"Graph is {'' if self.__is_oriented else 'not '}oriented\n" + \
               "\n".join(str(vertex) + ": " + ", ".join(str(neighbour) for neighbour in self.__graph_dict[vertex])
                         for vertex in self.__graph_dict)


if __name__ == "__main__":
    graph = Graph()
    graph.random_change_oriented()
    graph.random_create_graph()
    print(graph)
