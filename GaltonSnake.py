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
   'call' : 'call',
   'while' : 'while',
   'printCell' : 'printCell',
   'printCol' : 'printCol',
   'print' : 'print',
   'printHeaders' : 'printHeaders',
   'printRow' : 'printRow',
   'printTags' : 'printTags',
   'main' : 'main',
   'int' : 'int',
   'float' : 'float',
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
functionDirectory = {}  # {functionName : {functionType, [paramTypeList], #parameters, #localvariables, #quadruplecounter, {varTable}} }
                        # varTable -> {varID : {type, address, dimension}}
constantTable = {}      # {constant : {type, address, value} }
current_scope = ''      # current scope in the program
current_type = ''       # current type being used
current_sign = ''       # current sign being used
operands = []           # Operands stack
types = []              # Types stack 
operators = []          # Operators stack
quadruples = []         # quadruples list
jumps = []              # jumps stack
elseif_jumps = []       # elseif jumps stack
dimensions = []         # dimensions stack
current_dim = 0         # variable for current dimension
cont = 0                # quadruple counter  
paramCount = 0          # parameter counter
varCounter = 0          # local variable counter
callFunc_scopes = []    # stack of id of function call
pointers = []           # pointer stack
array_counter = 0       # value counter array
array_id = ''           # array id

# Memory counters
# 2,000 slots per block, dataframes 10,000 
globalVarCount = {}
globalVarCount['bool'] = 10000
globalVarCount['int'] = 12000
globalVarCount['float'] = 14000
globalVarCount['string'] = 16000
globalVarCount['dataframe'] = 20000

localVarCount = {}
localVarCount['bool'] = 40000
localVarCount['int'] = 42000
localVarCount['float'] = 44000
localVarCount['string'] = 46000
localVarCount['dataframe'] = 50000

tempVarCount = {}
tempVarCount['bool'] = 60000
tempVarCount['int'] = 62000
tempVarCount['float'] = 64000
tempVarCount['string'] = 66000
tempVarCount['dataframe'] = 70000

constVarCount = {}
constVarCount['bool'] = 80000
constVarCount['int'] = 82000
constVarCount['float'] = 84000
constVarCount['string'] = 86000

# Starting grammar
start = 'PROGRAM'

# --------- GRAMMARS ---------
def p_ACCESS_COL(p):
    '''ACCESS_COL : id SA_FIND_ID period row lPar EXP rPar '''

def p_ACCESS_ROW(p):
    '''ACCESS_ROW : id SA_FIND_ID period col lPar EXP rPar '''

def p_ASSIGNMENT(p):
    '''ASSIGNMENT : id SA_FIND_ID SA_EXP_1_ID equal SA_EXP_ADD_OP SUPER_EXPRESSION SA_EXP_10 semi_colon
                  | VAR_ARR equal SA_EXP_ADD_OP SUPER_EXPRESSION SA_EXP_10 semi_colon
                  | VAR_ARR equal SA_EXP_ADD_OP CALLFUNC SA_EXP_10 
                  | VAR_ARR equal SA_EXP_ADD_OP lSqBr SA_ARR_4 ASSIGNMENT_ARR rSqBr semi_colon '''

def p_ASSIGNMENT_ARR(p):
    '''ASSIGNMENT_ARR : EXP SA_ARR_5 coma ASSIGNMENT_ARR
                      | EXP SA_ARR_5'''

def p_BIND_COLS(p):
    '''BIND_COLS : cbind lPar id SA_FIND_ID coma ACCESS_COL rPar semi_colon '''

def p_BIND_ROWS(p):
    '''BIND_ROWS : rbind lPar id SA_FIND_ID coma ACCESS_ROW rPar semi_colon '''

def p_BINDINGS(p):
    '''BINDINGS : BIND_ROWS 
                | BIND_COLS'''

def p_BLOCK(p):
    '''BLOCK : lBr BLOCK_INST SA_FINAL_FUNC_VALUES BLOCK_STM rBr 
             | lBr BLOCK_INST SA_FINAL_FUNC_VALUES BLOCK_STM return EXP SA_RET semi_colon rBr '''

def p_BLOCK_INST(p):
    '''BLOCK_INST : INSTANTIATE BLOCK_INST 
                  | empty'''

def p_BLOCK_STM(p):
    '''BLOCK_STM : STATEMENT BLOCK_STM 
                 | empty'''

def p_CALLFUNC(p):
    '''CALLFUNC : call id SA_FIND_FUNC_ID lPar SA_CALLFUNC_2 CALLFUNC_PARAMS rPar SA_CALLFUNC_5 semi_colon SA_CALLFUNC_6'''

def p_CALLFUNC_EXP(p):
    '''CALLFUNC_EXP : id SA_FIND_FUNC_ID lPar SA_CALLFUNC_2 CALLFUNC_PARAMS rPar SA_CALLFUNC_5 SA_CALLFUNC_6 SA_CALLFUNC_7'''

def p_CALLFUNC_PARAMS(p):
    '''CALLFUNC_PARAMS : EXP SA_CALLFUNC_3 coma SA_CALLFUNC_4 CALLFUNC_PARAMS
                       | EXP SA_CALLFUNC_3
                       | empty'''

