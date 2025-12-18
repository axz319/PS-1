import krpc
import csv
import time

# Подключение к KSP
conn = krpc.connect(name="Flight Logger")
vessel = conn.space_center.active_vessel
engines = vessel.parts.engines

print(">> Логгер подключен к KSP.")
print(">> Ожидаем запуска двигателей...")

# Создаём streams для быстрого получения данных
altitude_stream = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
mass_stream = conn.add_stream(getattr, vessel, 'mass')
speed_stream = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'speed')
current_time = conn.add_stream(getattr, conn.space_center, 'ut')

# Ждём запуска двигателей
engine_active = conn.add_stream(getattr, engines[5], 'active')
while not engine_active():
    time.sleep(0.01)

# Двигатель запущен
start_time = conn.space_center.ut
print(">> Запуск! Начинаем запись...")

# Открываем CSV файл
with open('flight_logs.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Время', 'Масса', 'Скорость', 'Высота'])
    
    last_write = start_time
    
    # Запись
    while True:
        current = current_time()
        
        if current - last_write >= 0.1:
            time_flight = current - start_time
            
            if time_flight >= 180:
                break
            
            # Получаем данные
            mass = mass_stream()
            speed = speed_stream()
            altitude = altitude_stream()
            
            # Записываем данные
            writer.writerow([
                round(time_flight, 1),
                round(mass, 1),
                round(speed, 1),
                round(altitude, 1)
            ])
            
            f.flush()
            last_write = current
        
        time.sleep(0.01)

print(">> Запись завершена! Файл: flight_logs.csv")
