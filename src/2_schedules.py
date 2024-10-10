import random
import time

import matplotlib.pyplot as plt


# Генерация задач в виде кортежей (rj, tj)
def generate_tasks(num_tasks, n_machines):
    tasks = []
    for _ in range(num_tasks):
        rj = random.randint(1, n_machines)  # Количество необходимых машин для задачи
        tj = random.randint(1, 10)  # Время выполнения задачи (от 1 до 10)
        tasks.append((rj, tj))  # Каждая задача — это кортеж (rj, tj)
    return tasks

# Случайное распределение задач по контейнерам
def rnd(tasks, n_machines):
    containers = []
    for task in tasks:
        placed = False
        if containers:
            random_container = random.choice(containers)
            if sum(t[0] for t in random_container) + task[0] <= n_machines:
                random_container.append(task)
                placed = True
        if not placed:
            containers.append([task])
    return containers

# Алгоритм FFD (First-Fit Decreasing) для упаковки задач в контейнеры
def ffd(tasks, n_machines):
    # Задачи сортируются по убыванию количества машин (r_j)
    sorted_tasks = sorted(tasks, key=lambda x: x[0], reverse=True)
    
    containers = []  # Список для контейнеров

    # Проход по всем задачам
    for task in sorted_tasks:
        placed = False
        # Ищем первый контейнер, в который поместится текущая задача
        for container in containers:
            if sum([t[0] for t in container]) + task[0] <= n_machines:
                container.append(task)
                placed = True
                break

        # Если задачу некуда добавить, создаем новый контейнер
        if not placed:
            containers.append([task])

    return containers

# Алгоритм FFDH для минимизации количества машин с возвратом к началу
def ffdh(containers, n_machines):
    machines = [[] for _ in range(n_machines)]  # Инициализация всех машин
    machine_idx = 0  # Индекс текущей машины
    for container in containers:
        placed = False
        for i in range(n_machines):
            # Пытаемся разместить контейнер в первую машину, где есть место
            idx = (machine_idx + i) % n_machines  # Возврат к началу, если машины заканчиваются
            if sum(task[0] for task in machines[idx]) + sum(task[0] for task in container) <= n_machines:
                machines[idx].extend(container)
                placed = True
                break
        if not placed:
            # Если контейнер не помещается, добавляем в первую машину и увеличиваем целевую функцию
            machines[machine_idx].extend(container)
            machine_idx = (machine_idx + 1) % n_machines  # Переходим к следующей машине
    return machines

# Алгоритм NFDH для минимизации количества машин с возвратом к началу
def nfdh(containers, n_machines):
    machines = [[] for _ in range(n_machines)]  # Инициализация всех машин
    current_machine_idx = 0
    for container in containers:
        # Если контейнер помещается в текущую машину
        if sum(task[0] for task in machines[current_machine_idx]) + sum(task[0] for task in container) <= n_machines:
            machines[current_machine_idx].extend(container)
        else:
            # Если не помещается, переходим к следующей машине (с возвратом к началу)
            current_machine_idx = (current_machine_idx + 1) % n_machines
            machines[current_machine_idx].extend(container)
    return machines

# Функция для подсчета целевой функции T(S) — максимальное время выполнения среди всех машин
def objective_function(schedule):
    return max([sum([task[1] for task in machine]) for machine in schedule])

# Функция для построения графика зависимости T(S) от количества задач
def plot_experiment():
    task_sizes = range(500, 5500, 500)  # Количество задач от 500 до 5000 с шагом 500
    n_machines = 1024  # Количество машин

    t_nfdh = []
    t_ffdh = []

    # Проход по количеству задач
    for num_tasks in task_sizes:
        # Генерация задач
        tasks = generate_tasks(num_tasks, n_machines)

        # Упаковка задач по контейнерам
        f_containers = ffd(tasks, n_machines)
        r_containers = rnd(tasks, n_machines)

        # Применение NFDH
        nfdh_schedule = nfdh(r_containers, n_machines)
        nfdh_T = objective_function(nfdh_schedule)
        t_nfdh.append(nfdh_T)

        # Применение FFDH
        ffdh_schedule = ffdh(f_containers, n_machines)
        ffdh_T = objective_function(ffdh_schedule)
        t_ffdh.append(ffdh_T)

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(task_sizes, t_nfdh, label="NFDH", marker='o')
    plt.plot(task_sizes, t_ffdh, label="FFDH", marker='s')
    plt.xlabel("Количество задач")
    plt.ylabel("Целевая функция T(S)")
    plt.title("Зависимость T(S) от количества задач")
    plt.legend()
    plt.grid(True)
    plt.show()

# Запуск эксперимента
if __name__ == "__main__":
    plot_experiment()