def p_CONDITION(p):
    '''CONDITION : if lPar SUPER_EXPRESSION rPar SA_COND_1 BLOCK SA_COND_2
                 | if lPar SUPER_EXPRESSION rPar SA_COND_1 BLOCK SA_COND_2 elseif SA_COND_4 CONDITION_ELIF else SA_COND_3 BLOCK SA_COND_5
                 | if lPar SUPER_EXPRESSION rPar SA_COND_1 BLOCK else SA_COND_3 BLOCK SA_COND_2'''

def p_CONDITION_ELIF(p):
    '''CONDITION_ELIF : lPar SUPER_EXPRESSION rPar SA_COND_1 BLOCK SA_COND_2 elseif SA_COND_4 CONDITION_ELIF
                      | lPar SUPER_EXPRESSION rPar SA_COND_1 BLOCK'''

def p_CORR_HEADERS(p):
    '''CORR_HEADERS : correlateHeaders lPar TABLE_HEADER coma TABLE_HEADER coma cte_float rPar semi_colon '''

def p_CORR(p):
    '''CORR : correlate lPar id SA_FIND_ID coma id SA_FIND_ID coma cte_float rPar semi_colon '''

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
    '''EXP : TERM SA_EXP_8
           | TERM SA_EXP_8 plus SA_EXP_ADD_OP EXP 
           | TERM SA_EXP_8 minus SA_EXP_ADD_OP EXP '''

def p_EXPRESSION(p):
    '''EXPRESSION : EXP SA_EXP_7
                  | EXP SA_EXP_7 EXPRESSION_SYM EXPRESSION'''

def p_EXPRESSION_SYM(p):
    '''EXPRESSION_SYM : relop_ls SA_EXP_ADD_OP
                      | relop_gr SA_EXP_ADD_OP
                      | relop_lsequal SA_EXP_ADD_OP
                      | relop_grequal SA_EXP_ADD_OP
                      | relop_equals SA_EXP_ADD_OP
                      | relop_notequal SA_EXP_ADD_OP'''

def p_FACTOR(p):
    '''FACTOR : lPar SA_FAKE_BOTTOM EXPRESSION SA_FAKE_BOTTOM_REMOVE rPar 
              | plus SA_NEW_SIGN VAR_CTE 
              | minus SA_NEW_SIGN VAR_CTE 
              | VAR_CTE '''

def p_FUNCTION(p):
    '''FUNCTION : func void SA_VOID_FUNCTION id SA_NEW_FUNCTION lPar PARAMETERS rPar colon BLOCK SA_END_FUNCTION
                | func TYPE id SA_NEW_FUNCTION lPar PARAMETERS rPar colon BLOCK SA_END_FUNCTION'''

def p_INSTANTIATE(p):
    '''INSTANTIATE : CREATE_DF 
                   | VARS'''

