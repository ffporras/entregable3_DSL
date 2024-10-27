import sqlite3
from traductorUSQLaSQL import *
from FluentApiSQL import *

# Función para crear la base de datos y la tabla
def crear_base_de_datos():
    # Conectar a la base de datos (se creará si no existe)
    conn = sqlite3.connect('mi_base_de_datos.db')
    cursor = conn.cursor()

    # Crear la tabla 'usuarios'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER NOT NULL,
        ciudad TEXT NOT NULL
    );
    ''')

    # Insertar algunos datos de ejemplo
    cursor.execute("INSERT INTO usuarios (nombre, edad, ciudad) VALUES ('Juan', 25, 'Madrid')")
    cursor.execute("INSERT INTO usuarios (nombre, edad, ciudad) VALUES ('Ana', 22, 'Barcelona')")
    cursor.execute("INSERT INTO usuarios (nombre, edad, ciudad) VALUES ('Luis', 30, 'Madrid')")
    cursor.execute("INSERT INTO usuarios (nombre, edad, ciudad) VALUES ('María', 28, 'Valencia')")

    # Confirmar los cambios
    conn.commit()
    # Cerrar la conexión
    conn.close()
    print("Base de datos y tabla creadas con datos de ejemplo.")

# Función para probar el traductor SQL y la API Fluent
def probar_traductor_y_api():
    # Probar el traductor SQL
    consulta_usql = "TRAEME TODO DE_LA_TABLA usuarios DONDE edad > 18;"
    resultado = traducir_usql_a_sql(consulta_usql)
    print("Consulta SQL traducida:", resultado)

    # Ejecutar la consulta en la base de datos
    conn = sqlite3.connect('mi_base_de_datos.db')
    cursor = conn.cursor()

    cursor.execute(resultado)
    filas = cursor.fetchall()

    # Mostrar resultados
    for fila in filas:
        print(fila)

    # Cerrar la conexión
    conn.close()

if __name__ == '__main__':
    crear_base_de_datos()  # Crea la base de datos y tabla
    probar_traductor_y_api()  # Prueba el traductor y la API Fluent
