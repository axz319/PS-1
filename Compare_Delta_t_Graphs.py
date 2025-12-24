3import matplotlib.pyplot as plt

from MathModel import run_math_model, MODELLING_TIME

# Два шага интегрирования для сравнения
DELTA_T1 = 1
DELTA_T2 = 0.1


def setup_axes(ax):
    # Оформление осей и сетки
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)


def plot_mass_time(model1, model2):
    # График массы от времени
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        model1["time"],
        model1["mass"],
        color="#00008B",
        linewidth=2.0,
        linestyle="-",
        label=f"Δt = {DELTA_T1}",
    )
    ax.plot(
        model2["time"],
        model2["mass"],
        color="#1E90FF",
        linewidth=2.0,
        linestyle="--",
        label=f"Δt = {DELTA_T2}",
    )

    ax.set_xlabel("Время, t (с)")
    ax.set_ylabel("Масса, m (кг)")
    ax.set_title("Зависимость массы от времени")

    setup_axes(ax)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_speed_time(model1, model2):
    # График скорости от времени
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        model1["time"],
        model1["speed"],
        color="#8B0000",
        linewidth=2.0,
        linestyle="-",
        label=f"Δt = {DELTA_T1}",
    )
    ax.plot(
        model2["time"],
        model2["speed"],
        color="#FF6347",
        linewidth=2.0,
        linestyle="--",
        label=f"Δt = {DELTA_T2}",
    )

    ax.set_xlabel("Время, t (с)")
    ax.set_ylabel("Скорость, v (м/с)")
    ax.set_title("Зависимость скорости от времени")

    setup_axes(ax)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_altitude_time(model1, model2):
    # График высоты от времени
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        model1["time"],
        model1["altitude"],
        color="#006400",
        linewidth=2.0,
        linestyle="-",
        label=f"Δt = {DELTA_T1}",
    )
    ax.plot(
        model2["time"],
        model2["altitude"],
        color="#32CD32",
        linewidth=2.0,
        linestyle="--",
        label=f"Δt = {DELTA_T2}",
    )

    ax.set_xlabel("Время, t (с)")
    ax.set_ylabel("Высота, h (м)")
    ax.set_title("Зависимость высоты от времени")

    setup_axes(ax)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_speed_altitude(model1, model2):
    # График скорости от высоты
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        model1["altitude"],
        model1["speed"],
        color="#FF4500",
        linewidth=2.0,
        linestyle="-",
        label=f"Δt = {DELTA_T1}",
    )
    ax.plot(
        model2["altitude"],
        model2["speed"],
        color="#FF8C00",
        linewidth=2.0,
        linestyle="--",
        label=f"Δt = {DELTA_T2}",
    )

    ax.set_xlabel("Высота, h (м)")
    ax.set_ylabel("Скорость, v (м/с)")
    ax.set_title("Зависимость скорости от высоты")

    setup_axes(ax)
    ax.legend()
    plt.tight_layout()
    plt.show()


def main():
    print("СРАВНЕНИЕ ГРАФИКОВ МАТЕМАТИЧЕСКОЙ МОДЕЛИ ПРИ РАЗНЫХ Δt")
    print("Δt1 =", DELTA_T1, "   Δt2 =", DELTA_T2)
    print("1 - Масса от времени")
    print("2 - Скорость от времени")
    print("3 - Высота от времени")
    print("4 - Скорость от высоты")

    choice = input("\nВведите номер графика (1-4): ").strip()

    # Расчёт математической модели для двух шагов
    model_data_1 = run_math_model(DELTA_T1)
    model_data_2 = run_math_model(DELTA_T2)

    plots = {
        "1": plot_mass_time,
        "2": plot_speed_time,
        "3": plot_altitude_time,
        "4": plot_speed_altitude,
    }

    if choice in plots:
        plots[choice](model_data_1, model_data_2)
    else:
        print("Неверный выбор!")


if __name__ == "__main__":
    main()
