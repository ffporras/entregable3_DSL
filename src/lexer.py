import ply.lex as lex

palabras_clave = (
    'TRAEME', 'TODO', 'DE_LA_TABLA', 'DONDE', 'AGRUPANDO_POR', 'MEZCLANDO', 'EN', 'LOS_DISTINTOS', 'CONTANDO', 'METE_EN',
    'LOS_VALORES', 'ACTUALIZA', 'SETEA', 'BORRA_DE_LA', 'ORDENA_POR', 'COMO_MUCHO', 'WHERE_DEL_GROUP_BY', 'EXISTE', 'EN_ESTO',
    'ENTRE', 'PARECIDO_A', 'ES_NULO', 'CAMBIA_LA_TABLA', 'AGREGA_LA_COLUMNA', 'ELIMINA_LA_COLUMNA', 'CREA_LA_TABLA', 
    'TIRA_LA_TABLA', 'POR_DEFECTO', 'UNICO', 'CLAVE_PRIMA', 'CLAVE_REFERENTE', 'NO_NULO', 'TRANSFORMA_A',
    'Y', 'O', 'COUNT', 'VARCHAR',
)

operadores_alfanumericos = (
    'NOMBRE', 'NUMERO', 'STRING',
)

operadores_aritemticos = (
    'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 'IGUAL', 
)

simbolos = (
    'PARENIZQ', 'PARENDER', 'PUNTO_COMA', 'PUNTO',
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

t_NOMBRE = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_STRING = r'\'[^\']*\''
t_NUMERO = r'\d+'

t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_IGUAL = r'='

t_PARENIZQ = r'\('
t_PARENDER = r'\)'
t_PUNTO_COMA = r';'
t_PUNTO = r'.'

#Ignora espacios y tabulaciones
t_ignore = " \t"

#Maneja nuevos saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

#Maneja errores léxicos
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left','SUMA','RESTA'),
    ('left','MULTIPLICACION','DIVISON'),
    ('right','UMENOS'),
    ('left', 'Y', 'O'), 
)

# Gramatica para consultas básicas
def p_statement_select(t):
    'statement : TRAEME columns DE_LA_TABLA NAME condition'
    t[0] = f"SELECT {t[2]} FROM {t[4]} {t[5]}"

def p_columns_all(t):
    'columns : TODO'
    t[0] = "*"

def p_columns_distinct(t):
    'columns : LOS_DISTINTOS NOMBRE'
    t[0] = f"DISTINCT {t[2]}"

def p_condition_where(t):
    'condition : DONDE NOMBRE comparison value'
    t[0] = f"WHERE {t[2]} {t[3]} {t[4]}"

def p_value_number(t):
    '''value : NUMBER
             | STRING'''
    t[0] = t[1]

def p_comparison_gt(t):
    '''comparison : ">" 
                  | "<" 
                  | "="'''
    t[0] = t[1]

def p_statement_insert(t):
    'statement : METE_EN NAME PARENIZQ columns_list RPAREN LOS_VALORES PARENIZQ values_list PARENDER'
    t[0] = f"INSERT INTO {t[2]} ({t[4]}) VALUES ({t[8]})"

def p_columns_list(t):
    'columns_list : NOMBRE'
    t[0] = t[1]

def p_values_list(t):
    'values_list : value'
    t[0] = t[1]

def p_statement_update(t):
    'statement : ACTUALIZA NOMBRE SETEA assignments DONDE condition'
    t[0] = f"UPDATE {t[2]} SET {t[4]} WHERE {t[6]}"

def p_assignments(t):
    'assignments : NOMBRE "=" value'
    t[0] = f"{t[1]} = {t[3]}"

def p_statement_delete(t):
    'statement : BORRA_DE_LA NOMBRE DONDE condition'
    t[0] = f"DELETE FROM {t[2]} WHERE {t[4]}"

def p_error(t):
    print("Syntax error at '%s'" % t.value)

def test_manual_parse(consulta):
    lexer.input(consulta)  # Cargar la consulta en el lexer
    while True:
        token = lexer.token()  # Obtener el siguiente token
        if not token:  # Si no hay más tokens, salir
            break
        print(f"Token: {token.type}, Valor: {token.value}, Línea: {token.lineno}, Posición: {token.lexpos}")

if __name__ == '__main__':
    # Prueba manualmente
    test_manual_parse("TRAEME TODO DE_LA_TABLA usuarios DONDE edad > 18;")
    test_manual_parse("METE_EN usuarios (nombre, edad) LOS_VALORES ('Juan', 25);")