import krpc
conn = krpc.connect(name='Status check')
print(conn.krpc.get_status().version)
print('Соединение установлено\nГотово к запуску')