import sys
import random
import json
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPainter, QColor


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui.ui', self)

        # Инициализация списка окружностей и кофе
        self.circles = []
        self.coffee_list = []

        # Инициализация формы добавления/редактирования кофе
        self.add_edit_form = None

        # Подключение обработчиков событий
        self.btnAddCircle.clicked.connect(self.add_circle)
        self.btnEditCoffee.clicked.connect(self.open_add_edit_form)

        # Загрузка существующих данных кофе
        self.load_coffee_data()

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
        if self.add_edit_form is None or not self.add_edit_form.isVisible():
            try:
                self.add_edit_form = AddEditCoffeeForm(self)
                self.add_edit_form.exec_()
            except Exception as e:
                print(f"Ошибка при открытии формы добавления/редактирования кофе: {e}")

    def load_coffee_data(self):
        try:
            with open('coffee.json', 'r') as file:
                self.coffee_list = json.load(file)
                print("Данные о кофе загружены:", self.coffee_list)
        except FileNotFoundError:
            print("Файл с данными о кофе не найден. Создан новый файл.")
            self.coffee_list = []
        except json.JSONDecodeError:
            print("Ошибка чтения данных о кофе. Файл поврежден.")
            self.coffee_list = []

    def save_coffee_data(self):
        with open('coffee.json', 'w', encoding='utf-8') as file:
            json.dump(self.coffee_list, file, ensure_ascii=False)


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

        # Сохранение кофе в список родительского окна
        if coffee_name and coffee_type:
            coffee_entry = {'название кофе': coffee_name, 'тип кофе': coffee_type}
            self.parent().coffee_list.append(coffee_entry)
            self.parent().save_coffee_data()  # Сохраняем данные в файл
            print(f"Сохранено: {coffee_name}, Тип: {coffee_type}")
            self.close()
        else:
            print("Имя и тип кофе не могут быть пустыми.")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
