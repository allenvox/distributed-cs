import heapq
import random
import time

import matplotlib.pyplot as plt
import numpy as np


def generate_tasks(m, n): # m - number of tasks, n - number of processors
    tasks = []
    for _ in range(m):
        r_j = random.randint(1, n)
        t_j = random.randint(1, 100) # 100s - max task time
        tasks.append((r_j, t_j))
    return tasks


def generate_tasks_llnl(m):
    tasks = []
    for _ in range(m):
        r_j = random.randint(1, 9216) # 9216 processors on LLNL Atlas
        t_j = random.randint(1, 1000) # 1000s - max task time on LLNL Atlas
        tasks.append((r_j, t_j))
    return tasks


# next fit decreasing height
def NFDH(tasks, n):
    sorted_tasks = sorted(tasks, key=lambda x: x[1], reverse=True) # Sort by est. time
    machines = [0] * n                                             # Machines initialization
    for r_j, t_j in sorted_tasks:
        machines[machines.index(min(machines))] += t_j             # Assign task to min loaded machine
    return max(machines)                                           # Max makespan


# first fit decreasing height
def FFDH(tasks, n):
    machines = [0] * n
    for r_j, t_j in tasks:
        machines[machines.index(min(machines))] += t_j
    return max(machines)


# calculate mean and standard deviation
def calculate_statistics(alg_results):
    mean = np.mean(alg_results)
    std_dev = np.std(alg_results)
    return mean, std_dev


def run_time_experiments():
    task_counts = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    n_values = [1024, 4096]
    time_results = {n: {'NFDH': [], 'FFDH': []} for n in n_values}

    # for each m & n
    for n in n_values:
        for m in task_counts:
            time_NFDH = []
            time_FFDH = []

            # do 10 times for each
            for _ in range(10):
                tasks = generate_tasks(m, n)

                # NFDH time
                start_time = time.time()
                NFDH(tasks, n)
                end_time = time.time()
                time_NFDH.append(end_time - start_time)

                # FFDH time
                start_time = time.time()
                FFDH(tasks, n)
                end_time = time.time()
                time_FFDH.append(end_time - start_time)

            # time means
            time_results[n]['NFDH'].append(np.mean(time_NFDH))
            time_results[n]['FFDH'].append(np.mean(time_FFDH))

    return time_results, task_counts


def run_makespan_experiments():
    task_counts = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    n = 1024
    epsilon_NFDH = []
    epsilon_FFDH = []

    # for each m
    for m in task_counts:
        NFDH_results = []
        FFDH_results = []

        for _ in range(10):
            tasks = generate_tasks(m, n)

            # makespans
            makespan_NFDH = NFDH(tasks, n)
            makespan_FFDH = FFDH(tasks, n)

            NFDH_results.append(makespan_NFDH)
            FFDH_results.append(makespan_FFDH)

        mean_NFDH, std_NFDH = calculate_statistics(NFDH_results)
        mean_FFDH, std_FFDH = calculate_statistics(FFDH_results)

        # mean & standard deviation (ε)
        epsilon_NFDH.append((mean_NFDH, std_NFDH))
        epsilon_FFDH.append((mean_FFDH, std_FFDH))

    return epsilon_NFDH, epsilon_FFDH, task_counts


def run_llnl_experiments():
    task_counts = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    n = 1024
    epsilon_NFDH = []
    epsilon_FFDH = []

    for m in task_counts:
        NFDH_results = []
        FFDH_results = []

        for _ in range(10):
            tasks = generate_tasks_llnl(m)

            makespan_NFDH = NFDH(tasks, n)
            makespan_FFDH = FFDH(tasks, n)

            NFDH_results.append(makespan_NFDH)
            FFDH_results.append(makespan_FFDH)

        mean_NFDH, std_NFDH = calculate_statistics(NFDH_results)
        mean_FFDH, std_FFDH = calculate_statistics(FFDH_results)

        epsilon_NFDH.append((mean_NFDH, std_NFDH))
        epsilon_FFDH.append((mean_FFDH, std_FFDH))

    return epsilon_NFDH, epsilon_FFDH, task_counts


