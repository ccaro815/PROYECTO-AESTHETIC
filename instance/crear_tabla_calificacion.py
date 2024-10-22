import sqlite3


db_path = 'C:\\Users\\Flia Caro Sosa Veron\\OneDrive\\Desktop\\Proyecto-AESTETHIC\\instance\\Aestethic.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def crear_tabla_calificacion():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS calificacion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        servicio_id INTEGER NOT NULL,
        valor INTEGER NOT NULL CHECK (valor >= 1 AND valor <= 5),
        comentario TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (servicio_id) REFERENCES servicio (id)
    );
    """
    cursor.execute(create_table_query)
    print("Tabla 'calificacion' creada o ya existía.")


crear_tabla_calificacion()


conn.commit()


conn.close()
