import matplotlib.pyplot as plt
import numpy as np


# Функция для загрузки данных из файла
def load_data(filename):
    return np.loadtxt(filename)

# Загрузка данных из файлов
data_separate = load_data('1x8_separate.dat')
data_singlecore = load_data('1x8_singlecore.dat')
data_2x4 = load_data('2x4.dat')

# Извлечение данных для осей X и Y
x_separate, y_separate = data_separate[:, 0], data_separate[:, 1]
x_singlecore, y_singlecore = data_singlecore[:, 0], data_singlecore[:, 1]
x_2x4, y_2x4 = data_2x4[:, 0], data_2x4[:, 1]

# Построение графика
plt.figure(figsize=(10, 6))

plt.plot(x_separate, y_separate, label="1x8 Separate CPUs", marker='o')
plt.plot(x_singlecore, y_singlecore, label="1x8 Single CPU", marker='s')
plt.plot(x_2x4, y_2x4, label="2x4", marker='^')

# Установка логарифмической шкалы для оси X
plt.xscale('log', base=2)

# Настройка осей
plt.xlabel("Размер сообщения (МБ)")
plt.ylabel("Время выполнения (с)")
plt.title("Зависимость времени выполнения от размера сообщения")
plt.grid(True, which="both", ls="--")

# Добавление легенды
plt.legend()

# Показ графика
plt.show()
