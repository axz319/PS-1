import matplotlib.pyplot as plt

from MathModel import run_math_model, MODELLING_TIME


def setup_axes(ax):
    # Оформление осей и сетки
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)


def plot_mass_time(model_data):
    # График массы от времени
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        model_data["time"],
        model_data["mass"],
        color="#00008B",
        linewidth=2.0,
        linestyle="-",
        label="Математическая модель",
    )

    ax.set_xlabel("Время, t (с)")
    ax.set_ylabel("Масса, m (кг)")
    ax.set_title("Зависимость массы от времени")

    setup_axes(ax)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_speed_time(model_data):
    # График скорости от времени
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        model_data["time"],
        model_data["speed"],
        color="#8B0000",
        linewidth=2.0,
        linestyle="-",
        label="Математическая модель",
    )

    ax.set_xlabel("Время, t (с)")
    ax.set_ylabel("Скорость, v (м/с)")
    ax.set_title("Зависимость скорости от времени")

    setup_axes(ax)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_altitude_time(model_data):
    # График высоты от времени
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        model_data["time"],
        model_data["altitude"],
        color="#006400",
        linewidth=2.0,
        linestyle="-",
        label="Математическая модель",
    )

    ax.set_xlabel("Время, t (с)")
    ax.set_ylabel("Высота, h (м)")
    ax.set_title("Зависимость высоты от времени")

    setup_axes(ax)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_speed_altitude(model_data):
    # График скорости от высоты
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        model_data["altitude"],
        model_data["speed"],
        color="#FF4500",
        linewidth=2.0,
        linestyle="-",
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
    print("ГРАФИКИ МАТЕМАТИЧЕСКОЙ МОДЕЛИ ПОЛЁТА РАКЕТЫ")
    print("1 - Масса от времени")
    print("2 - Скорость от времени")
    print("3 - Высота от времени")
    print("4 - Скорость от высоты")

    choice = input("\nВведите номер графика (1-4): ").strip()

    # Расчёт математической модели
    model_data = run_math_model()

    # Вызов нужной функции построения графика
    plots = {
        "1": plot_mass_time,
        "2": plot_speed_time,
        "3": plot_altitude_time,
        "4": plot_speed_altitude,
    }

    if choice in plots:
        plots[choice](model_data)
    else:
        print("Неверный выбор!")


if __name__ == "__main__":
    # Точка входа в программу
    main()
