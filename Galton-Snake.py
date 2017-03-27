# Galton Snake
# Mauro Amarante A01191903
# Patricio Sanchez A01191893

import sys
from collections import deque
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

# -------------------------- LEX --------------------------
import ply.lex as lex

# Reserved words
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

# Tokens
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

# Regex
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
    t.type = reserved.get(t.value, 'file')
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

# Error handling
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build lexer
lex.lex()

# -------------------------- YACC --------------------------
import ply.yacc as yacc

# Global Variables
functionDirectory = {} # {functionName : [functionType, [paramTypeList], #parameters, #localvariables, #quadruplecounter, {varTable}] }
                        # varTable -> {varID : [type, value]}
constantTable = {}     # {constant : value}
current_scope = ''      # current scope in the program
current_type = ''       # current type being used
current_sign = ''       # current sign being used
operands = []           # Operands stack
types = []              # Types stack 
operators = []          # Operators stack
quadruples = deque([])  # quadruples queue
cont = 0                # quadruple counter  
paramCount = 0          # parameter counter
localVariableCount = 0  # local variable counter

# Starting grammar
start = 'PROGRAM'

# --------- GRAMMARS ---------
def p_ACCESS_COL(p):
    '''ACCESS_COL : id SA_FIND_ID period row lPar EXP rPar '''

def p_ACCESS_ROW(p):
    '''ACCESS_ROW : id SA_FIND_ID period col lPar EXP rPar '''

def p_ASSIGNMENT(p):
    '''ASSIGNMENT : id SA_FIND_ID equal EXP semi_colon
                  | id SA_FIND_ID equal CALLFUNC 
                  | VAR_ARR equal EXP semi_colon
                  | VAR_ARR equal CALLFUNC 
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
             | lBr BLOCK_INST BLOCK_STM return EXP semi_colon rBr '''

def p_BLOCK_INST(p):
    '''BLOCK_INST : INSTANTIATE BLOCK_INST 
                  | empty'''

def p_BLOCK_STM(p):
    '''BLOCK_STM : STATEMENT BLOCK_STM 
                 | empty'''

def p_CALLFUNC(p):
    '''CALLFUNC : id SA_FIND_FUNC_ID lPar CALLFUNC_PARAMS rPar semi_colon '''

def p_CALLFUNC_PARAMS(p):
    '''CALLFUNC_PARAMS : EXP coma CALLFUNC_PARAMS
                       | EXP
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
    '''CREATE_DF : dataframe SA_NEW_DF lPar id SA_CREATE_VAR coma lSqBr CREATE_DF_TAGS rSqBr coma file SA_DF_ADD_FILE rPar semi_colon 
                 | dataframe SA_NEW_DF lPar id SA_CREATE_VAR coma file SA_DF_ADD_FILE rPar semi_colon '''

def p_CREATE_DF_TAGS(p):
    '''CREATE_DF_TAGS : cte_string SA_ADD_DF_TAG coma CREATE_DF_TAGS
                      | cte_string SA_ADD_DF_TAG'''

def p_EXP(p):
    '''EXP : TERM 
           | TERM plus SA_EXP_3 EXP 
           | TERM minus SA_EXP_3 EXP'''

def p_EXPRESSION(p):
    '''EXPRESSION : EXP 
                  | EXP EXPRESSION_SYM EXP'''

def p_EXPRESSION_SYM(p):
    '''EXPRESSION_SYM : relop_ls SA_EXP_4
                      | relop_gr SA_EXP_4
                      | relop_lsequal SA_EXP_4
                      | relop_grequal SA_EXP_4
                      | relop_equals SA_EXP_4
                      | relop_notequal SA_EXP_4'''

def p_FACTOR(p):
    '''FACTOR : lPar EXPRESSION rPar 
              | plus SA_NEW_SIGN VAR_CTE 
              | minus SA_NEW_SIGN VAR_CTE 
              | VAR_CTE'''

def p_FUNCTION(p):
    '''FUNCTION : func void SA_VOID_FUNCTION id SA_NEW_FUNCTION lPar PARAMETERS rPar colon BLOCK SA_END_FUNCTION
                | func TYPE id SA_NEW_FUNCTION lPar PARAMETERS rPar colon BLOCK SA_END_FUNCTION'''

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
                  | empty'''
    

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
    '''PROGRAM : SA_PROGRAM_START PROGRAM_VARS PROGRAM_FUNCTIONS main SA_MAIN_START colon BLOCK SA_END_PROGRAM'''

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
    '''SUPER_EXPRESSION : EXPRESSION SA_EXP_6
                        | EXPRESSION SA_EXP_6 relop_and SA_EXP_5 EXPRESSION 
                        | EXPRESSION SA_EXP_6 relop_or SA_EXP_5 EXPRESSION'''

