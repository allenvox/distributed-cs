import random
import re
import time

import numpy as np
import pandas as pd


# Функция для парсинга файла логов
def parse_log(file_path, max_jobs=5000):
    tasks = []
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if i >= max_jobs:
                break

            # Регулярное выражение для извлечения StartTime, EndTime и NodeCnt
            match = re.match(r'JobId=\d+\s+UserId=\w+\(\d+\)\s+Name=\w+\s+JobState=\w+\s+Partition=\w+\s+TimeLimit=\w+\s+StartTime=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\s+EndTime=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\s+NodeList=[\w\[\],-]+\s+NodeCnt=(\d+)', line)

            if match:
                # Извлекаем StartTime, EndTime и NodeCnt
                start_time_str = match.group(1)  # StartTime
                end_time_str = match.group(2)  # EndTime
                node_cnt = int(match.group(3))  # NodeCnt

                # Преобразуем время в секунды с начала эпохи
                start_time = int(pd.to_datetime(start_time_str).timestamp())
                end_time = int(pd.to_datetime(end_time_str).timestamp())

                # Проверяем, что время выполнения положительное
                if end_time > start_time:
                    tj = end_time - start_time  # tj = EndTime - StartTime
                    tasks.append((node_cnt, tj))  # Создаем задачу как кортеж (NodeCnt, ExecutionTime)

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

# Функция для подсчета целевой функции T(S)
def objective_function(schedule):
    if not schedule:  # Проверяем, пустое ли расписание
        return 0
    return max(sum(task[1] for task in machine) for machine in schedule)

# Эксперимент 4 с задачами LLNL-Atlas
def experiment_4(log_file_path):
    n_machines = 1192  # Количество машин фиксировано
    tasks = parse_log(log_file_path, max_jobs=30000)

    # Подсчет матожидания и среднеквадратичного отклонения для каждой партии задач
    batch_size = 3000
    num_batches = len(tasks) // batch_size
    nfdh_results = []
    ffdh_results = []

    for i in range(num_batches):
        current_tasks = tasks[i * batch_size:(i + 1) * batch_size]

        # Упаковка задач по контейнерам с помощью FFD
        f_containers = rnd(tasks, n_machines)
        r_containers = rnd(tasks, n_machines)

        # Применение NFDH
        start_time = time.time()
        nfdh_schedule = nfdh(r_containers, n_machines)
        nfdh_T = objective_function(nfdh_schedule)
        nfdh_time = time.time() - start_time
        nfdh_results.append((nfdh_T, nfdh_time))

        # Применение FFDH
        start_time = time.time()
        ffdh_schedule = ffdh(f_containers, n_machines)
        ffdh_T = objective_function(ffdh_schedule)
        ffdh_time = time.time() - start_time
        ffdh_results.append((ffdh_T, ffdh_time))

    # Подсчет матожидания и среднеквадратичного отклонения
    nfdh_Ts, nfdh_times = zip(*nfdh_results)
    ffdh_Ts, ffdh_times = zip(*ffdh_results)

    nfdh_mean_T = np.mean(nfdh_Ts)
    nfdh_std_T = np.std(nfdh_Ts)

    ffdh_mean_T = np.mean(ffdh_Ts)
    ffdh_std_T = np.std(ffdh_Ts)

    nfdh_mean_time = np.mean(nfdh_times)
    nfdh_std_time = np.std(nfdh_times)

    ffdh_mean_time = np.mean(ffdh_times)
    ffdh_std_time = np.std(ffdh_times)

    # Вывод результатов
    print("Результаты NFDH:")
    print(f"Матожидание T(S): {nfdh_mean_T:.4f}, СКО T(S): {nfdh_std_T:.4f}")
    print(f"Матожидание времени выполнения: {nfdh_mean_time:.4f}, СКО времени: {nfdh_std_time:.4f}")

    print("\nРезультаты FFDH:")
    print(f"Матожидание T(S): {ffdh_mean_T:.4f}, СКО T(S): {ffdh_std_T:.4f}")
    print(f"Матожидание времени выполнения: {ffdh_mean_time:.4f}, СКО времени: {ffdh_std_time:.4f}")

# Запуск эксперимента
if __name__ == "__main__":
    experiment_4('./data/atlas.log')  # Укажите путь к файлу atlas.log
