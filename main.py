import sys, form, graph_view, ant_colony
from PyQt5 import QtWidgets, QtCore


class MainWindow(QtWidgets.QWidget):
    """Класс основного окна графического пользовательского интерфейса."""
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = form.Ui_Form()
        self.ui.setupUi(self)
        self.view = graph_view.View(self)
        self.ants = ant_colony.Ants(self)
        self.init_connections()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        self.ui.frame.setLayout(layout)
        self.distances = list()

    def init_connections(self):
        """Метод, инициализирующий соединения между сигналами и слотами."""
        self.ui.button_clear.clicked.connect(self.clear_view)
        self.ui.button_start.clicked.connect(self.button_start_clicked)
        self.ui.button_export.clicked.connect(self.export_to_txt)
        self.ui.button_import.clicked.connect(self.import_from_file_do)
        self.view.edge_created.connect(self.activate_buttons)

    def activate_buttons(self):
        """Метод, делающий доступными кнопки "Старт" и "Экспортировать граф в файл"."""
        self.ui.button_export.setEnabled(True)
        self.ui.button_start.setEnabled(True)

    def clear_view(self):
        """Метод, очищающий прошлые данные."""
        self.view.clear()
        self.ants.clear()
        self.ui.label_result.setText('Здесь будет выведен результат')
        self.ui.button_export.setEnabled(False)
        self.ui.button_start.setEnabled(False)
        self.distances.clear()

    def button_start_clicked(self):
        """Метод, запускающий алгоритм на графе, нарисованном в окне."""
        if not self.distances:
            self.ants.set_problem(self.view.vertices)
        else:
            self.ants.set_problem(self.view.vertices, self.distances)
        self.ants.find_solution()
        self.view.print_solution(self.ants.best_route)
        self.ui.label_result.setText('Длина маршрута: {}'.format(self.ants.best_len))
        self.distances = self.ants.distances

    def export_to_txt(self):
        """Метод, экспортирующий нарисованный граф в файл."""
        f_dialog = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', '', "Text files (*.txt)")
        file = open(f_dialog[0], 'w')
        file.write(str(len(self.view.vertices)) + '\n')
        for i in range(len(self.view.vertices)):
            file.write(str(i) + ' ' + str(self.view.vertices[i].x()) + ' ' + str(self.view.vertices[i].y()) + '\n')
        if self.distances:
            for i in range(len(self.view.vertices)):
                for j in range(i+1, len(self.view.vertices)):
                    file.write(str(i) + ' ' + str(j) + ' ' + str(self.distances[i][j]) + '\n')
        file.close()

    def import_from_file_do(self):
        """Метод, импортирующий граф из файла."""
        self.clear_view()
        f_dialog = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '',"Text files (*.txt)")
        file = open(f_dialog[0])
        line = file.readline()
        lst = line.strip().split()
        if len(lst) == 1:
            try:
                vertices = list()
                count = int(lst[0])
                for _ in range(count):
                    line = file.readline()
                    lst = line.strip().split()
                    if len(lst) == 3:
                        point = QtCore.QPointF(float(lst[1]), float(lst[2]))
                        vertices.append(point)
                line = file.readline()
                if line != '':
                    distances = [[None for _ in range(count)] for _ in range(count)]
                    for _ in range(int((count * count - count) / 2)):
                        lst = line.strip().split()
                        if len(lst) == 3:
                            distances[int(lst[0])][int(lst[1])] = float(lst[2])
                            distances[int(lst[1])][int(lst[0])] = float(lst[2])
                        line = file.readline()
                    if line == '':
                        correct = True
                        for i in range(count):
                            for j in range(i+1, count):
                                if not distances[i][j] or not distances[i][j]:
                                    correct = False
                                    break
                            if not correct:
                                break
                        if not correct:
                            return
                        else:
                            self.distances = distances
                file.close()
                self.view.vertices = vertices
                self.view.draw_edges()
                self.view.draw_vertices()
            except ValueError:
                error = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, 'Ошибка',
                                              'Неверный формат данных: ошибка типа данных.', QtWidgets.QMessageBox.Ok)
                error.exec()
                file.close()
        file.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())