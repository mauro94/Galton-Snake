literals = [ ':',';','(',')','{','}','[',']',',','=',
             '+','-','*','/','<','>','$']

reserved = {
   'if',
   'else',
   'int',
   'float',
   'row',
   'col',
   'cbind',
   'rbind',
   'return',
   'correlateHeaders',
   'correlate',
   'dataframe',
   'csv',
   'void',
   'func',
   'while',
   'printCell',
   'printCol',
   'printData',
   'printHeaders',
   'printRow',
   'printTags',
   'main',
   'int',
   'float',
   'char',
   'string',
   'null'
}

tokens = [
    'relop_grequal', 
    'relop_lsequal', 
    'relop_equals', 
    'relop_notequal', 
    'relop_and', 
    'relop_or', 
    'cte_string', 
    'cte_float', 
    'cte_int',
    'cte_char', 
    'id'
    ] + list(reserved)


relop_grequal = '>='
relop_lsequal = '<='
relop_equals = '=='
relop_notequal = '!='
relop_and = '&&'
relop_or = '||'


def t_cte_string(t):
    r'\".*\"'
    return t

def t_cte_float(t):
    r'[-+]?[0-9]+\.[0-9]+([Ee][\+-]?[0-9+])?'
    t.value = float(t.value)
    return t

def t_cte_char(t):
    r'\'.*\''
    return t

