import numpy as np
import random
import time
import heapq


# Функция для генерации задач
def generate_tasks(m, n):
    tasks = []
    for _ in range(m):
        r_j = random.randint(1, n)  # Псевдослучайное значение от 1 до n
        t_j = random.randint(1, 100)  # Псевдослучайное время выполнения от 1 до 100
        tasks.append((r_j, t_j))
    return tasks


# Алгоритм NFDH
def NFDH(tasks, n):
    sorted_tasks = sorted(tasks, key=lambda x: x[1], reverse=True)  # Сортировка по времени выполнения
    machines = [0] * n  # Инициализация машин
    for r_j, t_j in sorted_tasks:
        machines[machines.index(min(machines))] += t_j  # Назначаем задачу на машину с минимальной нагрузкой
    return max(machines)  # Максимальная загрузка (makespan)


# Алгоритм FFDH
def FFDH(tasks, n):
    machines = [0] * n  # Инициализация машин
    for r_j, t_j in tasks:
        machines[machines.index(min(machines))] += t_j  # Назначаем задачу на машину с минимальной загрузкой
    return max(machines)  # Максимальная загрузка (makespan)


# Функция для расчета статистики
def calculate_statistics(alg_results):
    # Математическое ожидание
    mean = np.mean(alg_results)
    # Среднеквадратическое отклонение
    std_dev = np.std(alg_results)
    return mean, std_dev


# Главная функция для проведения экспериментов
def run_experiments():
    task_counts = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    n = 1024
    epsilon_NFDH = []
    epsilon_FFDH = []

    # Запуск экспериментов для каждого значения m
    for m in task_counts:
        NFDH_results = []
        FFDH_results = []

        # Сгенерируем 10 наборов задач для каждого m
        for _ in range(10):
            tasks = generate_tasks(m, n)

            # Запускаем оба алгоритма и получаем целевую функцию (makespan)
            makespan_NFDH = NFDH(tasks, n)
            makespan_FFDH = FFDH(tasks, n)

            # Сохраняем результаты для дальнейшего анализа
            NFDH_results.append(makespan_NFDH)
            FFDH_results.append(makespan_FFDH)

        # Расчет математического ожидания и среднеквадратического отклонения
        mean_NFDH, std_NFDH = calculate_statistics(NFDH_results)
        mean_FFDH, std_FFDH = calculate_statistics(FFDH_results)

        # Расчет точности ε
        epsilon_NFDH.append((mean_NFDH, std_NFDH))
        epsilon_FFDH.append((mean_FFDH, std_FFDH))

    return epsilon_NFDH, epsilon_FFDH, task_counts


# Функция для отображения результатов
def plot_results(epsilon_NFDH, epsilon_FFDH, task_counts):
    means_NFDH = [x[0] for x in epsilon_NFDH]
    std_devs_NFDH = [x[1] for x in epsilon_NFDH]

    means_FFDH = [x[0] for x in epsilon_FFDH]
    std_devs_FFDH = [x[1] for x in epsilon_FFDH]

    plt.figure(figsize=(12, 8))

    # График для NFDH
    plt.errorbar(task_counts, means_NFDH, yerr=std_devs_NFDH, fmt='-o', label="NFDH", capsize=5)

    # График для FFDH
    plt.errorbar(task_counts, means_FFDH, yerr=std_devs_FFDH, fmt='-s', label="FFDH", capsize=5)

    plt.xlabel("Количество задач (m)")
    plt.ylabel("Целевая функция (Makespan)")
    plt.title("Сравнительный анализ алгоритмов NFDH и FFDH")
    plt.legend()
    plt.grid(True)
    plt.show()


# Основной блок
if __name__ == "__main__":
    epsilon_NFDH, epsilon_FFDH, task_counts = run_experiments()
    plot_results(epsilon_NFDH, epsilon_FFDH, task_counts)
