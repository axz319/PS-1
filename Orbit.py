import krpc
import time

# Подключение к KSP
conn = krpc.connect(name="Sputnik-1")
vessel = conn.space_center.active_vessel
control = vessel.control

# Streams для эффективного получения данных
altitude_stream = conn.add_stream(getattr, vessel.flight(), "mean_altitude")
apoapsis_stream = conn.add_stream(getattr, vessel.orbit, "apoapsis_altitude")
periapsis_stream = conn.add_stream(getattr, vessel.orbit, "periapsis_altitude")
time_to_ap_stream = conn.add_stream(getattr, vessel.orbit, "time_to_apoapsis")

# Получение ресурсов текущей ступени
decouple_stage_resources = vessel.resources_in_decouple_stage(
    stage=control.current_stage - 1, 
    cumulative=False
)

# Подготовка к взлёту
control.throttle = 1.0
control.sas = True

# Обратный отсчёт
for i in range(3, 0, -1):
    print(f"{i}.. ")
    time.sleep(1)

print("\nЗапуск!\n")
control.activate_next_stage()
flight_start_time = time.time()

# Обновляем ресурсы после запуска
decouple_stage_resources = vessel.resources_in_decouple_stage(
    stage=control.current_stage - 1, 
    cumulative=False
)

# Вертикальный взлёт до 2 км
while altitude_stream() <= 2_000:
    time.sleep(0.2)

# Начало гравитационного разворота
print(">> Начинаем гравитационный разворот")
control.pitch = -1
control.sas_mode = vessel.control.sas_mode.prograde

# Ожидание выгорания топлива первой ступени
while True:
    fuel = decouple_stage_resources.amount("LiquidFuel")
    if fuel == 0:
        control.pitch = 0
        control.sas_mode = vessel.control.sas_mode.stability_assist
        time.sleep(1)
        control.activate_next_stage()
        print(f">> Отделение ступени. {time.time() - flight_start_time:.1f} с")
        
        # Обновляем ресурсы ступени
        decouple_stage_resources = vessel.resources_in_decouple_stage(
            stage=control.current_stage - 2, 
            cumulative=False
        )
        break
    time.sleep(0.2)

time.sleep(1)
control.pitch = -1
control.sas_mode = vessel.control.sas_mode.prograde

# Набор апогея
print(">> Ожидаем достижения нужного значения апогея")
pitch_fixed = False

while True:
    pitch = vessel.flight().pitch
    apoapsis = apoapsis_stream()
    
    # Достигли целевого апогея
    if apoapsis >= 915_000:
        control.throttle = 0.0
        control.pitch = 0
        control.sas_mode = vessel.control.sas_mode.stability_assist
        break
    
    # Выравниваем наклон при достижении горизонта
    if pitch < 30 and not pitch_fixed:
        control.pitch = 0
        control.sas_mode = vessel.control.sas_mode.stability_assist
        pitch_fixed = True
    
    time.sleep(0.02)

# Полёт к апогею
print(f">> Полёт к апогею. AP={apoapsis_stream():.0f} м")

while time_to_ap_stream() > 15:
    time.sleep(2)

# Подготовка к увеличению перигея
print(">> Настраиваемся на увеличение перигея")
control.sas_mode = vessel.control.sas_mode.prograde
control.throttle = 1.0

# Циркуляризация орбиты
print(">> Увеличиваем перигей")
while periapsis_stream() < 210_000:
    time.sleep(0.01)

control.throttle = 0.0
time.sleep(0.5)

print(f">> Орбита готова. {apoapsis_stream():.0f} x {periapsis_stream():.0f} м")

# Выпуск спутника
print(">> Выпуск спутника и его антенн")
time.sleep(5)
control.activate_next_stage()
time.sleep(5)
control.activate_next_stage()
time.sleep(8)
control.antennas = True

print(">> Миссия завершена!")
