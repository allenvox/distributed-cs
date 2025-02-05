import random
import time

import matplotlib.pyplot as plt


# Генерация задач в виде кортежей (rj, tj)
def generate_tasks(num_tasks, n_machines):
    tasks = []
    for _ in range(num_tasks):
        rj = random.randint(1, n_machines)  # Количество необходимых машин для задачи
        tj = random.randint(1, 100)  # Время выполнения задачи
        tasks.append((rj, tj))  # Каждая задача — это кортеж (rj, tj)
    return tasks

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

# Эксперимент 2: сравнение времени выполнения NFDH и FFDH
def experiment_2():
    task_sizes = list(range(500, 5001, 500))  # Количество задач
    n_sizes = [1024, 4096]  # Количество машин

    # Словари для хранения результатов по времени выполнения
    results = {1024: {'NFDH': [], 'FFDH': []}, 4096: {'NFDH': [], 'FFDH': []}}

    for n_machines in n_sizes:
        for num_tasks in task_sizes:
            tasks = generate_tasks(num_tasks, n_machines)

            # Шаг 1: Упаковка задач по контейнерам с помощью FFD
            containers = ffd(tasks, n_machines)

            # Шаг 2: Применение NFDH
            start = time.time()
            nfdh(containers, n_machines)
            nfdh_time = time.time() - start

            # Шаг 3: Применение FFDH
            start = time.time()
            ffdh(containers, n_machines)
            ffdh_time = time.time() - start

            # Сохраняем результаты
            results[n_machines]['NFDH'].append(nfdh_time)
            results[n_machines]['FFDH'].append(ffdh_time)

    # Построим графики для каждого значения n_machines
    plt.figure(figsize=(10, 6))
    
    # Для n_machines = 1024
    plt.plot(task_sizes, results[1024]['NFDH'], label='NFDH (1024)', marker='o')
    plt.plot(task_sizes, results[1024]['FFDH'], label='FFDH (1024)', marker='x')
    
    # Для n_machines = 4096
    plt.plot(task_sizes, results[4096]['NFDH'], label='NFDH (4096)', marker='o', linestyle='--')
    plt.plot(task_sizes, results[4096]['FFDH'], label='FFDH (4096)', marker='x', linestyle='--')

    plt.yscale('log')
    
    plt.xlabel("Количество задач")
    plt.ylabel("Время выполнения (сек)")
    plt.title("Сравнение времени выполнения FFDH и NFDH для разных n_machines")
    plt.legend()
    plt.show()

# Запуск эксперимента
experiment_2()
