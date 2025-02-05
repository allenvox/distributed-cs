import matplotlib.pyplot as plt

def calculate_Theta(N, n, lambda_, mu, m=1):
    total = 0.0
    product = 1.0
    for j in range(n):
        denominator = mu * m * (N - j)
        if denominator == 0:
            product = 0
            break
        term = 1 + lambda_ / denominator
        product *= term
        total += product
    Theta = total / lambda_
    return Theta

def calculate_T(N, n, lambda_, mu, m=1):
    if n == 1:
        return 1.0 / (mu * m)
    else:
        total = 0.0
        product = 1.0
        for j in range(n):
            denominator = mu * m * (N - j)
            if denominator == 0:
                product = 0
                break
            term = 1 + lambda_ / denominator
            product *= term
            total += product
        return total

# Построение графиков для Theta(n) (задание 2)
def plot_theta_mu():
    N = 65536
    lambda_ = 1e-5
    m = 1
    n_values = list(range(65527, 65536 + 1))
    mu_list = [1, 10, 100, 1000]
    
    plt.figure(figsize=(12, 8))
    for mu in mu_list:
        theta_values = [calculate_Theta(N, n, lambda_, mu, m) / 3600 for n in n_values]  # Переводим в часы
        plt.plot(n_values, theta_values, marker='o', label=f'μ={mu}')
        print(f"μ={mu}: Θ (hours) for n={n_values}: {theta_values}")
    plt.xlabel('n, number of elementary machines')
    plt.ylabel('Mean time between failures (hours)')
    plt.title('Зависимость Θ от n при различных μ')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_theta_lambda():
    N = 65536
    mu = 1
    m = 1
    n_values = list(range(65527, 65536 + 1))
    lambda_list = [1e-5, 1e-6, 1e-7, 1e-8, 1e-9]
    
    plt.figure(figsize=(12, 8))
    for lambda_ in lambda_list:
        theta_values = [calculate_Theta(N, n, lambda_, mu, m) / 3600 for n in n_values]  # Переводим в часы
        plt.plot(n_values, theta_values, marker='o', label=f'λ={lambda_:.1e}')
        print(f"λ={lambda_:.1e}: Θ (hours) for n={n_values}: {theta_values}")
    plt.xlabel('n, number of elementary machines')
    plt.ylabel('Mean time between failures (hours)')
    plt.title('Зависимость Θ от n при различных λ')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_theta_m():
    N = 65536
    mu = 1
    lambda_ = 1e-5
    n_values = list(range(65527, 65536 + 1))
    m_list = [1, 2, 3, 4]
    
    plt.figure(figsize=(12, 8))
    for m in m_list:
        theta_values = [calculate_Theta(N, n, lambda_, mu, m) / 3600 for n in n_values]  # Переводим в часы
        plt.plot(n_values, theta_values, marker='o', label=f'm={m}')
        print(f"m={m}: Θ (hours) for n={n_values}: {theta_values}")
    plt.xlabel('n, number of elementary machines')
    plt.ylabel('Mean time between failures (hours)')
    plt.title('Зависимость Θ от n при различных m')
    plt.legend()
    plt.grid(True)
    plt.show()

# Построение графиков для T(n) (задание 3)
def plot_T_mu():
    N = 1000
    lambda_ = 1e-3
    m = 1
    n_values = list(range(900, 1000 + 1, 10))
    mu_list = [1, 2, 4, 6]
    
    plt.figure(figsize=(12, 8))
    for mu in mu_list:
        T_values = [calculate_T(N, n, lambda_, mu, m) / 3600 for n in n_values]  # Переводим в часы
        plt.plot(n_values, T_values, marker='o', label=f'μ={mu}')
        print(f"μ={mu}: T (hours) for n={n_values}: {T_values}")
    plt.xlabel('n, number of elementary machines')
    plt.ylabel('Mean time to recovery (hours)')
    plt.title('Зависимость T от n при различных μ')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_T_lambda():
    N = 8192
    mu = 1
    m = 1
    n_values = list(range(8092, 8192 + 1, 10))
    lambda_list = [1e-5, 1e-6, 1e-7, 1e-8, 1e-9]
    
    plt.figure(figsize=(12, 8))
    for lambda_ in lambda_list:
        T_values = [calculate_T(N, n, lambda_, mu, m) / 3600 for n in n_values]  # Переводим в часы
        plt.plot(n_values, T_values, marker='o', label=f'λ={lambda_:.1e}')
        print(f"λ={lambda_:.1e}: T (hours) for n={n_values}: {T_values}")
    plt.xlabel('n, number of elementary machines')
    plt.ylabel('Mean time to recovery (hours)')
    plt.title('Зависимость T от n при различных λ')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_T_m():
    N = 8192
    mu = 1
    lambda_ = 1e-5
    n_values = list(range(8092, 8192 + 1, 10))
    m_list = [1, 2, 3, 4]
    
    plt.figure(figsize=(12, 8))
    for m in m_list:
        T_values = [calculate_T(N, n, lambda_, mu, m) / 3600 for n in n_values]  # Переводим в часы
        plt.plot(n_values, T_values, marker='o', label=f'm={m}')
        print(f"m={m}: T (hours) for n={n_values}: {T_values}")
    plt.xlabel('n, number of elementary machines')
    plt.ylabel('Mean time to recovery (hours)')
    plt.title('Зависимость T от n при различных m')
    plt.legend()
    plt.grid(True)
    plt.show()

# Вызов функций для построения графиков
plot_theta_mu()
plot_theta_lambda()
plot_theta_m()
plot_T_mu()
plot_T_lambda()
plot_T_m()
