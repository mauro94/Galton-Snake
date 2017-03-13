
# Galton Snake
# Mauro Amarante A01191903
# Patricio Sanchez A01191893



# LEX
import ply.lex as lex

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

# A string containing ignored characters (spaces and tabs)
t_ignore = " \t"

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lex.lex()



# YACC
import ply.yacc as yacc

# Global Variables
functionDirectory = { }
constantTable = { }
current_scope = 'global'
current_type = ''
current_sign = ''

# Starting grammar
start = 'PROGRAM'


# GRAMMARS
def p_ACCESS_COL(p):
    '''ACCESS_COL : id SA_FIND_ID '.' row '(' EXP ')' '''

def p_ACCESS_ROW(p):
    '''ACCESS_ROW : id SA_FIND_ID '.' col '(' EXP ')' '''

def p_ASSIGNMENT(p):
    '''ASSIGNMENT : id SA_FIND_ID '=' EXP ';' '''

def p_BIND_COLS(p):
    '''BIND_COLS : cbind '(' id SA_FIND_ID ',' ACCESS_COL ')' ';' '''

def p_BIND_ROWS(p):
    '''BIND_ROWS : rbind '(' id SA_FIND_ID ',' ACCESS_ROW ')' ';' '''

def p_BINDINGS(p):
    '''BINDINGS : BIND_ROWS 
                | BIND_COLS'''

def p_BLOCK(p):
    '''BLOCK : '{' BLOCK_INST BLOCK_STM '}' 
             | '{' BLOCK_INST BLOCK_STM return EXP '}' '''

def p_BLOCK_INST(p):
    '''BLOCK_INST : INSTANTIATE BLOCK_INST 
                  | empty'''

def p_BLOCK_STM(p):
    '''BLOCK_STM : STATEMENT BLOCK_STM 
                 | empty'''

def p_CALLFUNC(p):
    '''CALLFUNC : id SA_FIND_ID '(' CALLFUNC_PARAMS ')' ';' '''

def p_CALLFUNC_PARAMS(p):
    '''CALLFUNC_PARAMS : EXP
                       | EXP ','
                       | empty'''

def p_CONDITION(p):
    '''CONDITION : if '(' SUPER_EXPRESSION ')' BLOCK 
                 | if '(' SUPER_EXPRESSION ')' BLOCK else BLOCK'''

def p_CORR_HEADERS(p):
    '''CORR_HEADERS : correlateHeaders '(' TABLE_HEADER ',' TABLE_HEADER ',' VAR_CTE ')' ';' '''

def p_CORR(p):
    '''CORR : correlate '(' id SA_FIND_ID ',' id SA_FIND_ID ',' VAR_CTE ')' ';' '''

def p_CORRELATION(p):
    '''CORRELATION : CORR_HEADERS 
                   | CORR'''

