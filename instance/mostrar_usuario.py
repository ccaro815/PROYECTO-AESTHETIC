import sqlite3

db_path = 'C:\\Users\\Flia Caro Sosa Veron\\Desktop\\PROYECTO-AESTHETIC\\instance\\users.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def mostrar_usuarios():
    select_query = "SELECT * FROM user;"
    cursor.execute(select_query)
    usuarios = cursor.fetchall()
    if usuarios:
        for usuario in usuarios:
            print(usuario)
    else:
        print("No hay usuarios en la base de datos.")

mostrar_usuarios()

conn.close()
