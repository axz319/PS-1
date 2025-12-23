import csv
import matplotlib.pyplot as plt

from MathModel import run_math_model, MODELLING_TIME

# Имя файла с данными симуляции
CSV_FILENAME = "Files/flight_logs.csv"


def load_simulation_data():
    # Открываем CSV-файл и читаем строки
    time = []
    mass = []
    speed = []
    altitude = []

    with open(CSV_FILENAME, encoding="cp1251") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            t = float(row[0])
            m = float(row[1])
            v = float(row[2])
            h = float(row[3])

            # Ограничиваем данные временем моделирования
            if t <= MODELLING_TIME:
                time.append(t)
                mass.append(m)
                speed.append(v)
                altitude.append(h)
    
    return {
        "time": time,
        "mass": mass,
        "speed": speed,
        "altitude": altitude,
    }


def setup_axes(ax):
    # Оформление осей и сетки
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)


def plot_mass_time(model_data, sim_data):
    # График массы от времени
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        sim_data["time"],
        sim_data["mass"],
        color="#1E90FF",
        linewidth=2.0,
        label="Симуляция KSP",
    )
    ax.plot(
        model_data["time"],
        model_data["mass"],
        color="#00008B",
        linewidth=2.0,
        linestyle="--",
        label="Математическая модель",
    )

    ax.set_xlabel("Время, t (с)")
    ax.set_ylabel("Масса, m (кг)")
    ax.set_title("Зависимость массы от времени")

    setup_axes(ax)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_speed_time(model_data, sim_data):
    # График скорости от времени
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        sim_data["time"],
        sim_data["speed"],
        color="#FF6347",
        linewidth=2.0,
        label="Симуляция KSP",
    )
    ax.plot(
        model_data["time"],
        model_data["speed"],
        color="#8B0000",
        linewidth=2.0,
        linestyle="--",
        label="Математическая модель",
    )

    ax.set_xlabel("Время, t (с)")
    ax.set_ylabel("Скорость, v (м/с)")
    ax.set_title("Зависимость скорости от времени")

    setup_axes(ax)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_altitude_time(model_data, sim_data):
    # График высоты от времени
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        sim_data["time"],
        sim_data["altitude"],
        color="#32CD32",
        linewidth=2.0,
        label="Симуляция KSP",
    )
    ax.plot(
        model_data["time"],
        model_data["altitude"],
        color="#006400",
        linewidth=2.0,
        linestyle="--",
        label="Математическая модель",
    )

    ax.set_xlabel("Время, t (с)")
    ax.set_ylabel("Высота, h (м)")
    ax.set_title("Зависимость высоты от времени")

    setup_axes(ax)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_speed_altitude(model_data, sim_data):
    # График скорости от высоты
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        sim_data["altitude"],
        sim_data["speed"],
        color="#FF8C00",
        linewidth=2.0,
        label="Симуляция KSP",
    )
    ax.plot(
        model_data["altitude"],
        model_data["speed"],
        color="#FF4500",
        linewidth=2.0,
        linestyle="--",
        label="Математическая модель",
    )

    ax.set_xlabel("Высота, h (м)")
    ax.set_ylabel("Скорость, v (м/с)")
    ax.set_title("Зависимость скорости от высоты")

    setup_axes(ax)
    ax.legend()
    plt.tight_layout()
    plt.show()


def main():
    print("1 - Масса от времени")
    print("2 - Скорость от времени")
    print("3 - Высота от времени")
    print("4 - Скорость от высоты")

    choice = input("\nВведите номер графика (1-4): ").strip()

    # Расчёт математической модели и загрузка данных симуляции из таблицы
    model_data = run_math_model()
    sim_data = load_simulation_data()

    # Вызов нужной функции построения графика
    plots = {
        "1": plot_mass_time,
        "2": plot_speed_time,
        "3": plot_altitude_time,
        "4": plot_speed_altitude,
    }

    if choice in plots:
        plots[choice](model_data, sim_data)


if __name__ == "__main__":
    # Точка входа в программу
    main()