def p_TABLE_HEADER(p):
    '''TABLE_HEADER : id SA_FIND_ID money_sign id SA_DF_FIND_HEADER_ID'''

def p_TERM(p):
    '''TERM : FACTOR
            | FACTOR times SA_EXP_2 TERM
            | FACTOR divide SA_EXP_2 TERM'''

def p_TYPE(p):
    '''TYPE : int SA_TYPE
            | float SA_TYPE
            | char SA_TYPE
            | string SA_TYPE
            | bool SA_TYPE'''

def p_VAR_ARR(p):
    '''VAR_ARR : id SA_FIND_ID lSqBr EXP rSqBr '''

def p_VAR_CTE(p):
    '''VAR_CTE : id SA_FIND_ID SA_EXP_1
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
               | id SA_CREATE_VAR lSqBr cte_int rSqBr coma VARS_ID
               | id SA_CREATE_VAR lSqBr cte_int rSqBr'''

# Empty grammar
def p_empty(p):
    'empty :'
    pass

# Error
def p_error(p):
    print("Syntax error at '%s'" % p.value)


# --------- EXTRA GRAMMARS / SEMANTIC ACTIONS ---------

# ID is declared.
# Verify ids is in var table. If not found declare error.
def p_SA_FIND_ID(p):
  '''SA_FIND_ID : empty'''
  # search for id in current varTable and in global varTable
  if not (varTable(functionDirectory, current_scope).has_key(p[-1]) or varTable(functionDirectory, 'global').has_key(p[-1])):
    # print error message
    print("ID does not exist '%s'" % p[-1])


# A function is being called.
# Verify ids is in function directory. If not found declare error.
def p_SA_FIND_FUNC_ID(p):
  '''SA_FIND_FUNC_ID : empty'''
  # search for function id in function directory
  if not p[-1] in functionDirectory.keys() :
    # print error message
    print("Function ID does not exist '%s'" % p[-1])


# A new porgram is created.
# Create function directory
def p_SA_PROGRAM_START(p):
  '''SA_PROGRAM_START : empty'''
  # global variables
  global current_type, current_scope
  # define current_type and current_scope
  current_type = 'void'
  current_scope = 'global'
  # create global function in function directory
  newFunction(functionDirectory, current_scope, current_type)


# Main function is declared.
# Add main function to function directory
def p_SA_MAIN_START(p):
  '''SA_MAIN_START : empty'''
  # global variables
  global current_type, current_scope
  # define current_type and current_scope
  current_type = 'void'
  current_scope = 'main'
  # create main function in function directory
  newFunction(functionDirectory, current_scope, current_type)


# New function is declared.
# Add new function to function directory with id, type add varTable. If not found declare error.
def p_SA_NEW_FUNCTION(p):
  '''SA_NEW_FUNCTION : empty'''
  # global variables
  global current_scope
  # define current_scope
  current_scope = p[-1]
  # verify if function id already exists
  if functionDirectory.has_key(current_scope):
    # print error message
    print("Function ID already exists '%s'" % p[-1])
  else:
    # create new function in function directory
    newFunction(functionDirectory, current_scope, current_type)


# Parameters are declared in function.
# Add paramaters types to function in function directory and variables to varTable. If not found declare error.
def p_SA_CREATE_PARAMS(p):
  '''SA_CREATE_PARAMS : empty'''
  # global variables
  global paramCount
  # search for current function
  if varTable(functionDirectory, current_scope).has_key(p[-1]):
    # print error message
    print("Parameter already exists '%s'" % p[-1])
  else:
    # add variable to varTable
    varTable(functionDirectory, current_scope)[p[-1]] = [current_type]
    # add data type to signature
    funcSignature(functionDirectory, current_scope).append(current_type)
    # increase parameter counter
    paramCount += 1


# New dataframe is being created.
# Define current type as dataframe
def p_SA_NEW_DF(p):
  '''SA_NEW_DF : empty'''
  # global variables
  global current_type
  # define current_type
  current_type = 'dataframe'


# Tag specified in dataframe. 
# Add tag to current dataframe
def p_SA_ADD_DF_TAG(p):
  '''SA_ADD_DF_TAG : empty'''
  # verify if new tag already exists
  if dataframeTags(functionDirectory, current_scope, p).has_key(p[-1]):
    # print error message
    print("Tag already exists '%s'" % p[-1])
  else:
    # add new tag
    dataframeTags(functionDirectory, current_scope, p)[p[-1]] = None


# File specified in dataframe. 
# Add file name to current dataframe
def p_SA_DF_ADD_FILE(p):
  '''SA_DF_ADD_FILE : empty'''
  # verify if current dataframe contains tags
  if not p[-8] == None:
    # add file name
    varTable(functionDirectory, current_scope)[p[-8]].append(p[-1])
  else:
    # add file name
    varTable(functionDirectory, current_scope)[p[-4]].append(p[-1])


