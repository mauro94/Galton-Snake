# Galton Snake
# Mauro Amarante A01191903
# Patricio Sanchez A01191893

import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

# LEX
import ply.lex as lex

reserved = {
   'if' : 'if',
   'else' : 'else',
   'elseif' : 'elseif',
   'row' : 'row',
   'col' : 'col',
   'cbind' : 'cbind',
   'rbind' : 'rbind',
   'return' : 'return',
   'correlateHeaders' : 'correlateHeaders',
   'correlate' : 'correlate',
   'dataframe' : 'dataframe',
   'void' : 'void',
   'func' : 'func',
   'while' : 'while',
   'printCell' : 'printCell',
   'printCol' : 'printCol',
   'printData' : 'printData',
   'printHeaders' : 'printHeaders',
   'printRow' : 'printRow',
   'printTags' : 'printTags',
   'main' : 'main',
   'int' : 'int',
   'float' : 'float',
   'char' : 'char',
   'string' : 'string',
   'bool' : 'bool',
   'null' : 'null',
   'true' : 'true',
   'false' : 'false'
}

tokens = [
    'relop_grequal', 
    'relop_gr',
    'relop_ls',
    'relop_lsequal', 
    'relop_equals', 
    'relop_notequal', 
    'relop_and', 
    'relop_or', 
    'cte_string', 
    'cte_float', 
    'cte_int',
    'cte_char', 
    'file',
    'id',
    'colon',
    'semi_colon',
    'lPar',
    'rPar',
    'lBr',
    'rBr',
    'lSqBr',
    'rSqBr',
    'coma',
    'equal',
    'plus',
    'minus',
    'times',
    'divide',
    'money_sign',
    'period'
    ] + list(reserved.values())


t_relop_gr = r'\>'
t_relop_ls = r'\<'
t_relop_grequal = r'\>\='
t_relop_lsequal = r'\<\='
t_relop_equals = r'\=\='
t_relop_notequal = r'\!\='
t_relop_and = r'\&\&'
t_relop_or = r'\|\|'
t_colon = r'\:'
t_semi_colon = r'\;'
t_lPar = r'\('
t_rPar = r'\)'
t_lBr = r'\{'
t_rBr = r'\}'
t_lSqBr = r'\['
t_rSqBr= r'\]'
t_coma = r'\,'
t_equal = r'\='
t_plus = r'\+'
t_minus = r'\-'
t_times = r'\*'
t_divide = r'\/'
t_money_sign = r'\$'
t_period = r'\.'

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

def t_file(t):
    r'[A-Za-z0-9\_\-]+.csv'
    t.value = reserved.get(t.value, 'file')
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
    '''ACCESS_COL : id SA_FIND_ID period row lPar EXP rPar '''

def p_ACCESS_ROW(p):
    '''ACCESS_ROW : id SA_FIND_ID period col lPar EXP rPar '''

def p_ASSIGNMENT(p):
    '''ASSIGNMENT : id SA_FIND_ID equal EXP semi_colon
                  | id SA_FIND_ID equal CALLFUNC semi_colon
                  | VAR_ARR equal EXP semi_colon
                  | VAR_ARR equal CALLFUNC semi_colon
                  | VAR_ARR equal lSqBr ASSIGNMENT_ARR rSqBr semi_colon '''

def p_ASSIGNMENT_ARR(p):
    '''ASSIGNMENT_ARR : EXP coma ASSIGNMENT_ARR
                      | EXP'''

def p_BIND_COLS(p):
    '''BIND_COLS : cbind lPar id SA_FIND_ID coma ACCESS_COL rPar semi_colon '''

def p_BIND_ROWS(p):
    '''BIND_ROWS : rbind lPar id SA_FIND_ID coma ACCESS_ROW rPar semi_colon '''

def p_BINDINGS(p):
    '''BINDINGS : BIND_ROWS 
                | BIND_COLS'''

def p_BLOCK(p):
    '''BLOCK : lBr BLOCK_INST BLOCK_STM rBr 
             | lBr BLOCK_INST BLOCK_STM return EXP rBr '''

