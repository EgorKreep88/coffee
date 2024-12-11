import sys
import random
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPainter, QColor


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui.ui', self)

        # Инициализация списка окружностей
        self.circles = []

        # Инициализация формы добавления/редактирования кофе
        self.add_edit_form = None

        # Подключение обработчиков событий
        self.btnAddCircle.clicked.connect(self.add_circle)
        self.btnEditCoffee.clicked.connect(self.open_add_edit_form)

    def add_circle(self):
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        diameter = random.randint(20, 100)
        self.circles.append((color, diameter))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for color, diameter in self.circles:
            painter.setBrush(color)
            x = random.randint(0, self.width() - diameter)
            y = random.randint(0, self.height() - diameter)
            painter.drawEllipse(x, y, diameter, diameter)

    def open_add_edit_form(self):
        # Если форма уже открыта, ничего не делаем
        if self.add_edit_form is None or not self.add_edit_form.isVisible():
            # Создание и отображение формы добавления/редактирования кофе
            try:
                self.add_edit_form = AddEditCoffeeForm(self)
                self.add_edit_form.exec_()  # Используем exec_() для модального диалога
            except Exception as e:
                print(f"Ошибка при открытии формы добавления/редактирования кофе: {e}")


class AddEditCoffeeForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddEditCoffeeForm, self).__init__(parent)
        try:
            uic.loadUi('addEditCoffeeForm.ui', self)
        except Exception as e:
            print(f"Ошибка загрузки UI: {e}")
            sys.exit(1)

        # Подключение обработчиков событий
        self.btnSave.clicked.connect(self.save_coffee)
        self.btnCancel.clicked.connect(self.close)

    def save_coffee(self):
        coffee_name = self.lineEditCoffeeName.text()
        coffee_type = self.lineEditCoffeeType.text()
        print(f"Сохранено: {coffee_name}, Тип: {coffee_type}")
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
