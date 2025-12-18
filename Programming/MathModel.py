import matplotlib.pyplot as plt
import numpy as np
from math import exp, pi

T0 = 288.15
R = 8.314
M = 0.029
P0 = 113250
p0 = 1.2

def calculate_temperature(h):
    return max(h * (-0.0065) + T0, 250)

def calculate_pressure(h):
    return (P0) * exp(-(M * 9.81 * h) / 
                      (R * (calculate_temperature(h))))

def calculate_density(h):
    T = calculate_temperature(h)
    P = calculate_pressure(h)
    return (P * M) / (R * T)

#Функция силы гравитации
def calculate_gravitation_force(m, h):
    G = 6.6743*10**-11
    M = 5.2915158*10**22
    R = 600000
    Fgr = G*((M*m)/((R+h)**2))
    return Fgr

#Функция силы сопротивления
def calculate_resistance_force(q, v):
    c = 0.47
    r = 2
    S = pi*r**2
    Fs = c*S*q*v**2/2
    return Fs

#Функция ускорения
def calculate_acceleration(h, q, v, power, m):
    Fgr = calculate_gravitation_force(m, h)
    Fs = calculate_resistance_force(q, v)
    Ft_max = 1_357_730
    a = (power*Ft_max/100 - Fgr - Fs)/m
    return a

#Функция скорости
def calculate_velocity(power, h, v, m):
    q = calculate_density(h)
    a = calculate_acceleration(h, q, v, power, m)
    v = v + a
    return v

#Начальные параметры
h = 87
v = 0
m = 52700
power = 100
t = 0

#Массивы для вывода графиков
speed_data = []
high_data = []
mass_data = []
time_data = []

while t <= 78:
    if t == 64:
        m -= 9000
        power = 22.7
    
    v = calculate_velocity(power, h, v, m)
    n = 485 * power/100
    h += v
    m = m - n
    
    time_data.append(int(t))
    speed_data.append(int(v))
    high_data.append(int(h))
    mass_data.append(int(m))
    t += 1

# Построение графиков
x = np.linspace(0, time_data[-1], len(time_data))  # Общее значение X для всех графиков
y1 = mass_data  # Первый график: масса
y2 = speed_data  # Второй график: скорость
y3 = high_data  # Третий график: высота

# Создание фигуры и осей
fig, axs = plt.subplots(3, 1, figsize=(10, 12))

for i, ax in enumerate(axs):
    # Переносим оси в (0,0)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # Стрелки на концах осей
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False, markersize=8)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False, markersize=8)

# Первый график
axs[0].plot(x, y1, color="blue", label="Масса", linewidth=2.5)
axs[0].set_xlabel('Время, t (с)', fontsize=12, fontweight='bold', loc='right')
axs[0].set_ylabel('Масса, m (кг)', fontsize=12, fontweight='bold', loc='top')
axs[0].set_title('Зависимость массы от времени', fontsize=13, loc='left', pad=10)
axs[0].grid(True, alpha=0.3, linestyle='--')
axs[0].legend(loc='upper right', fontsize=10)
axs[0].set_xlim(0, 80)

# Второй график
axs[1].plot(x, y2, color="red", label="Скорость", linewidth=2.5)
axs[1].set_xlabel('Время, t (с)', fontsize=12, fontweight='bold', loc='right')
axs[1].set_ylabel('Скорость, v (м/с)', fontsize=12, fontweight='bold', loc='top')
axs[1].set_title('Зависимость скорости от времени', fontsize=13, loc='left', pad=10)
axs[1].grid(True, alpha=0.3, linestyle='--')
axs[1].legend(loc='upper left', fontsize=10)
axs[1].set_xlim(0, 80)

# Третий график
axs[2].plot(x, y3, color="green", label="Высота", linewidth=2.5)
axs[2].set_xlabel('Время, t (с)', fontsize=12, fontweight='bold', loc='right')
axs[2].set_ylabel('Высота, h (м)', fontsize=12, fontweight='bold', loc='top')
axs[2].set_title('Зависимость высоты от времени', fontsize=13, loc='left', pad=10)
axs[2].grid(True, alpha=0.3, linestyle='--')
axs[2].legend(loc='upper left', fontsize=10)
axs[2].set_xlim(0, 80)

# Настройка общего расстояния между графиками
plt.tight_layout()

# Показ графиков
plt.show()
