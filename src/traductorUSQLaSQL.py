import ply.lex as lex
import ply.yacc as yacc


palabras_clave = (
    'TRAEME', 'TODO', 'DE_LA_TABLA', 'DONDE', 'AGRUPANDO_POR', 'MEZCLANDO', 'EN', 'LOS_DISTINTOS', 'CONTANDO', 'METE_EN',
    'LOS_VALORES', 'ACTUALIZA', 'SETEA', 'BORRA_DE_LA', 'ORDENA_POR', 'COMO_MUCHO', 'WHERE_DEL_GROUP_BY', 'EXISTE', 'EN_ESTO',
    'ENTRE', 'PARECIDO_A', 'ES_NULO', 'CAMBIA_LA_TABLA', 'AGREGA_LA_COLUMNA', 'ELIMINA_LA_COLUMNA', 'CREA_LA_TABLA', 
    'TIRA_LA_TABLA', 'POR_DEFECTO', 'UNICO', 'CLAVE_PRIMA', 'CLAVE_REFERENTE', 'NO_NULO', 'TRANSFORMA_A',
    'Y', 'O', 'COUNT', 'VARCHAR', #Estos son agregados de la lista original
)

operadores_alfanumericos = (
    'NOMBRE', 'NUMERO', 'STRING',
)

operadores_aritemticos = (
    'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 'IGUAL', 'MAYOR_QUE', 'MENOR_QUE', 'MAYOR_IGUAL', 'MENOR_IGUAL'
)

simbolos = (
    'PARENIZQ', 'PARENDER', 'PUNTO_COMA', 'PUNTO', 'COMA',
)
tokens = palabras_clave + operadores_alfanumericos + operadores_aritemticos + simbolos

t_TRAEME = r'TRAEME'
t_TODO = r'TODO'
t_DE_LA_TABLA = r'DE\s+LA\s+TABLA'
t_DONDE = r'DONDE'
t_LOS_DISTINTOS = r'LOS\s+DISTINTOS'
t_AGRUPANDO_POR = r'AGRUPANDO\s+POR'
t_MEZCLANDO = r'MEZCLANDO'
t_EN = r'EN'
t_CONTANDO = r'CONTANDO'
t_METE_EN = r'METE\s+EN'
t_LOS_VALORES = r'LOS\s+VALORES'
t_ACTUALIZA = r'ACTUALIZA'
t_SETEA = r'SETEA'
t_BORRA_DE_LA = r'BORRA\s+DE\s+LA'
t_ORDENA_POR = r'ORDENA\s+POR'
t_COMO_MUCHO = r'COMO\s+MUCHO'
t_EXISTE = r'EXISTE'
t_EN_ESTO = r'EN\s+ESTO'
t_ENTRE = r'ENTRE'
t_PARECIDO_A = r'PARECIDO\s+A'
t_ES_NULO = r'ES\s+NULO'
t_CAMBIA_LA_TABLA = r'CAMBIA\s+LA\s+TABLA'
t_AGREGA_LA_COLUMNA = r'AGREGA\s+LA\s+COLUMNA'
t_ELIMINA_LA_COLUMNA = r'ELIMINA\s+LA\s+COLUMNA'
t_CREA_LA_TABLA = r'CREA\s+LA\s+TABLA'
t_TIRA_LA_TABLA = r'TIRA\s+LA\s+TABLA'
t_POR_DEFECTO = r'POR\s+DEFECTO'
t_UNICO = r'UNICO'
t_CLAVE_PRIMA = r'CLAVE\s+PRIMA'
t_CLAVE_REFERENTE = r'CLAVE\s+REFERENTE'
t_NO_NULO = r'NO\s+NULO'
t_TRANSFORMA_A = r'TRANSFORMA\s+A'
t_Y = r'Y'
t_O = r'O'
t_COUNT = r'COUNT'
t_VARCHAR = r'VARCHAR'

#t_NOMBRE = r'[a-zA-Z_][a-zA-Z0-9_]*'
def t_NOMBRE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.upper() in palabras_clave:
        print(f"Token encontrado: {t.value} como {t.value.upper()}")  # Imprimir el token encontrado
        t.type = t.value.upper()  # Cambia el tipo de token si es una palabra clave
    else:
        print(f"Token encontrado: {t.value} como NOMBRE")  # Imprimir el token encontrado
    return t
t_STRING = r'\'[^\']*\''
t_NUMERO = r'\d+'

t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_IGUAL = r'='
t_MAYOR_QUE = r'>'
t_MENOR_QUE = r'<'
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='

t_PARENIZQ = r'\('
t_PARENDER = r'\)'
t_PUNTO_COMA = r';'
t_PUNTO = r'\.'
t_COMA = r','

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left','SUMA','RESTA'),
    ('left','MULTIPLICACION','DIVISION'),
    #('right','UMENOS'),
    ('left', 'Y', 'O'), 
)

