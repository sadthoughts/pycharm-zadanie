import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton,
                             QComboBox, QTableWidget, QTableWidgetItem,
                             QHeaderView, QGridLayout, QMessageBox)
from PyQt5.QtCore import Qt


class CropBalanceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Основные данные
        self.crop_yields = {
            'подсолнечник': 35,
            'ячмень': 30,
            'пшеница': 31
        }
        self.starting_balance = 2000  # Остаток на начало периода

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной вертикальный layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Заголовок
        title_label = QLabel('Баланс продукции растениеводства')
        title_label.setStyleSheet('font-size: 16px; font-weight: bold;')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Создаем форму ввода данных
        form_layout = QGridLayout()

        # Выбор культуры
        form_layout.addWidget(QLabel('Тип культуры:'), 0, 0)
        self.crop_combo = QComboBox()
        self.crop_combo.addItems(['подсолнечник', 'ячмень', 'пшеница'])
        self.crop_combo.currentTextChanged.connect(self.update_yield)
        form_layout.addWidget(self.crop_combo, 0, 1)

        # Урожайность (только чтение)
        form_layout.addWidget(QLabel('Урожайность, ц/га:'), 1, 0)
        self.yield_label = QLabel('35')
        self.yield_label.setStyleSheet('background-color: #f0f0f0; padding: 5px;')
        form_layout.addWidget(self.yield_label, 1, 1)

        # Площадь посева
        form_layout.addWidget(QLabel('Площадь посева, га:'), 2, 0)
        self.area_input = QLineEdit()
        self.area_input.setPlaceholderText('Введите площадь')
        form_layout.addWidget(self.area_input, 2, 1)

        # Кнопка и поле для объема производства
        production_button = QPushButton('Объем производства')
        production_button.clicked.connect(self.calculate_production)
        form_layout.addWidget(production_button, 3, 0)

        self.production_output = QLineEdit()
        self.production_output.setReadOnly(True)
        self.production_output.setPlaceholderText('Результат расчета')
        form_layout.addWidget(self.production_output, 3, 1)

        # Объем приобретения
        form_layout.addWidget(QLabel('Объем приобретения, ц:'), 4, 0)
        self.purchase_input = QLineEdit()
        self.purchase_input.setPlaceholderText('Введите объем приобретения')
        form_layout.addWidget(self.purchase_input, 4, 1)

        # Объем реализации работникам
        form_layout.addWidget(QLabel('Реализация работникам, ц:'), 5, 0)
        self.sale_staff_input = QLineEdit()
        self.sale_staff_input.setPlaceholderText('Введите объем')
        form_layout.addWidget(self.sale_staff_input, 5, 1)

        # Объем реализации сторонним организациям
        form_layout.addWidget(QLabel('Реализация организациям, ц:'), 6, 0)
        self.sale_org_input = QLineEdit()
        self.sale_org_input.setPlaceholderText('Введите объем')
        form_layout.addWidget(self.sale_org_input, 6, 1)

        # Кнопка и поле для общего объема реализации
        total_sale_button = QPushButton('Общий объем реализации')
        total_sale_button.clicked.connect(self.calculate_total_sales)
        form_layout.addWidget(total_sale_button, 7, 0)

        self.total_sale_output = QLineEdit()
        self.total_sale_output.setReadOnly(True)
        self.total_sale_output.setPlaceholderText('Результат расчета')
        form_layout.addWidget(self.total_sale_output, 7, 1)

        # На семена
        form_layout.addWidget(QLabel('На семена, ц:'), 8, 0)
        self.seeds_input = QLineEdit()
        self.seeds_input.setPlaceholderText('Введите объем на семена')
        form_layout.addWidget(self.seeds_input, 8, 1)

        main_layout.addLayout(form_layout)

        # Кнопка расчета баланса
        balance_button = QPushButton('Баланс продукции')
        balance_button.clicked.connect(self.show_balance)
        balance_button.setStyleSheet('background-color: #4CAF50; color: white; padding: 10px;')
        main_layout.addWidget(balance_button)

        # Таблица баланса
        self.balance_table = QTableWidget(5, 2)
        self.balance_table.setHorizontalHeaderLabels(['Направление', 'Значение, ц'])
        self.balance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Заполняем названия строк
        table_items = [
            'Остаток на начало периода',
            'Произведено',
            'Приобретено',
            'Реализация',
            'На семена'
        ]

        for i, item in enumerate(table_items):
            self.balance_table.setItem(i, 0, QTableWidgetItem(item))

        main_layout.addWidget(self.balance_table)

        # Остаток на конец периода
        self.ending_balance_label = QLabel('Остаток на конец периода: -- ц')
        self.ending_balance_label.setStyleSheet('font-weight: bold; font-size: 14px;')
        main_layout.addWidget(self.ending_balance_label)

        # Настройка окна
        self.setWindowTitle('Баланс продукции растениеводства')
        self.setGeometry(100, 100, 600, 700)

        # Инициализируем урожайность
        self.update_yield()

    def update_yield(self):
        """Обновляет значение урожайности при смене культуры"""
        crop = self.crop_combo.currentText()
        self.yield_label.setText(str(self.crop_yields[crop]))

    def calculate_production(self):
        """Рассчитывает объем производства"""
        try:
            area = float(self.area_input.text().replace(',', '.'))
            crop = self.crop_combo.currentText()
            yield_value = self.crop_yields[crop]
            production = area * yield_value
            self.production_output.setText(f'{production:.2f}')
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Введите корректную площадь посева')

    def calculate_total_sales(self):
        """Рассчитывает общий объем реализации"""
        try:
            sale_staff = float(self.sale_staff_input.text().replace(',', '.')) if self.sale_staff_input.text() else 0
            sale_org = float(self.sale_org_input.text().replace(',', '.')) if self.sale_org_input.text() else 0
            total_sales = sale_staff + sale_org
            self.total_sale_output.setText(f'{total_sales:.2f}')
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Введите корректные значения объемов реализации')

    def show_balance(self):
        """Отображает баланс продукции в таблице"""
        try:
            # Получаем значения из полей ввода
            production = float(self.production_output.text().replace(',', '.')) if self.production_output.text() else 0
            purchase = float(self.purchase_input.text().replace(',', '.')) if self.purchase_input.text() else 0
            total_sales = float(self.total_sale_output.text().replace(',', '.')) if self.total_sale_output.text() else 0
            seeds = float(self.seeds_input.text().replace(',', '.')) if self.seeds_input.text() else 0

            # Обновляем таблицу
            self.balance_table.setItem(0, 1, QTableWidgetItem(f'{self.starting_balance:.2f}'))
            self.balance_table.setItem(1, 1, QTableWidgetItem(f'{production:.2f}'))
            self.balance_table.setItem(2, 1, QTableWidgetItem(f'{purchase:.2f}'))
            self.balance_table.setItem(3, 1, QTableWidgetItem(f'{total_sales:.2f}'))
            self.balance_table.setItem(4, 1, QTableWidgetItem(f'{seeds:.2f}'))

            # Рассчитываем остаток на конец периода
            ending_balance = self.starting_balance + production + purchase - total_sales - seeds
            self.ending_balance_label.setText(f'Остаток на конец периода: {ending_balance:.2f} ц')

        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все необходимые поля корректными значениями')


def main():
    app = QApplication(sys.argv)
    window = CropBalanceApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()