def p_BLOCK_INST(p):
    '''BLOCK_INST : INSTANTIATE BLOCK_INST 
                  | empty'''

def p_BLOCK_STM(p):
    '''BLOCK_STM : STATEMENT BLOCK_STM 
                 | empty'''

def p_CALLFUNC(p):
    '''CALLFUNC : id SA_FIND_ID lPar CALLFUNC_PARAMS rPar semi_colon '''

def p_CALLFUNC_PARAMS(p):
    '''CALLFUNC_PARAMS : EXP
                       | EXP coma
                       | empty'''

def p_CONDITION(p):
    '''CONDITION : if lPar SUPER_EXPRESSION rPar BLOCK 
                 | if lPar SUPER_EXPRESSION rPar BLOCK elseif CONDITION_ELIF else BLOCK
                 | if lPar SUPER_EXPRESSION rPar BLOCK else BLOCK'''

def p_CONDITION_ELIF(p):
    '''CONDITION_ELIF : lPar SUPER_EXPRESSION rPar BLOCK elseif CONDITION_ELIF
                      | lPar SUPER_EXPRESSION rPar BLOCK'''

def p_CORR_HEADERS(p):
    '''CORR_HEADERS : correlateHeaders lPar TABLE_HEADER coma TABLE_HEADER coma VAR_CTE rPar semi_colon '''

def p_CORR(p):
    '''CORR : correlate lPar id SA_FIND_ID coma id SA_FIND_ID coma VAR_CTE rPar semi_colon '''

def p_CORRELATION(p):
    '''CORRELATION : CORR_HEADERS 
                   | CORR'''

def p_CREATE_DF(p):
    '''CREATE_DF : dataframe SA_NEW_DF lPar id SA_CREATE_VAR coma lSqBr CREATE_DF_TAGS rSqBr coma file rPar semi_colon 
                 | dataframe SA_NEW_DF lPar id SA_CREATE_VAR coma file rPar semi_colon '''

def p_CREATE_DF_TAGS(p):
    '''CREATE_DF_TAGS : cte_string coma CREATE_DF_TAGS
                      | cte_string'''

def p_EXP(p):
    '''EXP : TERM 
           | TERM plus EXP 
           | TERM minus EXP'''

def p_EXPRESSION(p):
    '''EXPRESSION : EXP 
                  | EXP EXPRESSION_SYM EXP'''

def p_EXPRESSION_SYM(p):
    '''EXPRESSION_SYM : relop_ls 
                      | relop_gr 
                      | relop_lsequal 
                      | relop_grequal 
                      | relop_equals 
                      | relop_notequal '''

def p_FACTOR(p):
    '''FACTOR : lPar EXPRESSION rPar 
              | plus SA_NEW_SIGN VAR_CTE 
              | minus SA_NEW_SIGN VAR_CTE 
              | VAR_CTE'''

def p_FUNCTION(p):
    '''FUNCTION : func void SA_VOID_FUNCTION id SA_NEW_FUNCTION lPar PARAMETERS rPar colon BLOCK 
                | func TYPE id SA_NEW_FUNCTION lPar PARAMETERS rPar colon BLOCK'''
    del functionDirectory[current_scope]

def p_INSTANTIATE(p):
    '''INSTANTIATE : CREATE_DF 
                   | VARS'''

def p_LOOP(p):
    '''LOOP : while lPar SUPER_EXPRESSION rPar BLOCK'''

def p_OPERATION(p):
    '''OPERATION : BINDINGS 
                 | CORRELATION '''

def p_PARAMETERS(p):
    '''PARAMETERS : TYPE id SA_CREATE_PARAMS coma PARAMETERS 
                  | TYPE id SA_CREATE_PARAMS
                  | '''
    

def p_PRINT_CELL(p):
    '''PRINT_CELL : printCell id SA_FIND_ID lSqBr EXP coma EXP rSqBr semi_colon '''

def p_PRINT_COL(p):
    '''PRINT_COL : printCol TABLE_HEADER semi_colon
                 | printCol ACCESS_COL semi_colon '''