# Sign defined for variable. 
# Define current_sign
def p_SA_NEW_SIGN(p):
  '''SA_NEW_SIGN : empty'''
  # global variables
  global current_sign
  # define current_sign
  current_sign = p[-1]


# New variable is being created. 
# Add new variable to current varTable. If not found declare error.
def p_SA_CREATE_VAR(p):
  '''SA_CREATE_VAR : empty'''
  # global variables
  global localVariableCount
  # validate if current variable does already exists in current varTable and global varTable
  if varTable(functionDirectory, current_scope).has_key(p[-1]) or varTable(functionDirectory, 'global').has_key(p[-1]):
    # print error message
    print("ID already exists '%s'" % p[-1])
  else:
    #dataframe
    if current_type == 'dataframe':
      # create variable
      varTable(functionDirectory, current_scope)[p[-1]] = [current_type, {}, {}]
    #other variable type
    else:
      # create variable
      varTable(functionDirectory, current_scope)[p[-1]] = [current_type]
    # increase local variable counter
    localVariableCount += 1


# Void function found. 
# Define current_type to void
def p_SA_VOID_FUNCTION(p):
  '''SA_VOID_FUNCTION : empty'''
  # global variables
  global current_type
  # define current_type
  current_type = 'void'


# Program ended. 
# Clear function dictionary
def p_SA_END_PROGRAM(p):
  '''SA_END_PROGRAM : empty'''
  # global variables
  global functionDirectory
  # clear function dictionary
  functionDirectory.clear() 
  print operators
  print operands
  print types


# Type is declared. 
# Define current_type
def p_SA_TYPE(p):
  '''SA_TYPE : empty'''
  # global variables
  global current_type
  # define current_type
  current_type = p[-1]


# Table header ID is declared.
# Verify header id is in current dataframe. If not found declare error.
def p_SA_DF_FIND_HEADER_ID(p):
  '''SA_DF_FIND_HEADER_ID : empty'''
  # search for dataframe id and header id in current varTable and in global varTable
  if not (functionDirectory[current_scope][2][p[-3]][2].has_key(p[-1]) or functionDirectory['global'][2][p[-3]][2].has_key(p[-1])) :
    # print error message
    print("ID does not exist '%s'" % p[-1])

# Function ended. 
# Clear function varTable
def p_SA_END_FUNCTION(p):
  '''SA_END_FUNCTION : empty'''
  # global variables
  global functionDirectory
  # clear function varTable
  varTable(functionDirectory, current_scope).clear() 


# --------- EXTRA GRAMMARS / QUADRUPPLES ---------

# id was declared
# operands.Push(id.name) and operators.Push(id.type)
def p_SA_EXP_1(p):
  '''SA_EXP_1 : empty'''
  # push id name to operands
  stackPush(operands, p[-2])
  # push id type to operands
  # check if id is in current_scope or global
  if varTable(functionDirectory, current_scope).has_key(p[-2]):
    t = varTable(functionDirectory, current_scope)[p[-2]]
  else:
    t = varTable(functionDirectory, 'global')[p[-2]]
  # push
  stackPush(types, t[0])


# * or / was declared
# operators.Push(* or /)
def p_SA_EXP_2(p):
  '''SA_EXP_2 : empty'''
  # push * or /
  stackPush(operators, p[-1])


# + or - was declared
# operators.Push(+ or -)
def p_SA_EXP_3(p):
  '''SA_EXP_3 : empty'''
  # push + or -
  stackPush(operators, p[-1])


# [<, >, <=, >=, ==, !=] was declared
# operators.Push([<, >, <=, >=, ==, !=])
def p_SA_EXP_4(p):
  '''SA_EXP_4 : empty'''
  # push [<, >, <=, >=, ==, !=]
  stackPush(operators, p[-1])


# && or || was declared
# operators.Push(&& or ||)
def p_SA_EXP_5(p):
  '''SA_EXP_5 : empty'''
  # push && or ||
  stackPush(operators, p[-1])

# Verify && or || are at top of stack
# generate corresponding quadruple
def p_SA_EXP_6(p):
  '''SA_EXP_6 : empty'''
  # top stack
  op = stackTop(operators)
  # if && or || are at top of stack
  if op == '&&' or op == '||':
    # get righ and left operands 
    rightOp = stackPop(operands)
    leftOp = stackPop(operands)
    # get right and left operand types
    rightType = stackPop(types)
    leftType = stackPop(types)
    # get operator
    operator = stackPop(operators)
    # validate if operation is valid
    resultType = getResultType(leftOp, rightOp, operator)
    #valid operation
    if resultType > 0:
      #create quadruple
      createQuadruple(operator, leftOp, rightOp, ALGO)
      

# Build the parser
yacc.yacc()

# -------------------------- FILE IMPORTS --------------------------
from Cube import *
from Functions import *

# -------------------------- TEST --------------------------

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