def plot_results_llnl(epsilon_NFDH, epsilon_FFDH, task_counts):
    means_NFDH = [x[0] for x in epsilon_NFDH]
    std_devs_NFDH = [x[1] for x in epsilon_NFDH]

    means_FFDH = [x[0] for x in epsilon_FFDH]
    std_devs_FFDH = [x[1] for x in epsilon_FFDH]

    plt.figure(figsize=(12, 8))

    # NFDH
    plt.errorbar(task_counts, means_NFDH, yerr=std_devs_NFDH, fmt='-o', label="NFDH", capsize=5)

    # FFDH
    plt.errorbar(task_counts, means_FFDH, yerr=std_devs_FFDH, fmt='-s', label="FFDH", capsize=5)

    plt.xlabel("Количество задач (m)")
    plt.ylabel("Целевая функция (Makespan)")
    plt.title("Сравнительный анализ алгоритмов NFDH и FFDH для системы LLNL Atlas")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_time_results(time_results, task_counts):
    plt.figure(figsize=(12, 8))

    for n in time_results:
        times_NFDH = time_results[n]['NFDH']
        times_FFDH = time_results[n]['FFDH']

        plt.plot(task_counts, times_NFDH, '-o', label=f"NFDH (n={n})")
        plt.plot(task_counts, times_FFDH, '-s', label=f"FFDH (n={n})")

    plt.xlabel("Количество задач (m)")
    plt.ylabel("Время выполнения (секунды)")
    plt.title("Время выполнения алгоритмов NFDH и FFDH при различных n")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_results(epsilon_NFDH, epsilon_FFDH, task_counts):
    means_NFDH = [x[0] for x in epsilon_NFDH]
    std_devs_NFDH = [x[1] for x in epsilon_NFDH]

    means_FFDH = [x[0] for x in epsilon_FFDH]
    std_devs_FFDH = [x[1] for x in epsilon_FFDH]

    plt.figure(figsize=(12, 8))

    plt.errorbar(task_counts, means_NFDH, yerr=std_devs_NFDH, fmt='-o', label="NFDH", capsize=5)
    plt.errorbar(task_counts, means_FFDH, yerr=std_devs_FFDH, fmt='-s', label="FFDH", capsize=5)

    plt.xlabel("Количество задач (m)")
    plt.ylabel("Целевая функция (Makespan)")
    plt.title("Сравнительный анализ алгоритмов NFDH и FFDH")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # 1. Example with basic tasks

    # 2. Execution times analysis
    time_results, task_counts = run_time_experiments()
    plot_time_results(time_results, task_counts)

    # 3. Makespan analysis
    epsilon_NFDH, epsilon_FFDH, task_counts = run_makespan_experiments()
    print(epsilon_NFDH, epsilon_FFDH)
    plot_results(epsilon_NFDH, epsilon_FFDH, task_counts)

    # 4. LLNL Atlas example
    epsilon_NFDH, epsilon_FFDH, task_counts = run_llnl_experiments()
    plot_results_llnl(epsilon_NFDH, epsilon_FFDH, task_counts)


"""
- Какова вычислительная сложность алгоритмов?

Алгоритм NFDH имеет сложность O(m), так как задачи размещаются по уровням последовательно.

Алгоритм FFDH с использованием дерева турнира имеет сложность O(mlogn), так как
для каждой задачи нужно найти подходящий уровень за O(logn).


- Как изменяется время работы алгоритмов в зависимости от m?

Для NFDH время работы увеличивается линейно с ростом числа задач m.

Для FFDH время работы увеличивается пропорционально mlogn, что более эффективно при увеличении n.


- Как изменяется время работы алгоритмов в зависимости от n?

Для NFDH изменение числа машин n практически не влияет на сложность.

Для FFDH увеличение n делает алгоритм более сложным из-за работы с деревом турнира,
но его эффективность по сравнению с NFDH будет лучше при больших n.
"""
