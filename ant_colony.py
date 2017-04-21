import math, random


class Ants:
    """Класс, отвечающий за работу алгоритма решения задачи коммивояжёра методом муравьиного интеллекта."""
    def __init__(self, parent):
        self.alpha = 1
        self.beta = 3
        self.Q = 5
        self.rho = 0.6
        self.vertices = None
        self.count_cities = None
        self.count_ants = None
        self.feromones = self.visions = None
        self.location = None
        self.unvisited_cities = None
        self.trails_len = None
        self.trails_route = None
        self.best_route = None
        self.best_len = math.inf

    def clear(self):
        self.vertices = self.count_cities = self.count_ants = self.feromones = self.visions = None
        self.location = self.unvisited_cities = self.trails_len = self.trails_route = self.best_route = None
        self.best_len = math.inf

    def set_problem(self, vertices, edges=None):
        """Метод, инициализирующий начальную конфигурацию. Устанавливает вершины, матрицы расстояний, видимости и феромонов."""
        self.vertices = vertices
        self.count_cities = len(vertices)
        self.count_ants = 100
        if not edges:
            self.distances = [[None for _ in range(len(vertices))] for _ in range(len(vertices))]
        else:
            self.distances = edges
        self.feromones = [[1 for _ in range(len(vertices))] for _ in range(len(vertices))]
        self.visions = [[None for _ in range(len(vertices))] for _ in range(len(vertices))]
        for i in range(len(vertices)):
            for j in range(i+1, len(vertices)):
                if not edges:
                    distance = math.sqrt((self.vertices[i].x() - self.vertices[j].x()) ** 2 + (self.vertices[i].y() - self.vertices[j].y()) ** 2)
                    self.distances[i][j] = distance
                    self.distances[j][i] = distance
                else:
                    distance = edges[i][j]
                self.visions[i][j] = 1 / distance
                self.visions[j][i] = 1 / distance

    def __init_ants(self):
        """Приватный метод, расставляющий муравьёв по вершинам."""
        self.location = [random.choice(range(self.count_cities)) for _ in range(self.count_ants)]
        self.unvisited_cities = [[city for city in range(self.count_cities) if city != self.location[ant]] for ant in range(self.count_ants)]
        self.trails_len = [0 for _ in range(self.count_ants)]
        self.trails_route = [list() for _ in range(self.count_ants)]

    def __generate_solutions(self):
        """Приватный метод, генерирующий решения всех установленных муравьёв."""
        for ant in range(self.count_ants):
            visited_cities = 1
            while visited_cities < self.count_cities:
                p = list()
                temp = sum(
                    [self.feromones[self.location[ant]][l] ** self.alpha * self.visions[self.location[ant]][l] ** self.beta for l
                     in self.unvisited_cities[ant]])
                for city in self.unvisited_cities[ant]:
                    p.append((self.feromones[self.location[ant]][city] ** self.alpha * self.visions[self.location[ant]][city] ** self.beta) / temp)
                chosen_city = random.choices(self.unvisited_cities[ant], weights=p)[0]
                self.trails_len[ant] += self.distances[self.location[ant]][chosen_city]
                self.trails_route[ant].append((self.location[ant], chosen_city))
                self.location[ant] = chosen_city
                self.unvisited_cities[ant].remove(chosen_city)
                visited_cities += 1
            self.trails_len[ant] += self.distances[self.trails_route[ant][-1][1]][self.trails_route[ant][0][0]]
            self.trails_route[ant].append((self.trails_route[ant][-1][1], self.trails_route[ant][0][0]))

    def __pheromones_update(self):
        """Приватный метод, обновляющий матрицу феромонов в соответствии с новыми решениями."""
        elite = 1
        for i in range(len(self.feromones)):
            for j in range(i + 1, len(self.feromones[i]) - 1):
                delta_feromones = 0
                for ant in range(self.count_ants):
                    if (i, j) in self.trails_route or (j, i) in self.trails_route:
                        delta_feromones += self.Q / self.trails_len[ant]
                    if (i, j) in self.best_route or (j, i) in self.best_route:
                        delta_feromones += (self.Q / self.trails_len[ant]) * (1+ elite)
                self.feromones[i][j] = self.feromones[j][i] = max([self.rho * self.feromones[i][j] + delta_feromones, 0.000001])

    def __best_variant(self):
        """Приватный метод, проверяющий, есть ли в сгенерированных решениях вариант, который лучше минимального решения, найденного на прошлых итерациях."""
        best_ant = min(range(len(self.trails_len)), key=self.trails_len.__getitem__)
        if self.best_len - self.trails_len[best_ant] > 0.001:
            self.best_len = self.trails_len[best_ant]
            self.best_route = self.trails_route[best_ant]

    def find_solution(self):
        """Основной метод, запускающий работу алгоритма."""
        for t in range(150):
            self.__init_ants()
            self.__generate_solutions()
            self.__best_variant()
            self.__pheromones_update()