def t_cte_int(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_id(t):
    r'[A-Za-z]([A-Za-z]|[0-9])*'
    t.type = reserved.get(t.value,'id')
    return t

#que hacen estas cosas
t_ignore = " \t"

def t_newline(t):
    r'\n+'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# lex
import ply.lex as lex
lex.lex()

# gramaticas
def p_PROGRAM(p):
    '''PROGRAM : PROGRAM_VARS PROGRAM_FUNCTIONS main ':' BLOCK'''

def p_ACCESS_COL(p):
    '''ACCESS_COL : id '.' row '(' EXP ')' '''

def p_ACCESS_ROW(p):
    '''ACCESS_ROW : id '.' col '(' EXP ')' '''

def p_ASSIGNMENT(p):
    '''ASSIGNMENT : id '=' EXP ';' '''

def p_BIND_COLS(p):
    '''BIND_COLS : cbind '(' id ',' ACCESS_COL ')' ';' '''

def p_BIND_ROWS(p):
    '''BIND_ROWS : rbind '(' id ',' ACCESS_ROW ')' ';' '''

def p_BINDINGS(p):
    '''BINDINGS : BIND_ROWS 
                | BIND_COLS'''

def p_BLOCK(p):
    '''BLOCK : '{' BLOCK_INST BLOCK_STM '}' 
             | '{' BLOCK_INST BLOCK_STM return EXP '}' '''

def p_BLOCK_INST(p):
    '''BLOCK_INST : INSTANTIATE BLOCK_INST 
                  | '''

def p_BLOCK_STM(p):
    '''BLOCK_STM : STATEMENT BLOCK_STM 
                 | '''

def p_CALLFUNC(p):
    '''CALLFUNC : id '(' CALLFUNC_PARAMS ')' ';' '''

def p_CALLFUNC_PARAMS(p):
    '''CALLFUNC_PARAMS : EXP
                       | EXP ','
                       | '''

def p_CONDITION(p):
    '''CONDITION : if '(' SUPER_EXPRESSION ')' BLOCK 
                 | if '(' SUPER_EXPRESSION ')' BLOCK else BLOCK'''

def p_CORR_HEADERS(p):
    '''CORR_HEADERS : correlateHeaders '(' TABLE_HEADER ',' TABLE_HEADER ',' VAR_CTE ')' ';' '''

def p_CORR(p):
    '''CORR : correlate '(' id ',' id ',' VAR_CTE ')' ';' '''

def p_CORRELATION(p):
    '''CORRELATION : CORR_HEADERS 
                   | CORR'''

def p_CREATE_DF(p):
    '''CREATE_DF : dataframe '(' id ',' '[' CREATE_DF_TAGS ']' ',' FILE_INPUT ')' ';' 
                 | dataframe '(' id ',' FILE_INPUT ')' ';' '''

def p_CREATE_DF_TAGS(p):
    '''CREATE_DF_TAGS : cte_string ',' 
                      | cte_string'''

def p_EXP(p):
    '''EXP : TERM 
           | TERM '+' EXP 
           | TERM '-' EXP'''

def p_EXPRESSION(p):
    '''EXPRESSION : EXP 
                  | EXP EXPRESSION_SYM EXP'''

def p_EXPRESSION_SYM(p):
    '''EXPRESSION_SYM : '<' 
                      | '>' 
                      | relop_lsequal 
                      | relop_grequal 
                      | relop_equals 
                      | relop_notequal '''

def p_FACTOR(p):
    '''FACTOR : '(' EXPRESSION ')' 
              | '+' VAR_CTE 
              | '-' VAR_CTE 
              | VAR_CTE'''

def p_FILE_INPUT(p):
    '''FILE_INPUT : cte_string '.' csv'''

def p_FUNCTION(p):
    '''FUNCTION : void func id '(' PARAMETERS ')' ':' BLOCK 
                | TYPE func id '(' PARAMETERS ')' ':' BLOCK'''

def p_INSTANTIATE(p):
    '''INSTANTIATE : CREATE_DF 
                   | VARS'''

def p_LOOP(p):
    '''LOOP : while '(' SUPER_EXPRESSION ')' BLOCK'''

def p_OPERATION(p):
    '''OPERATION : BINDINGS 
                 | CORRELATION 
                 | CALLFUNC'''

def p_PARAMETERS(p):
    '''PARAMETERS : TYPE id ',' PARAMETERS 
                  | TYPE id'''

def p_PRINT_CELL(p):
    '''PRINT_CELL : printCell id '[' EXP ',' EXP ']' ';' '''

def p_PRINT_COL(p):
    '''PRINT_COL : printCol TABLE_HEADER ';'
                 | printCol ACCESS_COL ';' '''

def p_PRINT_DATA(p):
    '''PRINT_DATA : printData id ';' '''

def p_PRINT_HEADERS(p):
    '''PRINT_HEADERS : printHeaders id ';' '''

def p_PRINT_ROW(p):
    '''PRINT_ROW : printRow id ACCESS_ROW ';' '''

def p_PRINT_TAGS(p):
    '''PRINT_TAGS : printTags id ';' '''

def p_PRINT(p):
    '''PRINT : PRINT_COL
             | PRINT_TAGS
             | PRINT_DATA
             | PRINT_HEADERS
             | PRINT_CELL
             | PRINT_ROW'''

def p_PROGRAM_VARS(p):
    '''PROGRAM_VARS : INSTANTIATE PROGRAM_VARS
                    | '''

def p_PROGRAM_FUNCTIONS(p):
    '''PROGRAM_FUNCTIONS : FUNCTION PROGRAM_FUNCTIONS
         | '''

def p_STATEMENT(p):
    '''STATEMENT : ASSIGNMENT
                 | CONDITION
                 | OPERATION
                 | PRINT
                 | LOOP
                 | CALLFUNC'''

def p_SUPER_EXPRESSION(p):
    '''SUPER_EXPRESSION : EXPRESSION
                        | EXPRESSION relop_and EXPRESSION
                        | EXPRESSION relop_or EXPRESSION'''

def p_TABLE_HEADER(p):
    '''TABLE_HEADER : id '$' id'''

def p_TERM(p):
    '''TERM : FACTOR
            | FACTOR '*' TERM
            | FACTOR '/' TERM'''

def p_TYPE(p):
    '''TYPE : int
            | float
            | char
            | string'''

def p_VAR_CTE(p):
    '''VAR_CTE : id
               | cte_float
               | cte_int
               | cte_char
               | cte_string
               | null'''

def p_VARS(p):
    '''VARS : TYPE VARS_ID ';' '''

def p_VARS_ID(p):
    '''VARS_ID : id ',' VARS_ID
               | id'''

def p_error(p):
    print("Syntax error at '%s'" % p.value)

#Yacc
import ply.yacc as yacc
yacc.yacc()

#test
#file = open ("test2.txt", "r");
#yacc.parse(file.read())