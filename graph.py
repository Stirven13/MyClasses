import math

from PIL import Image, ImageDraw, ImageFont


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
        if not self.is_oriented:
            for vertex in graph_dict:
                for neighbour in graph_dict[vertex]:
                    if vertex not in graph_dict[neighbour]:
                        graph_dict[neighbour].append(vertex)
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
                self.__graph_dict[edge[0]].sort()
        else:
            if edge[1] not in self.__graph_dict[edge[0]]:
                self.__graph_dict[edge[0]].append(edge[1])
                self.__graph_dict[edge[0]].sort()
            if edge[0] not in self.__graph_dict[edge[1]]:
                self.__graph_dict[edge[1]].append(edge[0])
                self.__graph_dict[edge[1]].sort()

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

    def draw(self, filename: str):
        width, height = 600, 600
        radius = 20
        distance = 250

        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        vertices = self.vertices()
        n = len(vertices)

        list_cos_sin = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n)]
        coordinates_vertices = [(int(width / 2 + distance * list_cos_sin[i][0]),
                                 int(height / 2 + distance * list_cos_sin[i][1]))
                                for i in range(n)]

        for vertex, neighbours in self.graph_dict.items():
            x1, y1 = coordinates_vertices[vertex - 1]
            for neighbour in neighbours:
                x2, y2 = coordinates_vertices[neighbour - 1]
                draw.line((x1, y1, x2, y2), fill="black")
                if self.is_oriented:
                    angle = math.atan2(y2 - y1, x2 - x1)
                    arrow_cursor = x2 - (radius + 3) * math.cos(angle), y2 - (radius + 3) * math.sin(angle)
                    left_part_arrow = (arrow_cursor[0] - 5 * math.cos(angle + math.pi / 6),
                                       arrow_cursor[1] - 5 * math.sin(angle + math.pi / 6))
                    right_part_arrow = (arrow_cursor[0] - 5 * math.cos(angle - math.pi / 6),
                                        arrow_cursor[1] - 5 * math.sin(angle - math.pi / 6))

                    draw.polygon((arrow_cursor, left_part_arrow, right_part_arrow), fill="black")

        font = ImageFont.truetype("arial.ttf", 20)

        for i, vertex in enumerate(vertices):
            x, y = coordinates_vertices[i]
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="black")
            draw.text((x, y), str(vertex), fill="white", anchor="mm", font=font)

        image.save(filename)


if __name__ == "__main__":
    graph = Graph()
    graph.random_change_oriented()
    graph.random_create_graph(10, .5)
    print(graph)
    # Erace # to draw graph
    # graph.draw("graph.png")