#Gramatica para consultas básicas
def p_statement(t):
    '''statement : select_statement
                 | insert_statement
                 | update_statement
                 | delete_statement
                 | alter_statement'''
    t[0] = t[1]

#Reglas para SELECT
def p_select_statement(t):
    'select_statement : TRAEME columns DE_LA_TABLA NOMBRE condition_opt'
    t[0] = f"SELECT {t[2]} FROM {t[4]} {t[5]}"

def p_condition_opt(t):
    '''condition_opt : condition
                     | empty'''
    t[0] = t[1] if t[1] else ''

def p_empty(t):
    'empty :'
    pass

def p_columns(t):
    '''columns : TODO
               | columns_list'''
    if t[1] == 'TODO':
        t[0] = "*"
    else:
        t[0] = t[1]  

def p_columns_list(t):
    '''columns_list : NOMBRE
                    | columns_list COMA NOMBRE'''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = f"{t[1]}, {t[3]}"

def p_columns_distinct(t):
    'columns : LOS_DISTINTOS NOMBRE'
    t[0] = f"DISTINCT {t[2]}"

def p_condition_where(t):
    'condition : DONDE NOMBRE comparison value PUNTO_COMA'
    t[0] = f"WHERE {t[2]} {t[3]} {t[4]}"

def p_value(t):
    '''value : NUMERO
             | STRING'''
    t[0] = t[1]

def p_comparison_gt(t):
    '''comparison : MAYOR_QUE
                  | MENOR_QUE
                  | IGUAL
                  | MAYOR_IGUAL
                  | MENOR_IGUAL'''
    t[0] = t[1]

#Reglas para INSERT
def p_insert_statement(t):
    'insert_statement : METE_EN NOMBRE PARENIZQ columns_list PARENDER LOS_VALORES PARENIZQ values_list PARENDER PUNTO_COMA'
    t[0] = f"INSERT INTO {t[2]} ({t[4]}) VALUES ({t[8]})"

def p_columns_list(t):
    '''columns_list : NOMBRE
                    | columns_list COMA NOMBRE'''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = f"{t[1]}, {t[3]}"

def p_values_list(t):
    '''values_list : value
                   | values_list COMA value'''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = f"{t[1]}, {t[3]}"

#Reglas para UPDATE
def p_update_statement(t):
    'update_statement : ACTUALIZA NOMBRE SETEA assignments DONDE condition PUNTO_COMA'
    t[0] = f"UPDATE {t[2]} SET {t[4]} WHERE {t[6]}"

def p_assignments(t):
    'assignments : NOMBRE IGUAL value'
    t[0] = f"{t[1]} = {t[3]}"

#Reglas para DELETE
def p_delete_statement(t):
    'delete_statement : BORRA_DE_LA NOMBRE DONDE condition PUNTO_COMA'
    t[0] = f"DELETE FROM {t[2]} WHERE {t[4]}"

#Reglas para ALTER
def p_alter_statement(t):
    'alter_statement : CAMBIA_LA_TABLA NOMBRE alter_actions PUNTO_COMA'
    t[0] = f"ALTER TABLE {t[2]} {t[3]}"

def p_alter_actions(t):
    '''alter_actions : AGREGA_LA_COLUMNA NOMBRE VARCHAR PARENIZQ NUMERO PARENDER NO_NULO
                     | ELIMINA_LA_COLUMNA NOMBRE'''
    
    if t[1] == 'AGREGA_LA_COLUMNA':
        t[0] = f"ADD COLUMN {t[2]} VARCHAR({t[4]}) NOT NULL"
    else:
        t[0] = f"DROP COLUMN {t[2]}"

def p_error(t):
    print(f"Syntax error at '{t.value}' '{t.type} {type(t.type)}'")

#Inicializamos parser
parser = yacc.yacc()

def traducir_usql_a_sql(consulta_usql):
    """
    Esta función toma una consulta en USQL y devuelve su equivalente en SQL.
    """
    lexer.input(consulta_usql)
    try:
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)  # Añadido para depuración: imprime los tokens generados
        resultado = parser.parse(consulta_usql)
        return resultado
    except Exception as e:
        print(f"Error al procesar la consulta USQL: {str(e)}")
        return None

if __name__ == '__main__':
    consulta_usql = "CAMBIA_LA_TABLA empleados AGREGA_LA_COLUMNA direccion VARCHAR(255) NO_NULO;"
    resultado = traducir_usql_a_sql(consulta_usql)
    print(resultado)  # Debería devolver: SELECT * FROM usuarios WHERE edad > 18;
 