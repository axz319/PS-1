from math import exp, pi

MODELLING_TIME = 500  # Время моделирования (секунды)
DELTA_T = 1           # Шаг времени по умолчанию (секунды)


def run_math_model(delta_t: float = DELTA_T):
    """
    Функция математической модели полета ракеты.
    Возвращает словарь с массивами time, mass, speed, altitude.
    """

    # ----- Физические константы атмосферы -----
    T0 = 288.15  # Температура на уровне моря (К)
    R = 8.314    # Универсальная газовая постоянная
    M = 0.029    # Молярная масса воздуха (кг/моль)
    P0 = 113250  # Давление на уровне старта (Па)

    # ----- Константы планеты (Кербин) -----
    G = 6.6743e-11          # Гравитационная постоянная
    PLANET_MASS = 5.2915158e22  # Масса планеты (кг)
    PLANET_RADIUS = 600000      # Радиус планеты (м)

    # ----- Параметры ракеты -----
    DRAG_COEFFICIENT = 0.47  # Коэффициент сопротивления
    ROCKET_RADIUS = 2        # Радиус ракеты (м)
    MAX_THRUST = 1_357_730   # Максимальная тяга (Н)
    FUEL_CONSUMPTION = 485   # Расход топлива при 100% тяге (кг/с)

    # ----- Начальные условия -----
    h = 87      # Начальная высота (м)
    v = 0       # Начальная скорость (м/с)
    m = 52700   # Начальная масса (кг)
    power = 100 # Начальная мощность двигателя (%)
    t = 0       # Начальное время (с)

    # ----- События полета -----
    STAGE_SEPARATION_TIME = 64     # Время отделения первой ступени (с)
    STAGE_MASS_DROP = 9000         # Масса первой ступени (кг)
    POWER_AFTER_SEPARATION = 22.7  # Мощность после отделения первой ступени (%)
    ENGINE_CUTOFF_TIME = 105       # Время отключения двигателей (с)

    # Флаги для отслеживания событий
    stage_separated = False
    engine_cutoff = False

    # ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
    def calculate_temperature(altitude):
        return max(altitude * (-0.0065) + T0, 250)

    def calculate_pressure(altitude):
        T = calculate_temperature(altitude)
        return P0 * exp(-(M * 9.81 * altitude) / (R * T))

    def calculate_density(altitude):
        T = calculate_temperature(altitude)
        P = calculate_pressure(altitude)
        return (P * M) / (R * T)

    def calculate_gravitation_force(mass, altitude):
        return G * ((PLANET_MASS * mass) / ((PLANET_RADIUS + altitude) ** 2))

    def calculate_resistance_force(air_density, velocity):
        S = pi * ROCKET_RADIUS ** 2
        return DRAG_COEFFICIENT * S * air_density * velocity ** 2 / 2

    def calculate_acceleration(altitude, air_density, velocity, thrust_percent, mass):
        F_gravity = calculate_gravitation_force(mass, altitude)
        F_drag = calculate_resistance_force(air_density, velocity)
        F_thrust = thrust_percent * MAX_THRUST / 100
        return (F_thrust - F_gravity - F_drag) / mass

    # ========== ОСНОВНОЙ ЦИКЛ ==========
    time_data = []
    mass_data = []
    speed_data = []
    high_data = []

    while t <= MODELLING_TIME:
        # События полета
        if not stage_separated and t >= STAGE_SEPARATION_TIME:
            m -= STAGE_MASS_DROP
            power = POWER_AFTER_SEPARATION
            stage_separated = True

        if not engine_cutoff and t >= ENGINE_CUTOFF_TIME:
            power = 0
            engine_cutoff = True

        # Расчет параметров
        air_density = calculate_density(h)
        acceleration = calculate_acceleration(h, air_density, v, power, m)

        v = v + acceleration * delta_t
        fuel_burned = FUEL_CONSUMPTION * power / 100 * delta_t

        # Обновление
        h += v * delta_t
        m = m - fuel_burned

        # Сохранение
        time_data.append(t)
        mass_data.append(m)
        speed_data.append(v)
        high_data.append(h)

        t += delta_t

    return {
        "time": time_data,
        "mass": mass_data,
        "speed": speed_data,
        "altitude": high_data,
    }
