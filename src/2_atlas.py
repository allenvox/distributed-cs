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

# FFD (First Fit Decreasing)
def ffd(tasks, n_machines):
    sorted_tasks = sorted(tasks, key=lambda x: x[0], reverse=True)  # Сортируем по NodeCnt
    containers = []
    for task in sorted_tasks:
        placed = False
        for container in containers:
            if sum(t[0] for t in container) + task[0] <= n_machines:
                container.append(task)
                placed = True
                break
        if not placed:
            containers.append([task])
    return containers

# NFDH: алгоритм распределения контейнеров по машинам
def nfdh(containers, n_machines):
    machines = []
    current_machine = []
    for container in containers:
        if sum(task[0] for task in current_machine) + sum(task[0] for task in container) <= n_machines:
            current_machine.extend(container)
        else:
            machines.append(current_machine)
            current_machine = container.copy()
    if current_machine:
        machines.append(current_machine)
    return machines

# FFDH: алгоритм распределения контейнеров по машинам
def ffdh(containers, n_machines):
    machines = []
    for container in containers:
        placed = False
        for machine in machines:
            if sum(task[0] for task in machine) + sum(task[0] for task in container) <= n_machines:
                machine.extend(container)
                placed = True
                break
        if not placed:
            machines.append(container.copy())
    return machines

# Функция для подсчета целевой функции T(S)
def objective_function(schedule):
    if not schedule:  # Проверяем, пустое ли расписание
        return 0
    return max(sum(task[1] for task in machine) for machine in schedule)

# Эксперимент 4
def experiment_4(log_file_path):
    n_machines = 1192  # Количество машин фиксировано
    tasks = parse_log(log_file_path, max_jobs=10000)

    # Подсчет матожидания и среднеквадратичного отклонения для каждой партии задач
    batch_size = 1000
    num_batches = len(tasks) // batch_size
    nfdh_results = []
    ffdh_results = []

    for i in range(num_batches):
        current_tasks = tasks[i * batch_size:(i + 1) * batch_size]

        # Упаковка задач по контейнерам с помощью FFD
        containers = ffd(current_tasks, n_machines)

        # Применение NFDH
        start_time = time.time()
        nfdh_schedule = nfdh(containers, n_machines)
        nfdh_T = objective_function(nfdh_schedule)
        nfdh_time = time.time() - start_time
        nfdh_results.append((nfdh_T, nfdh_time))

        # Применение FFDH
        start_time = time.time()
        ffdh_schedule = ffdh(containers, n_machines)
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
    print("\nРезультаты NFDH:")
    print(f"Матожидание T(S): {nfdh_mean_T:.4f}, СКО T(S): {nfdh_std_T:.4f}")
    print(f"Матожидание времени выполнения: {nfdh_mean_time:.4f}, СКО времени: {nfdh_std_time:.4f}")

    print("\nРезультаты FFDH:")
    print(f"Матожидание T(S): {ffdh_mean_T:.4f}, СКО T(S): {ffdh_std_T:.4f}")
    print(f"Матожидание времени выполнения: {ffdh_mean_time:.4f}, СКО времени: {ffdh_std_time:.4f}")

# Запуск эксперимента
if __name__ == "__main__":
    experiment_4('./data/atlas.log')  # Укажите путь к файлу atlas.log
