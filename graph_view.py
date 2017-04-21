from PyQt5 import QtWidgets, QtCore, QtGui

class View(QtWidgets.QGraphicsView):
    """Класс, отвечающий за работу окна, в котором рисуется граф."""
    def __init__(self, parent):
        QtWidgets.QGraphicsView.__init__(self, parent)
        self.setScene(QtWidgets.QGraphicsScene(self))
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
        self.vertices = list()

    edge_created = QtCore.pyqtSignal()

    def clear(self):
        self.scene().clear()
        self.vertices.clear()

    def draw_vertices(self):
        """Метод, рисующий все вершины графа."""
        for i in range(len(self.vertices)):
            node = QtWidgets.QGraphicsEllipseItem(self.vertices[i].x()-2, self.vertices[i].y()-2, 5, 5)
            node.setBrush(QtCore.Qt.black)
            self.scene().addItem(node)
            name = QtWidgets.QGraphicsTextItem('{}'.format(i))
            name.setPos(QtCore.QPointF(self.vertices[i].x() - 20, self.vertices[i].y() - 20))
            self.scene().addItem(name)

    def draw_edges(self):
        """Метод, рисующий все рёбра графа."""
        gray_pen = QtGui.QPen(QtGui.QColor(240, 240, 240))
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                line = QtWidgets.QGraphicsLineItem(QtCore.QLineF(self.vertices[i], self.vertices[j]))
                line.setPen(gray_pen)
                self.scene().addItem(line)
        self.edge_created.emit()

    def mouseReleaseEvent(self, event):
        """Метод, обрабатывающий сигнал нажатия мыши. Рисует вершину в кликнутой точке и рёбра, соединяющие её с другими вершинами."""
        self.scene().clear()
        point = QtCore.QPointF(self.mapToScene(event.pos()))
        self.vertices.append(point)
        if len(self.vertices) != 1:
            self.draw_edges()
        self.draw_vertices()

    def print_solution(self, route):
        """Метод, выделяющий на графе лучший путь, найденный алгоритмом."""
        route_pen = QtGui.QPen(QtCore.Qt.black, 2)
        for edge in route:
            line = QtWidgets.QGraphicsLineItem(QtCore.QLineF(QtCore.QPointF(self.vertices[edge[0]]), self.vertices[edge[1]]))
            line.setPen(route_pen)
            self.scene().addItem(line)