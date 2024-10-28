import re
import sqlparse

# Diccionario de traducción SQL a USQL
sql_a_usql = {
    "SELECT": "TRAEME",
    "*": "TODO",
    "FROM": "DE LA TABLA",
    "WHERE": "DONDE",
    "GROUP BY": "AGRUPANDO POR",
    "JOIN": "MEZCLANDO",
    "ON": "EN",
    "DISTINCT": "LOS DISTINTOS",
    "COUNT": "CONTANDO",
    "INSERT INTO": "METE EN",
    "VALUES": "LOS VALORES",
    "UPDATE": "ACTUALIZA",
    "SET": "SETEA",
    "DELETE FROM": "BORRA DE LA TABLA",
    "ORDER BY": "ORDENA POR",
    "LIMIT": "COMO MUCHO",
    "HAVING": "WHERE DEL GROUP BY",
    "EXISTS": "EXISTE",
    "IN": "EN ESTO",
    "BETWEEN": "ENTRE",
    "LIKE": "PARECIDO A",
    "IS NULL": "ES NULO",
    "ALTER TABLE": "CAMBIA LA TABLA",
    "ADD COLUMN": "AGREGA LA COLUMNA",
    "DROP COLUMN": "ELIMINA LA COLUMNA",
    "CREATE TABLE": "CREA LA TABLA",
    "DROP TABLE": "TIRA LA TABLA",
    "DEFAULT": "POR DEFECTO",
    "UNIQUE": "UNICO",
    "PRIMARY KEY": "CLAVE PRIMA",
    "FOREIGN KEY": "CLAVE REFERENTE",
    "NOT NULL": "NO NULO",
    "CAST": "TRANSFORMA A",
}

def traducir_sql_a_usql(consulta_sql):
    # Procesar frases compuestas primero para evitar conflictos
    for sql_frase, usql_frase in sql_a_usql.items():
        consulta_sql = re.sub(rf'\b{re.escape(sql_frase)}\b', usql_frase, consulta_sql, flags=re.IGNORECASE)

    # Parsear la consulta SQL y procesar tokens
    parsed = sqlparse.parse(consulta_sql)[0]
    translated_tokens = []

    for token in parsed.tokens:
        token_str = token.value.upper().strip()
        
        # Intentar traducir usando el diccionario o mantener el token original si no hay traducción
        translated_token = sql_a_usql.get(token_str, token_str)
        
        # Manejar funciones con paréntesis como COUNT()
        if re.match(r"^[A-Z_]+\(.+\)$", token_str):
            palabra_clave, resto = token_str.split('(', 1)
            translated_token = f"{sql_a_usql.get(palabra_clave, palabra_clave)}({resto}"
        
        translated_tokens.append(translated_token)

    # Unir los tokens y ajustar el formato final
    final_query = " ".join(translated_tokens)
    final_query = re.sub(r'\(\s*', '(', final_query)
    final_query = re.sub(r'\s*\)', ')', final_query)
    final_query = re.sub(r'\s*,\s*', ', ', final_query)

    return final_query

# Ejemplos de uso
consultas_sql = [
    "SELECT * FROM usuarios WHERE edad > 18;",
    "SELECT DISTINCT nombre FROM clientes WHERE ciudad = 'Madrid';",
    "INSERT INTO usuarios (nombre, edad) VALUES ('Juan', 25);",
    "UPDATE empleados SET salario = 3000 WHERE puesto = 'ingeniero';",
    "SELECT * FROM pedidos JOIN clientes ON pedidos.cliente_id = clientes.id WHERE clientes.ciudad = 'Barcelona';",
    "SELECT COUNT() FROM ventas GROUP BY producto HAVING COUNT() > 5;",
    "DELETE FROM clientes WHERE edad BETWEEN 18 AND 25;",
    "ALTER TABLE empleados ADD COLUMN direccion VARCHAR(255) NOT NULL;",
    "ALTER TABLE empleados DROP COLUMN direccion;"
]

for consulta in consultas_sql:
    consulta_usql = traducir_sql_a_usql(consulta)
    print(consulta_usql)