def p_LOOP(p):
    '''LOOP : while SA_LOOP_1 lPar SUPER_EXPRESSION rPar SA_LOOP_2 BLOCK SA_LOOP_3'''

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
    '''PRINT_DATA : print id SA_FIND_ID SA_PRINT_DATA semi_colon '''

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
                        | EXPRESSION SA_EXP_6 relop_and SA_EXP_ADD_OP SUPER_EXPRESSION 
                        | EXPRESSION SA_EXP_6 relop_or SA_EXP_ADD_OP SUPER_EXPRESSION'''

def p_TABLE_HEADER(p):
    '''TABLE_HEADER : id SA_FIND_ID money_sign id SA_DF_FIND_HEADER_ID'''

def p_TERM(p):
    '''TERM : FACTOR SA_EXP_9
            | FACTOR SA_EXP_9 times SA_EXP_ADD_OP TERM 
            | FACTOR SA_EXP_9 divide SA_EXP_ADD_OP TERM '''

def p_TYPE(p):
    '''TYPE : int SA_TYPE
            | float SA_TYPE
            | string SA_TYPE
            | bool SA_TYPE'''

def p_VAR_ARR(p):
    '''VAR_ARR : id SA_FIND_ID lSqBr SA_ARR_2 SA_FAKE_BOTTOM EXP SA_ARR_3 SA_FAKE_BOTTOM_REMOVE rSqBr '''

def p_VAR_CTE(p):
    '''VAR_CTE : id SA_FIND_ID SA_EXP_1_ID
               | cte_int SA_CREATE_CONST SA_EXP_1_CTE
               | cte_float SA_CREATE_CONST SA_EXP_1_CTE
               | cte_string SA_CREATE_CONST SA_EXP_1_CTE
               | true SA_CREATE_CONST SA_EXP_1_CTE 
               | false SA_CREATE_CONST SA_EXP_1_CTE
               | VAR_ARR 
               | null SA_CREATE_CONST SA_EXP_1_CTE
               | CALLFUNC_EXP'''

def p_VARS(p):
    '''VARS : TYPE VARS_ID semi_colon '''

def p_VARS_ID(p):
    '''VARS_ID : id SA_CREATE_VAR coma VARS_ID
               | id SA_CREATE_VAR 
               | id SA_CREATE_VAR lSqBr cte_int SA_ARR_1 rSqBr coma VARS_ID
               | id SA_CREATE_VAR lSqBr cte_int SA_ARR_1 rSqBr'''

# Empty grammar
def p_empty(p):
    'empty :'
    pass

# Error
def p_error(p):
    print("Syntax error at '%s'" % p.value)
    exit(1)


# --------- EXTRA GRAMMARS / SEMANTIC ACTIONS ---------

# File specified in dataframe. 
# Add file name to current dataframe
def p_SA_DF_ADD_FILE(p):
  '''SA_DF_ADD_FILE : empty'''
  # global variables
  global functionDirectory
  # get dataframe id
  varID = p[-8]
  # get file name
  file = p[-1]
  # define which grammar is active
  if (varID == None):
    # get dataframe id
    varID = p[-4]
  # add file name
  functionDirectory[current_scope]['varTable'][varID]['file'] = file



# Tag specified in dataframe. 
# Add tag to current dataframe
def p_SA_ADD_DF_TAG(p):
  '''SA_ADD_DF_TAG : empty'''
  # global variables
  global functionDirectory
  # get dataframe id
  varID = p[-5]
  # get tag
  tag = p[-1]
  # verify if new tag already exists
  if functionDirectory[current_scope]['varTable'][varID]['tags'].has_key(tag):
    # print error message
    print("Tag already exists '%s'" % tag)
    exit(1)
  else:
    # add new tag
    functionDirectory[current_scope]['varTable'][varID]['tags'][tag] = tag



# New constant. 
# Add new constant to constantTable. If not found ignore.
def p_SA_CREATE_CONST(p):
  '''SA_CREATE_CONST : empty'''
  # global variables
  global constantTable
  # get constant 
  constant = p[-1]
  # validate if current constant does already exists and create
  if not constantTable.has_key(str(constant)):
    # bool
    if constant == 'true' or constant == 'false':
      #define type code
      t = 1
      # define constant
      if str(constant) == 'true':
        cte = True
      else:
        cte = False
    # integer
    elif isinstance(constant, int):
      # define constant
      cte = int(constant)
      # validate curret sign
      if current_sign == '-':
        cte *= -1
        constant = str(cte)
      #define type code
      t = 2
    # float
    elif isinstance(constant, float):
      # define constant
      cte = float(constant)
      # validate curret sign
      if current_sign == '-':
        cte *= -1
        constant = str(cte)
      #define type code
      t = 3
    # string
    elif isinstance(constant, str):
      # define constant
      cte = str(constant)
      #define type code
      t = 4
    #create constant
    constantTable[str(constant)] = {'type': t, 'address': constVarCount[getTypeString(t)], 'val': cte}
    #increase constant variable counter
    constVarCount[getTypeString(t)] += 1



# Parameters are declared in function.
# Add paramaters types to function in function directory and variables to varTable. If not found declare error.
def p_SA_CREATE_PARAMS(p):
  '''SA_CREATE_PARAMS : empty'''
  # global variables
  global functionDirectory, paramCount, varCounter
  # get var id
  varID = p[-1]
  # search for current function
  if functionDirectory[current_scope]['varTable'].has_key(varID):
    # print error message
    print("Parameter already exists '%s'" % varID)
    exit(1)
  else:
    # add variable to varTable
    functionDirectory[current_scope]['varTable'][varID] = {'type': getTypeCode(current_type), 'address': localVarCount[current_type], 'dimension': []} 
    # add data type to signature
    functionDirectory[current_scope]['signature'].append(getTypeCode(current_type))
    #increase global variable counter
    localVarCount[current_type] += 1
    # increase parameter counter
    paramCount += 1
    # increase local variable counter
    varCounter += 1




  # New variable is being created. 
# Add new variable to current varTable. If found declare error.
def p_SA_CREATE_VAR(p):
  '''SA_CREATE_VAR : empty'''
  # global variables
  global varCounter, localVarCount, globalVarCount
  # var id
  varID = p[-1]
  # validate if current variable does already exists in current varTable and global varTable
  if functionDirectory[current_scope]['varTable'].has_key(varID) or functionDirectory['global']['varTable'].has_key(varID):
    # print error message
    print("ID already exists '%s'" % varID)
    exit(1)
  else:
    # dataframe
    if current_type == 'dataframe':
      # create variable PENDING
      functionDirectory[current_scope]['varTable'][varID] = {'type': getTypeCode(current_type), 'address': 0, 'tags': {}, 'file': None, 'headers': {'name': '', 'col': 0}, 'data': [[]]}
    # other variable type
    else:
      # create variable
      functionDirectory[current_scope]['varTable'][varID] = {'type': getTypeCode(current_type), 'address': 0, 'dimension': []}

    # define apropiate address to var
    if current_scope == 'global':
      # assign address
      functionDirectory[current_scope]['varTable'][varID]['address'] = globalVarCount[current_type]
      #increase global variable counter
      globalVarCount[current_type] += 1
    else:
      # assign address
      functionDirectory[current_scope]['varTable'][varID]['address'] = localVarCount[current_type]
      #increase global variable counter
      localVarCount[current_type] += 1
    # increase local variable counter
    varCounter += 1



# Table header ID is declared. PENDING
# Verify header id is in current dataframe. If not found declare error.
def p_SA_DF_FIND_HEADER_ID(p):
  '''SA_DF_FIND_HEADER_ID : empty'''
  # dataframe id
  varID = p[-4]
  # header id
  headerID = p[-1]
  # search for dataframe id and header id in current varTable and in global varTable
  if not (functionDirectory[current_scope]['varTable'][varID]['headers'].has_key(headerID) or functionDirectory['global']['varTable'][varID]['headers'].has_key(headerID)):
    # print error message
    print("ID does not exist '%s'" % p[-1])
    exit(1)


# Function ended. 
# Clear function varTable
def p_SA_END_FUNCTION(p):
  '''SA_END_FUNCTION : empty'''
  # global variables
  global functionDirectory, cont
  # clear function varTable
  functionDirectory[current_scope]['varTable'].clear()
  # create endproc quadruple
  newQuadruple(quadruples, 'EndProc', None, None, None)
  # update quadruple counter
  cont += 1



# Program ended. 
# Clear function dictionary
def p_SA_END_PROGRAM(p):
  '''SA_END_PROGRAM : empty'''
  # global variables
  global functionDirectory

  # create end quadruple
  newQuadruple(quadruples, 'end', None, None, None)
  
  c = 0
  for q in quadruples:
    print c, '  op: ', q['operator'], ' oper1: ', q['operand1'], ' oper2: ', q['operand2'], ' result: ', q['result']
    c += 1

  print functionDirectory

  # clear function dictionary
  functionDirectory.clear() 



# New function is declared.
# Add new function to function directory with id, type add varTable. If not found declare error.
def p_SA_FINAL_FUNC_VALUES(p):
  '''SA_FINAL_FUNC_VALUES : empty'''
  # global variables
  global functionDirectory, varCounter
  # define parameter count for function
  functionDirectory[current_scope]['parameterCount'] = paramCount
  # define local variable count for function and reset counter
  functionDirectory[current_scope]['localVariableCount'] = varCounter
  varCounter = 0
  # define current quadruple for function
  functionDirectory[current_scope]['quadCounter'] = cont



# ID is declared.
# Verify ids is in var table. If not found declare error.
def p_SA_FIND_ID(p):
  '''SA_FIND_ID : empty'''
  # get id
  varID = p[-1]
  # search for id in current varTable and in global varTable
  if not (functionDirectory[current_scope]['varTable'].has_key(varID) or functionDirectory['global']['varTable'].has_key(varID)):
    # print error message
    print("ID does not exist '%s'" % varID)
    exit(1)



# A function is being called.
# Verify ids is in function directory. If not found declare error.
def p_SA_FIND_FUNC_ID(p):
  '''SA_FIND_FUNC_ID : empty'''
  # get function id
  funcID = p[-1]
  # search for function id in function directory
  if not funcID in functionDirectory.keys() :
    # print error message
    print("Function ID does not exist '%s'" % funcID)
    exit(1)



# Main function is declared.
# Add main function to function directory
def p_SA_MAIN_START(p):
  '''SA_MAIN_START : empty'''
  # global variables
  global current_type, current_scope, quadruples
  # define current_type and current_scope
  current_type = 'void'
  current_scope = 'main'
  # get jump
  jump = stackPop(jumps)
  # fill blank space
  quadruples[jump]['result'] = cont
  # create main function in function directory
  functionDirectory[current_scope] = {'type': current_type, 'signature': [], 'parameterCount': 0, 'localVariableCount': 0, 'quadCounter': 0, 'varTable': {}}



# New dataframe is being created.
# Define current type as dataframe
def p_SA_NEW_DF(p):
  '''SA_NEW_DF : empty'''
  # global variables
  global current_type
  # define current_type
  current_type = 'dataframe'



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
    print("Function ID already exists '%s'" % current_scope)
    exit(1)
  else:
    # create new function in function directory
    functionDirectory[current_scope] = {'type': current_type, 'signature': [], 'parameterCount': 0, 'localVariableCount': 0, 'quadCounter': 0, 'varTable': {}}



# Sign defined for variable. 
# Define current_sign
def p_SA_NEW_SIGN(p):
  '''SA_NEW_SIGN : empty'''
  # global variables
  global current_sign
  # define current_sign
  current_sign = p[-1]



# A new porgram is created.
# Create function directory
def p_SA_PROGRAM_START(p):
  '''SA_PROGRAM_START : empty'''
  # global variables
  global functionDirectory, current_type, current_scope, cont
  # define current_type and current_scope
  current_type = 'void'
  current_scope = 'global'
  # create global function in function directory
  functionDirectory[current_scope] = {'type': current_type, 'signature': [], 'parameterCount': 0, 'localVariableCount': 0, 'quadCounter': 0, 'varTable': {}}
  # create first quadruple (jump to main)
  newQuadruple(quadruples, 'GoTo', None, None, -1)
  # update quadruple counter
  cont += 1
  # push cont to jumps
  stackPush(jumps, cont-1)



# Type is declared. 
# Define current_type
def p_SA_TYPE(p):
  '''SA_TYPE : empty'''
  # global variables
  global current_type
  # define current_type
  current_type = p[-1]



# Void function found. 
# Define current_type to void
def p_SA_VOID_FUNCTION(p):
  '''SA_VOID_FUNCTION : empty'''
  # global variables
  global current_type
  # define current_type
  current_type = 'void'



# --------- EXTRA GRAMMARS / EXP QUADRUPPLES ---------

# id was declared
# operands.Push(id.name) and operators.Push(id.type)
def p_SA_EXP_1_ID(p):
  '''SA_EXP_1_ID : empty'''
  # get id
  varID = p[-2]
  # push id name to operands
  stackPush(operands, varID)
  # check if id is in current_scope or global
  if functionDirectory[current_scope]['varTable'].has_key(varID):
    t = functionDirectory[current_scope]['varTable'][varID]['type']
  else:
    t = functionDirectory['global']['varTable'][varID]['type']
  # push
  stackPush(types, t)


# constant was declared
# operands.Push(constant) and types.Push(id.type)
def p_SA_EXP_1_CTE(p):
  '''SA_EXP_1_CTE : empty'''
  # get id
  varID = p[-2]
  # push id name to operands
  stackPush(operands, varID)
  if constantTable.has_key(str(varID)):
    t = constantTable[str(varID)]['type']
  elif constantTable.has_key('-' + str(varID)):
    t = constantTable[str('-' + varID)]['type']
  # push
  stackPush(types, t)



# * or / was declared
# SA EXP 2 - 5
# operators.Push(* or /)
def p_SA_EXP_ADD_OP(p):
  '''SA_EXP_ADD_OP : empty'''
  # get op
  op = p[-1]
  # push * or /
  stackPush(operators, op)


# Verify && or || are at top of stack
# generate corresponding quadruple
def p_SA_EXP_6(p):
  '''SA_EXP_6 : empty'''
  # global variables
  global cont
  # top stack
  op = stackTop(operators)
  # if && or || are at top of stack
  temp_op = ['&&', '||']
  if op in temp_op:
    # get righ and left operands 
    rightOp = stackPop(operands)
    leftOp = stackPop(operands)
    # get right and left operand types
    rightType = stackPop(types)
    leftType = stackPop(types)
    # get operator
    operator = stackPop(operators)
    # validate if operation is valid
    resultType = getResultType(leftType, rightType, operator)
    #valid operation
    if resultType > 0:
      # create quadruple
      newQuadruple(quadruples, operator, leftOp, rightOp, tempVarCount[getTypeString(resultType)])
      # update quadruple counter
      cont += 1
      # push result to operand stack
      stackPush(operands, tempVarCount[getTypeString(resultType)])
      # push type result to type stack
      stackPush(types, resultType)
      # update tempVar count
      tempVarCount[getTypeString(resultType)] += 1
    else:
      # print error message
      print("Result type mismatch")
      exit(1)

# Verify [<, >, <=, >=, ==, !=] are at top of stack
# generate corresponding quadruple
def p_SA_EXP_7(p):
  '''SA_EXP_7 : empty'''
  # global variables
  global cont
  # top stack
  op = stackTop(operators)
  # if [<, >, <=, >=, ==, !=] are at top of stack
  temp_op = ['<', '>', '<=', '>=', '==', '!=']
  if op in temp_op:
    # get righ and left operands 
    rightOp = stackPop(operands)
    leftOp = stackPop(operands)
    # get right and left operand types
    rightType = stackPop(types)
    leftType = stackPop(types)
    # get operator
    operator = stackPop(operators)
    # validate if operation is valid
    resultType = getResultType(leftType, rightType, operator)    
    #valid operation
    if resultType > 0:
      # create quadruple
      newQuadruple(quadruples, operator, leftOp, rightOp, tempVarCount[getTypeString(resultType)])
      # update quadruple counter
      cont += 1
      # push result to operand stack
      stackPush(operands, tempVarCount[getTypeString(resultType)])
      # push type result to type stack
      stackPush(types, resultType)
      # update tempVar count
      tempVarCount[getTypeString(resultType)] += 1
    else:
      # print error message
      print("Result type mismatch")
      exit(1)

# Verify + or -  are at top of stack
# generate corresponding quadruple
def p_SA_EXP_8(p):
  '''SA_EXP_8 : empty'''
  # global variables
  global cont
  # top stack
  op = stackTop(operators)
  # if + or -  are at top of stack
  temp_op = ['+', '-']
  if op in temp_op:
    # get righ and left operands 
    rightOp = stackPop(operands)
    leftOp = stackPop(operands)
    # get right and left operand types
    rightType = stackPop(types)
    leftType = stackPop(types)
    # get operator
    operator = stackPop(operators)
    # validate if operation is valid
    resultType = getResultType(leftType, rightType, operator)
    #valid operation
    if resultType > 0:
      # create quadruple
      newQuadruple(quadruples, operator, leftOp, rightOp, tempVarCount[getTypeString(resultType)])
      # update quadruple counter
      cont += 1
      # push result to operand stack
      stackPush(operands, tempVarCount[getTypeString(resultType)])
      # push type result to type stack
      stackPush(types, resultType)
      # update tempVar count
      tempVarCount[getTypeString(resultType)] += 1
    else:
      # print error message
      print("Result type mismatch")
      exit(1)

# Verify * or / are at top of stack
# generate corresponding quadruple
def p_SA_EXP_9(p):
  '''SA_EXP_9 : empty'''
  # global variables
  global cont
  # top stack
  op = stackTop(operators)
  # if * or / are at top of stack
  temp_op = ['*', '/']
  if op in temp_op:
    # get righ and left operands 
    rightOp = stackPop(operands)
    leftOp = stackPop(operands)
    # get right and left operand types
    rightType = stackPop(types)
    leftType = stackPop(types)
    # get operator
    operator = stackPop(operators)
    # validate if operation is valid
    resultType = getResultType(leftType, rightType, operator)
    #valid operation
    if resultType > 0:
      # create quadruple
      newQuadruple(quadruples, operator, leftOp, rightOp, tempVarCount[getTypeString(resultType)])
      # update quadruple counter
      cont += 1
      # push result to operand stack
      stackPush(operands, tempVarCount[getTypeString(resultType)])
      # push type result to type stack
      stackPush(types, resultType)
      # update tempVar count
      tempVarCount[getTypeString(resultType)] += 1
    else:
      # print error message
      print("Result type mismatch")
      exit(1)


# Verify = are at top of stack
# generate corresponding quadruple
def p_SA_EXP_10(p):
  '''SA_EXP_10 : empty'''
  # global variables
  global cont
  # top stack
  op = stackTop(operators)
  # if * or / are at top of stack
  temp_op = ['=']
  if op in temp_op:
    # get righ and left operands 
    rightOp = stackPop(operands)
    leftOp = stackPop(operands)
    # get right and left operand types
    rightType = stackPop(types)
    leftType = stackPop(types)
    # get operator
    operator = stackPop(operators)
    # validate if operation is valid
    resultType = getResultType(leftType, rightType, operator)
    #valid operation
    if resultType > 0:
      # create quadruple
      newQuadruple(quadruples, operator, rightOp, None, leftOp)
      # update quadruple counter
      cont += 1
    else:
      # print error message
      print("Result type mismatch")
      exit(1)


# Parenthesis found in expression
# Add fake bottom to stack
def p_SA_FAKE_BOTTOM(p):
  '''SA_FAKE_BOTTOM : empty'''
  # add fake bottom to operators
  stackPush(operators, '(')


# Ending parenthesis found in expression
# Remove fake bottom to stack
def p_SA_FAKE_BOTTOM_REMOVE(p):
  '''SA_FAKE_BOTTOM_REMOVE : empty'''
  # add fake bottom to operators
  stackPop(operators)



# --------- EXTRA GRAMMARS / CONDITIONAL QUADRUPPLES ---------



# Ending parenthesis after conditional expression
# Validate condition and generate quadruples
def p_SA_COND_1(p):
  '''SA_COND_1 : empty'''
  # global variables
  global cont
  # get type top
  t = stackPop(types)
  # validate previous expression is bool
  if t != getTypeCode('bool'):
    # print error message
    print("Type mismatch")
    exit(1)
  else:
    # get current operand
    result = stackPop(operands)
    # create quadruple
    newQuadruple(quadruples, 'GoToF', result, None, -1)
    # update quadruple counter
    cont += 1
    # push quadruple counter to jumps
    stackPush(jumps, cont-1)


# Ending of Block in conditional expression
# End block, fill blank jump
def p_SA_COND_2(p):
  '''SA_COND_2 : empty'''
  # get top jump
  end = stackPop(jumps)
  # fill blank space
  quadruples[end]['result'] = cont

# Else statement
# generate final quadruple for if statement
def p_SA_COND_3(p):
  '''SA_COND_3 : empty'''
  # global variables
  global cont
  # Cretae quadruple
  newQuadruple(quadruples, 'GoTo', None, None, -1)
  # update quadruple counter
  cont += 1
  # get top jump
  jump = stackPop(jumps)
  # push cont to jumps
  stackPush(jumps, cont-1)
  # fill blank space
  quadruples[jump]['result'] = cont


# Else statement
# generate final quadruple for if statement
def p_SA_COND_4(p):
  '''SA_COND_4 : empty'''
  # global variables
  global cont
  # Cretae quadruple
  newQuadruple(quadruples, 'GoTo', None, None, -1)
  # update quadruple counter
  cont += 1
  # push cont to jumps
  stackPush(elseif_jumps, cont-1)


# Else statement
# generate final quadruple for if statement
def p_SA_COND_5(p):
  '''SA_COND_5 : empty'''
  while len(elseif_jumps) > 0:
    # get top jump
    jump = stackPop(elseif_jumps)
    # fill blank space
    quadruples[jump]['result'] = cont


# --------- EXTRA GRAMMARS / LOOP QUADRUPPLES ---------


# Begining of loop statement
# push to jumps
def p_SA_LOOP_1(p):
  '''SA_LOOP_1 : empty'''
  # push to jumps
  stackPush(jumps, cont)


# Loop expression ended
# Validate expression and create quadruple
def p_SA_LOOP_2(p):
  '''SA_LOOP_2 : empty'''
  # global variables
  global cont
  # get type
  t = stackPop(types)
  # validate previous expression is bool
  if t != getTypeCode('bool'):
    # print error message
    print("Type mismatch")
    exit(1)
  else:
    # get current operand
    result = stackPop(operands)
    # create quadruple
    newQuadruple(quadruples, 'GoToF', result, None, 0)
    # update quadruple counter
    cont += 1
    # push quadruple counter to jumps
    stackPush(jumps, cont-1)


# End of loop block
# generate final quadruple for loop
def p_SA_LOOP_3(p):
  '''SA_LOOP_3 : empty'''
  # global variables
  global cont
  # get jump
  end = stackPop(jumps)
  # get jump
  r = stackPop(jumps)
  # Create quadruple
  newQuadruple(quadruples, 'GoTo', None, None, r)
  # update quadruple counter
  cont += 1
  # fill blank space
  quadruples[end]['result'] = cont



# --------- EXTRA GRAMMARS / FUNCTION QUADRUPPLES ---------



# Parameter declaration is going to start
# generate necesary quadruples and variables
def p_SA_CALLFUNC_2(p):
  '''SA_CALLFUNC_2 : empty'''
  # global variables
  global cont, parameterCount, pointers, callFunc_scopes
  # function id
  funcID = p[-3]
  # update current func call id
  stackPush(callFunc_scopes, funcID)
  # Create ERA quadruple
  newQuadruple(quadruples, 'era', funcID, None, None)
  # update quadruple counter
  cont += 1
  # reset parameter count
  parameterCount = 1
  # push to pointer stack
  stackPush(pointers, 0)


# Parameter declared
# validate parameter
def p_SA_CALLFUNC_3(p):
  '''SA_CALLFUNC_3 : empty'''
  # global variables
  global cont
  # get operand
  argument = stackPop(operands)
  # get type
  argumentType = stackPop(types)
  # get pointer
  pointer = stackTop(pointers)
  # get call func scope
  callFunc_scope = stackTop(callFunc_scopes)
  # verify type with current parameter in pointer
  if argumentType == functionDirectory[callFunc_scope]['signature'][pointer]:
    # Create action quadruple
    newQuadruple(quadruples, 'param', argument, None, pointer)
    # update quadruple counter
    cont += 1
  else:
    # print error message
    print("Result type mismatch")
    exit(1)


# Another parameter will be declared
# update pointer
def p_SA_CALLFUNC_4(p):
  '''SA_CALLFUNC_4 : empty'''
  # global variables
  global pointers
  # get  pointer
  pointer = stackPop(pointers)
  # update pointer
  pointer += 1
  # push pointer
  stackPush(pointers, pointer)

# Parameters finished
# Verify total parameter count
def p_SA_CALLFUNC_5(p):
  '''SA_CALLFUNC_5 : empty'''
  # get call func scope
  callFunc_scope = stackTop(callFunc_scopes)
  # verify if function does not have any parameters
  if functionDirectory[callFunc_scope]['signature']:
    pointer = stackTop(pointers)
    # verify parameter count
    if pointer+1 != len(functionDirectory[callFunc_scope]['signature']):
      # print error message
      print("Wrong parameter count")
      exit(1)


# Function call finished
# Generate necesary quadruple
def p_SA_CALLFUNC_6(p):
  '''SA_CALLFUNC_6 : empty'''
  # global variables
  global cont, pointers
  # pop pointers
  stackPop(pointers)
  # get function id
  funcID = p[-8]
  # In case the function is in an expression
  # -7 because it does not have a ;
  if funcID is None:
    funcID = p[-7]
  # Create gosub quadruple
  newQuadruple(quadruples, 'GoSub', funcID, None, None)
  # update quadruple counter
  cont += 1

# Function check if there is return value
# Generate necesary quadruple
def p_SA_CALLFUNC_7(p):
  '''SA_CALLFUNC_7 : empty'''
  # Global Variables
  global cont, callFunc_scopes
  # Get function id
  funcID = p[-8]
  # get call func scope
  callFunc_scope = stackTop(callFunc_scopes)
  # Get function type
  funcType = functionDirectory[callFunc_scope]['type']
  # pop callFunc_scopes
  stackPop(callFunc_scopes)
  # Verify that function has a return type
  if datatypeCode[funcType] > 0:
  # Generate assignment quadruple to function value
    newQuadruple(quadruples, '=', funcID, None, tempVarCount[funcType])
  # Push temporary value to operands
    stackPush(operands, tempVarCount[funcType])
  # Push temporary value to types
    stackPush(types, datatypeCode[funcType])
  # Update tempVar count
    tempVarCount[funcType] += 1

# Return value
# Generate necesary quadruple
def p_SA_RET(p):
  '''SA_RET : empty'''
  # Global variables
  global cont
  # Temporary variables for type validation
  returnType = stackPop(types)
  functionRetType = datatypeCode[functionDirectory[current_scope]['type']]
  # Value to return, result of expression
  returnValue = stackPop(operands)
  # Validate type of expression with return type of function
  if functionRetType == returnType:
  # Create return quadruple
    newQuadruple(quadruples, 'Return', None, None, returnValue)
  # Update quadruple counter
    cont += 1
  else:
    print("Return type mismatch")
    exit(1)


# --------- EXTRA GRAMMARS / ARRAY QUADRUPPLES ---------


# Array declared
# Generate first dimension level
def p_SA_ARR_1(p):
  '''SA_ARR_1 : empty'''
  # Global Variables
  global cont, array_id
  # get var id
  varID = p[-4]
  # set current array id
  array_id = varID
  # get size of array
  size =  p[-1]
  # agregar dimension a variable
  functionDirectory[current_scope]['varTable'][varID]['dimension'].append({'dim': 1, 'inf': 0, 'sup': size, 'K': 0})
  # crear espacio para arreglo en memoria
  # define apropiate address to var
  if current_scope == 'global':
    #increase global variable counter
    globalVarCount[current_type] += size-1
  else:
    #increase global variable counter
    localVarCount[current_type] += size-1


# Array access declared
# Verify dimension var
def p_SA_ARR_2(p):
  '''SA_ARR_2 : empty'''
  # Global Variables
  global cont, current_dim
  # Get var id
  varID = p[-3]
  # Verify id is dimensioned
  if len(functionDirectory[current_scope]['varTable'][varID]['dimension']) > 0:
    # define current dimension
    current_dim = 1
    # push var to dimensions stack
    stackPush(dimensions, {'varID': varID, 'dim': current_dim})
  else:
    print("Inocrrect variable type. Dimensioned variable required.")
    exit(1)


# Array exp evaluated
# Create array quadruples
def p_SA_ARR_3(p):
  '''SA_ARR_3 : empty'''
  # Global Variables
  global cont
  # Get var id
  varID = p[-6]
  # get oprand
  op = stackTop(operands)
  # get inferior limit
  inf = functionDirectory[current_scope]['varTable'][varID]['dimension'][current_dim-1]['inf']
  # get superior limit
  sup = functionDirectory[current_scope]['varTable'][varID]['dimension'][current_dim-1]['sup']
  # create quadruple
  newQuadruple(quadruples, 'Ver', op, inf, sup)
  # update quadruple counter
  cont += 1
  # get operand
  aux = stackPop(operands)
  # validate if operation is valid
  t = getTypeCode('int')
  # get base direction
  dir = functionDirectory[current_scope]['varTable'][varID]['address']
  # verify dir is in constTable
  if not constantTable.has_key(str(dir)):
    #create constant
    constantTable[str(dir)] = {'type': t, 'address': constVarCount[getTypeString(t)], 'val': dir}
    #increase constant variable counter
    constVarCount[getTypeString(t)] += 1
  #cretae special dir
  specialDir = '(' + str(tempVarCount[getTypeString(t)]) + ')'
  # create quadruple
  newQuadruple(quadruples, '+', aux, constantTable[str(dir)]['address'], specialDir)
  # update quadruple counter
  cont += 1
  # push result to operand stack
  stackPush(operands, specialDir)
  # push type result to type stack
  stackPush(types, t)
  # update tempVar count
  tempVarCount[getTypeString(t)] += 1


# Array assignment started a = [ ]
# Prepare assignment
def p_SA_ARR_4(p):
  '''SA_ARR_4 : empty'''
  # Global Variables
  global array_counter
  # reset array size
  array_counter = 0


# Array values are being assigned
# Create array assignment quadruples
def p_SA_ARR_5(p):
  '''SA_ARR_5 : empty'''
  # Global Variables
  global array_counter, cont
  # get base direction
  dir = functionDirectory[current_scope]['varTable'][array_id]['address']
  # get array count
  array_size = functionDirectory[current_scope]['varTable'][array_id]['dimension'][current_dim-1]['sup'] - 1
  # validate limit of array size i not exceeded
  if array_counter < array_size:
    # get operand
    op = stackPop(operands) 
    # create quadruple
    newQuadruple(quadruples, '=', op, None, dir+array_counter)
    # update quadruple counter
    cont += 1
    # update array counter
    array_counter += 1



  


# --------- EXTRA GRAMMARS / PRINT QUADRUPPLES ---------
# Print declared
# Create print quadruple
def p_SA_PRINT_DATA(p):
  '''SA_PRINT_DATA : empty'''
  # get id
  varID = p[-2]
  # create quadruple
  newQuadruple(quadruples, 'print', None, None, varID)
  # update quadruple counter
  cont += 1

# Build the parser
yacc.yacc()

# -------------------------- FILE IMPORTS --------------------------
from Cube import *
from Functions import *
from VirtualMachine import *
# from Memory import *?

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
      # Execute virtual machine
      execute(quadruples, globalVarCount, localVarCount, tempVarCount, constVarCount)
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