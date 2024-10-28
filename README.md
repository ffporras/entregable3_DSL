# Descripción General
Este proyecto implementa una Fluent API para construir consultas SQL y un sistema de traducción entre SQL y una sintaxis simplificada, denominada USQL.
 
## Estructura del Proyecto
- **FluentApiSQL**:
 - `traeme(columns)`: Selecciona columnas (o todas si no se especifican).
 - `de_la_tabla(table)`: Especifica la tabla.
 - `donde(condition)`: Añade una condición WHERE.
 - `ordena_por(column, order)`: Ordena los resultados.
 - `agrupando_por(column)`: Agrupa los resultados.
 - `mezclar_con(table, condition)`: Realiza una operación JOIN.
 - `contar()`: Devuelve un conteo de resultados.
 - `build()`: Construye y retorna la consulta SQL completa.
 
- **traductor_SQLaUSQL**:
 - Traduce consultas SQL estándar a USQL.
 
- **traductor_USQLaSQL**:
 - Traduce consultas en USQL a SQL ejecutable.
 
- **main**:
 - `crear_base_de_datos()`: Crea una base de datos de ejemplo para pruebas.
 - `probar_traductor_y_api()`: Testea el funcionamiento de los traductores y la API fluida.
 
## Ejecución del Proyecto
 
### Requisitos
- **Python 3.x**
- **SQLite3**: para manejar la base de datos local.
 
### Instalación y Ejecución
1. Clonar el repositorio y navegar al directorio del proyecto.
2. Ejecutar el archivo principal:
 
   ```bash
   python main.py
   ```
 
  Esto creará una base de datos `mi_base_de_datos.db` con datos de prueba y mostrará ejemplos de uso de la API Fluent y la traducción de USQL a SQL.
 
## Cobertura de Pruebas
Se ha implementado un conjunto de pruebas que incluye un informe de cobertura detallado para evaluar el rendimiento y la precisión de los componentes del sistema. Este informe está disponible en el directorio `/tests/cobertura` y permite verificar qué partes del código han sido cubiertas por las pruebas.