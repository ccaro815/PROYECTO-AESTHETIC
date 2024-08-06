#Borrar registros
import sqlite3

db_path = 'C:\\Users\\Flia Caro Sosa Veron\\Desktop\\PROYECTO-AESTHETIC\\instance\\users.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def eliminar_usuario(user_id):
    delete_query = "DELETE FROM user WHERE id = ?;"
    cursor.execute(delete_query, (user_id,))
    conn.commit()
    print(f"Usuario con ID {user_id} eliminado.")

user_id = int(input("Ingrese el ID del usuario que desea eliminar: "))
eliminar_usuario(user_id)

conn.close()