def p_CREATE_DF(p):
    '''CREATE_DF : dataframe SA_NEW_DF '(' id SA_CREATE_VAR ',' '[' CREATE_DF_TAGS ']' ',' FILE_INPUT ')' ';' 
                 | dataframe SA_NEW_DF '(' id SA_CREATE_VAR ',' FILE_INPUT ')' ';' '''

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
              | '+' SA_NEW_SIGN VAR_CTE 
              | '-' SA_NEW_SIGN VAR_CTE 
              | VAR_CTE'''

def p_FILE_INPUT(p):
    '''FILE_INPUT : cte_string '.' csv'''

def p_FUNCTION(p):
    '''FUNCTION : void SA_VOID_FUNCTION func id SA_NEW_FUNCTION '(' PARAMETERS SA_FUNCTION_PARAMS ')' ':' BLOCK 
                | TYPE func id SA_NEW_FUNCTION '(' PARAMETERS SA_FUNCTION_PARAMS ')' ':' BLOCK'''
    del functionDirectory[current_scope]

def p_INSTANTIATE(p):
    '''INSTANTIATE : CREATE_DF 
                   | VARS'''

def p_LOOP(p):
    '''LOOP : while '(' SUPER_EXPRESSION ')' BLOCK'''

def p_OPERATION(p):
    '''OPERATION : BINDINGS 
                 | CORRELATION '''

def p_PARAMETERS(p):
    '''PARAMETERS : TYPE id ',' PARAMETERS 
                  | TYPE id'''
    

def p_PRINT_CELL(p):
    '''PRINT_CELL : printCell id SA_FIND_ID '[' EXP ',' EXP ']' ';' '''

def p_PRINT_COL(p):
    '''PRINT_COL : printCol TABLE_HEADER ';'
                 | printCol ACCESS_COL ';' '''

def p_PRINT_DATA(p):
    '''PRINT_DATA : printData id SA_FIND_ID ';' '''

def p_PRINT_HEADERS(p):
    '''PRINT_HEADERS : printHeaders id SA_FIND_ID ';' '''

def p_PRINT_ROW(p):
    '''PRINT_ROW : printRow id ACCESS_ROW ';' '''

def p_PRINT_TAGS(p):
    '''PRINT_TAGS : printTags id SA_FIND_ID ';' '''

def p_PRINT(p):
    '''PRINT : PRINT_COL
             | PRINT_TAGS
             | PRINT_DATA
             | PRINT_HEADERS
             | PRINT_CELL
             | PRINT_ROW'''

def p_PROGRAM(p):
    '''PROGRAM : SA_PROGRAM_START PROGRAM_VARS PROGRAM_FUNCTIONS main SA_MAIN_START ':' BLOCK'''
    functionDirectory.clear()

def p_PROGRAM_VARS(p):
    '''PROGRAM_VARS : INSTANTIATE PROGRAM_VARS
                    | empty'''

def p_PROGRAM_FUNCTIONS(p):
    '''PROGRAM_FUNCTIONS : FUNCTION PROGRAM_FUNCTIONS
                         | empty'''

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
    '''TABLE_HEADER : id SA_FIND_ID '$' id'''

def p_TERM(p):
    '''TERM : FACTOR
            | FACTOR '*' TERM
            | FACTOR '/' TERM'''

def p_TYPE(p):
    '''TYPE : int
            | float
            | char
            | string '''
    current_type = p[-1]

def p_VAR_CTE(p):
    '''VAR_CTE : id SA_FIND_ID
               | cte_float
               | cte_int
               | cte_char
               | cte_string
               | null'''

def p_VARS(p):
    '''VARS : TYPE VARS_ID ';' '''

def p_VARS_ID(p):
    '''VARS_ID : id SA_CREATE_VAR ',' VARS_ID
               | id SA_CREATE_VAR '''

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Syntax error at '%s'" % p.value)


# EXTRA GRAMMARS / SEMANTIC ACTIONS

def p_SA_FIND_ID(p):
  '''SA_FIND_ID : empty'''
  # Verify ids is in var table (not found error)
  if  not functionDirectory[current_scope][2].has_key(p[-1]):
    # ERROR
    print("ID does not exist '%s'" % p[-1])

def p_SA_PROGRAM_START(p):
  '''SA_PROGRAM_START : empty'''
  # Generate function directory
  current_type = 'void'
  functionDirectory[current_scope] = [current_type, [], {}]

def p_SA_MAIN_START(p):
  '''SA_MAIN_START : empty'''
  # Add main row to function directory
  current_type = 'void'
  current_scope = 'main'
  functionDirectory[current_scope] = [current_type, [], {}]

def p_SA_NEW_FUNCTION(p):
  '''SA_NEW_FUNCTION : empty'''
  # Add row to function directory with id, type add variable table
  current_scope = p[-1]
  functionDirectory[current_scope] = [current_type, [], {}]

def p_SA_FUNCTION_PARAMS(p):
  '''SA_FUNCTION_PARAMS : empty'''
  # Push id to params in function directory (if found error, else push)
  if functionDirectory[current_scope][2].has_key(p[-1]):
    # ERROR
    print("ID already exists '%s'" % p[-1])
  else:
    functionDirectory[current_scope][2][p[-1]] = [current_type]
    functionDirectory[current_scope][1].append(current_type)

def p_SA_NEW_DF(p):
  '''SA_NEW_DF : empty'''
  # current type = dataframe
  current_type = 'dataframe'

def p_SA_NEW_SIGN(p):
  '''SA_NEW_SIGN : empty'''
  # Current sign = sign
  current_sign = p[-1]

def p_SA_CREATE_VAR(p):
  '''SA_CREATE_VAR : empty'''
  # Search for id name in vars table if (found) error else add to vars table
  if functionDirectory[current_scope][2].has_key(p[-1]):
    # ERROR
    print("ID already exists '%s'" % p[-1])
  else:
    functionDirectory[current_scope][2][p[-1]] = [current_type]

def p_SA_VOID_FUNCTION(p):
  '''SA_VOID_FUNCTION : empty'''
  # Define current type to void
  current_type = 'void'


# PENDING

# def p_VAR_CTE_TWO(p): 
  '''VAR_CTE_TWO : empty'''
  #TODO - verify cte is in cte table (not found error)
  #PENDING CONSTANTS
  # ask if cst table is global and what should this table store

# def p_TABLE_HEADER_TWO(p):
  '''TABLE_HEADER_TWO : empty'''
  #TODO - verify if header id is in previous id (not found error)
  # PENDING CREATE DATAFRAME DS for search of header in dataframe

# def p_ASSIGNMENT_TWO(p):
  '''ASSIGNMENT_TWO : empty'''
  #TODO - Assign new value to var in varstable
  # PENDING ASSIGN VALUE IN VARIABLE TABLE DS, should value be stored in this table?

# def p_FUNCTION_FOUR(p):
  '''FUNCTION_FOUR : empty'''
  #TODO - Set initial point for function gotofunction true
  # PENDING FUNCTION SEMANTIC

# def p_STATEMENT_ONE(p):
  '''STATEMENT_ONE : empty'''
  #TODO - set return point for the function after/before(?) callfunc
  #PENDING FUNCTION SEMANTIC SHIT


# Build the parser
yacc.yacc()

#test
#file = open ("test2.txt", "r");
#yacc.parse(file.read())