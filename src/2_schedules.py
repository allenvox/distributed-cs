import random
import time


# Генерация задач в виде кортежей (rj, tj)
def generate_tasks(num_tasks, n_machines):
    tasks = []
    for _ in range(num_tasks):
        rj = random.randint(1, n_machines)  # Количество необходимых машин для задачи
        tj = random.randint(1, 10)  # Время выполнения задачи (от 1 до 10)
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

# Функция для подсчета целевой функции T(S) — максимальное время выполнения среди всех машин
def objective_function(schedule):
    return max([sum([task[1] for task in machine]) for machine in schedule])

# Эксперимент 1: запуск для m = 30, n = 5, tj от 1 до 10
def experiment_1():
    num_tasks = 100  # Количество задач
    n_machines = 64  # Количество машин

    # Генерируем задачи
    tasks = generate_tasks(num_tasks, n_machines)

    print("\nСгенерированные задачи (rj, tj):")
    print(tasks)

    # Шаг 1: Упаковка задач по контейнерам с помощью FFD
    containers = ffd(tasks, n_machines)

    print("\nКонтейнеры после FFD:")
    for idx, container in enumerate(containers):
        print(f"Контейнер {idx + 1}: {container}")

    # Шаг 2: Применение NFDH
    start = time.time()
    nfdh_schedule = nfdh(containers, n_machines)
    nfdh_time = time.time() - start
    nfdh_T = objective_function(nfdh_schedule)

    print("\nNFDH расписание:")
    for idx, machine in enumerate(nfdh_schedule):
        print(f"Машина {idx + 1}: {machine}")
    print(f"NFDH целевая функция T(S): {nfdh_T}")
    print(f"NFDH время выполнения: {nfdh_time:.6f} секунд")

    # Шаг 3: Применение FFDH
    start = time.time()
    ffdh_schedule = ffdh(containers, n_machines)
    ffdh_time = time.time() - start
    ffdh_T = objective_function(ffdh_schedule)

    print("\nFFDH расписание:")
    for idx, machine in enumerate(ffdh_schedule):
        print(f"Машина {idx + 1}: {machine}")
    print(f"FFDH целевая функция T(S): {ffdh_T}")
    print(f"FFDH время выполнения: {ffdh_time:.6f} секунд")

    # Нижняя граница для T'(S) — это среднее время выполнения всех задач, разделенное на количество машин
    lower_bound_T = sum([task[1] for task in tasks]) / n_machines
    epsilon_nfdh = (nfdh_T - lower_bound_T) / lower_bound_T
    epsilon_ffdh = (ffdh_T - lower_bound_T) / lower_bound_T

    print(f"\nНижняя граница T'(S): {lower_bound_T:.2f}")
    print(f"Epsilon NFDH: {epsilon_nfdh:.2%}")
    print(f"Epsilon FFDH: {epsilon_ffdh:.2%}")

# Запуск эксперимента
if __name__ == "__main__":
    experiment_1()
