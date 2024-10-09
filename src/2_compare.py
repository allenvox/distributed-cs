import random
import time

import matplotlib.pyplot as plt
import numpy as np


# Генерация задач в виде кортежей (rj, tj)
def generate_tasks(num_tasks, n_machines):
    tasks = []
    for _ in range(num_tasks):
        rj = random.randint(1, n_machines)  # Количество необходимых машин для задачи
        tj = random.randint(1, 100)  # Время выполнения задачи (от 1 до 100)
        tasks.append((rj, tj))  # Каждая задача — это кортеж (rj, tj)
    return tasks

# Алгоритм FFD (First-Fit Decreasing) для упаковки задач в контейнеры
def ffd(tasks, n_machines):
    sorted_tasks = sorted(tasks, key=lambda x: x[0], reverse=True)
    containers = []
    for task in sorted_tasks:
        placed = False
        for container in containers:
            if sum([t[0] for t in container]) + task[0] <= n_machines:
                container.append(task)
                placed = True
                break
        if not placed:
            containers.append([task])
    return containers

def best_fit(tasks, n_machines):
    containers = []
    for task in tasks:
        best_index = -1
        min_space_left = n_machines + 1  # Начинаем с "бесконечности"

        for i, container in enumerate(containers):
            space_left = n_machines - sum(t[0] for t in container)
            if space_left >= task[0] and space_left < min_space_left:
                min_space_left = space_left
                best_index = i

        if best_index != -1:
            containers[best_index].append(task)
        else:
            containers.append([task])  # Создаем новый контейнер

    return containers

def worst_fit(tasks, n_machines):
    containers = []
    for task in tasks:
        worst_index = -1
        max_space_left = -1

        for i, container in enumerate(containers):
            space_left = n_machines - sum(t[0] for t in container)
            if space_left >= task[0] and space_left > max_space_left:
                max_space_left = space_left
                worst_index = i

        if worst_index != -1:
            containers[worst_index].append(task)
        else:
            containers.append([task])  # Создаем новый контейнер

    return containers

def next_fit(tasks, n_machines):
    containers = []
    current_container = []

    for task in tasks:
        if sum(t[0] for t in current_container) + task[0] <= n_machines:
            current_container.append(task)
        else:
            containers.append(current_container)  # Сохраняем текущий контейнер
            current_container = [task]  # Начинаем новый контейнер

    if current_container:  # Не забываем добавить последний контейнер
        containers.append(current_container)

    return containers


def ffdh(containers, n_machines):
    machines = []
    for container in containers:
        placed = False
        for machine in machines:
            # Если в машине есть место, помещаем туда контейнер
            if sum(task[1] for task in machine) + sum(task[1] for task in container) <= n_machines:
                machine.extend(container)
                placed = True
                break
        # Если не нашли подходящую машину, создаем новую
        if not placed:
            machines.append(container.copy())
    return machines

def nfdh(containers, n_machines):
    machines = []
    current_machine = []
    for container in containers:
        # Если есть место в текущей машине, помещаем туда
        if sum(task[1] for task in current_machine) + sum(task[1] for task in container) <= n_machines:
            current_machine.extend(container)
        else:
            # Если нет места, сохраняем текущую машину и начинаем новую
            machines.append(current_machine)
            current_machine = container.copy()
    # Не забываем добавить последнюю машину, если она не пустая
    if current_machine:
        machines.append(current_machine)
    return machines


# Функция для подсчета целевой функции T(S)
def objective_function(schedule):
    return max([sum([task[1] for task in machine]) for machine in schedule])

# Функция для вычисления нижней границы T'(S)
def lower_bound(tasks, n_machines):
    total_time = sum([task[1] for task in tasks])
    return total_time / n_machines

# Эксперимент 3: сравнение NFDH и FFDH по точности для фиксированного n = 1024
def experiment_3():
    n_machines = 1024  # Количество машин
    task_sizes = range(500, 5500, 500)  # Количество задач от 500 до 5000 с шагом 500
    num_experiments = 2  # Количество повторений для каждого размера задач

    nfdh_epsilons = []
    ffdh_epsilons = []

    # Проход по количеству задач m
    for m in task_sizes:
        nfdh_epsilon_set = []
        ffdh_epsilon_set = []
        
        # Повторяем эксперимент num_experiments раз для каждого значения m
        for _ in range(num_experiments):
            # Генерация задач
            tasks = generate_tasks(m, n_machines)

            # Упаковка в контейнеры
            containers = ffd(tasks, n_machines)
            #containers = best_fit(tasks, n_machines)
            #containers = worst_fit(tasks, n_machines)
            #containers = next_fit(tasks, n_machines)

            # Нижняя граница T'
            T_prime = lower_bound(tasks, n_machines)

            # NFDH алгоритм
            nfdh_schedule = nfdh(containers, n_machines)
            nfdh_T = objective_function(nfdh_schedule)
            nfdh_epsilon = (nfdh_T - T_prime) / T_prime
            nfdh_epsilon_set.append(nfdh_epsilon)

            # FFDH алгоритм
            ffdh_schedule = ffdh(containers, n_machines)
            ffdh_T = objective_function(ffdh_schedule)
            ffdh_epsilon = (ffdh_T - T_prime) / T_prime
            ffdh_epsilon_set.append(ffdh_epsilon)

        # Записываем матожидание и СКО для каждого набора задач
        nfdh_epsilons.append((np.mean(nfdh_epsilon_set), np.std(nfdh_epsilon_set)))
        ffdh_epsilons.append((np.mean(ffdh_epsilon_set), np.std(ffdh_epsilon_set)))

    # Разбираем результаты для построения графика
    nfdh_means, nfdh_stds = zip(*nfdh_epsilons)
    ffdh_means, ffdh_stds = zip(*ffdh_epsilons)

    # Построение графиков
    plt.figure(figsize=(10, 6))

    # График математического ожидания epsilon
    plt.subplot(2, 1, 1)
    plt.plot(task_sizes, nfdh_means, label="NFDH", marker="o")
    plt.plot(task_sizes, ffdh_means, label="FFDH", marker="o")
    plt.xlabel("Количество задач (m)")
    plt.ylabel("Матожидание от ϵ")
    plt.title("Зависимость mean(ϵ) от количества задач")
    plt.legend()

    # График среднеквадратичного отклонения epsilon
    plt.subplot(2, 1, 2)
    plt.plot(task_sizes, nfdh_stds, label="NFDH", marker="o")
    plt.plot(task_sizes, ffdh_stds, label="FFDH", marker="o")
    plt.xlabel("Количество задач (m)")
    plt.ylabel("Среднеквадратичное отклонение от ϵ")
    plt.title("Зависимость std_dev(ϵ) от количества задач")
    plt.legend()

    plt.tight_layout()
    plt.show()

# Запуск эксперимента
if __name__ == "__main__":
    experiment_3()