def p_PRINT_DATA(p):
    '''PRINT_DATA : printData id SA_FIND_ID semi_colon '''

def p_PRINT_HEADERS(p):
    '''PRINT_HEADERS : printHeaders id SA_FIND_ID semi_colon '''

def p_PRINT_ROW(p):
    '''PRINT_ROW : printRow id ACCESS_ROW semi_colon '''

def p_PRINT_TAGS(p):
    '''PRINT_TAGS : printTags id SA_FIND_ID semi_colon '''

def p_PRINT(p):
    '''PRINT : PRINT_COL
             | PRINT_TAGS
             | PRINT_DATA
             | PRINT_HEADERS
             | PRINT_CELL
             | PRINT_ROW'''

def p_PROGRAM(p):
    '''PROGRAM : SA_PROGRAM_START PROGRAM_VARS PROGRAM_FUNCTIONS main SA_MAIN_START colon BLOCK'''
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
    '''TABLE_HEADER : id SA_FIND_ID money_sign id'''

def p_TERM(p):
    '''TERM : FACTOR
            | FACTOR times TERM
            | FACTOR divide TERM'''

def p_TYPE(p):
    '''TYPE : int
            | float
            | char
            | string 
            | bool'''
    current_type = p[-1]

def p_VAR_ARR(p):
    '''VAR_ARR : id lSqBr EXP rSqBr '''

def p_VAR_CTE(p):
    '''VAR_CTE : id SA_FIND_ID
               | cte_float
               | cte_int
               | cte_char
               | cte_string
               | true
               | false
               | VAR_ARR
               | null'''

def p_VARS(p):
    '''VARS : TYPE VARS_ID semi_colon '''

def p_VARS_ID(p):
    '''VARS_ID : id SA_CREATE_VAR coma VARS_ID
               | id SA_CREATE_VAR 
               | id SA_CREATE_VAR lSqBr EXP rSqBr coma VARS_ID
               | id SA_CREATE_VAR lSqBr EXP rSqBr'''

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Syntax error at '%s'" % p.value)


# EXTRA GRAMMARS / SEMANTIC ACTIONS

def p_SA_FIND_ID(p):
  '''SA_FIND_ID : empty'''
  # Verify ids is in var table (not found error)
  if not (functionDirectory[current_scope][2].has_key(p[-1]) or functionDirectory['global'][2].has_key(p[-1])) :
    # ERROR
    print("ID does not exist '%s'" % p[-1])

def p_SA_PROGRAM_START(p):
  '''SA_PROGRAM_START : empty'''
  # Generate function directory
  global current_type, current_scope
  current_type = 'void'
  current_scope = 'global'
  functionDirectory[current_scope] = [current_type, [], {}]

def p_SA_MAIN_START(p):
  '''SA_MAIN_START : empty'''
  # Add main row to function directory
  global current_type, current_scope
  current_type = 'void'
  current_scope = 'main'
  functionDirectory[current_scope] = [current_type, [], {}]

def p_SA_NEW_FUNCTION(p):
  '''SA_NEW_FUNCTION : empty'''
  # Add row to function directory with id, type add variable table
  global current_scope
  current_scope = p[-1]
  functionDirectory[current_scope] = [current_type, [], {}]

def p_SA_CREATE_PARAMS(p):
  '''SA_CREATE_PARAMS : empty'''
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
  global current_type
  current_type = 'dataframe'

def p_SA_NEW_SIGN(p):
  '''SA_NEW_SIGN : empty'''
  # Current sign = sign
  global current_sign
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
  global current_type
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
if __name__ == '__main__':
  # Check for file
  if (len(sys.argv) > 1):
    file = sys.argv[1]
    # Open file
    try:
      f = open(file, 'r')
      data = f.read()
      f.close()
      # Parse the data
      if (yacc.parse(data, tracking = True) == 'OK'):
        print(dirProc);
    except EOFError:
        print(EOFError)
  else:
    print('File missing')
    while 1:
        try:
            s = raw_input('')
        except EOFError:
            break
        if not s:
            continue
        yacc.parse(s)