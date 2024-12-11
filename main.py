import sys
import random
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui.ui', self)

        # Инициализация списка окружностей
        self.circles = []

        # Подключение обработчиков событий
        self.btnAddCircle.clicked.connect(self.add_circle)
        self.btnEditCoffee.clicked.connect(self.open_add_edit_form)

    def add_circle(self):
        # Генерация случайного цвета и диаметра
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        diameter = random.randint(20, 100)

        # Добавление окружности в список
        self.circles.append((color, diameter))

        # Перерисовка виджета
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for color, diameter in self.circles:
            painter.setBrush(color)
            # Рисуем окружность в случайном месте
            x = random.randint(0, self.width() - diameter)
            y = random.randint(0, self.height() - diameter)
            painter.drawEllipse(x, y, diameter, diameter)

    def open_add_edit_form(self):
        # Создание и отображение формы добавления/редактирования кофе
        self.add_edit_form = AddEditCoffeeForm()
        self.add_edit_form.show()


class AddEditCoffeeForm(QtWidgets.QWidget):
    def __init__(self):
        super(AddEditCoffeeForm, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)

        # Подключение обработчиков событий
        self.btnSave.clicked.connect(self.save_coffee)
        self.btnCancel.clicked.connect(self.close)

    def save_coffee(self):
        # Здесь вы можете добавить логику для сохранения кофе в базу данных
        # Например, извлечение данных из полей и их сохранение
        coffee_name = self.lineEditCoffeeName.text()
        coffee_type = self.lineEditCoffeeType.text()
        print(f"Сохранено: {coffee_name}, Тип: {coffee_type}")
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
