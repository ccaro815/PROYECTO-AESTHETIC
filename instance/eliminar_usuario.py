import sqlite3

# Conectar a la base de datos
db_path = 'C:\\Users\\Flia Caro Sosa Veron\\Desktop\\PROYECTO-AESTHETIC\\instance\\users.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Función para eliminar un usuario por ID
def eliminar_usuario(user_id):
    delete_query = "DELETE FROM user WHERE id = ?;"
    cursor.execute(delete_query, (user_id,))
    conn.commit()
    print(f"Usuario con ID {user_id} eliminado.")

# Solicitar el ID del usuario a eliminar
user_id = int(input("Ingrese el ID del usuario que desea eliminar: "))
eliminar_usuario(user_id)

# Cerrar la conexión
conn.close()

import sqlite3

db_path = 'C:\\Users\\Flia Caro Sosa Veron\\Desktop\\PROYECTO-AESTHETIC\\instance\\users.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Función para obtener y mostrar todos los usuarios
def mostrar_usuarios():
    select_query = "SELECT * FROM user;"
    cursor.execute(select_query)
    usuarios = cursor.fetchall()
    if usuarios:
        for usuario in usuarios:
            print(usuario)
    else:
        print("No hay usuarios en la base de datos.")

# Mostrar los usuarios
mostrar_usuarios()

# Cerrar la conexión
conn.close()
