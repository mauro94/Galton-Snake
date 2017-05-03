# Galton Snake
# Mauro Amarante A01191903
# Patricio Sanchez A01191893

import sys
import time
from collections import deque
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

# -----------------------------------------------------
# ------------------ FILE IMPORTS ---------------------
# -----------------------------------------------------

from Cube import *
from Functions import *
from VirtualMachine import *
# from Memory import *?

# -----------------------------------------------------
# --------------------- LEX ---------------------------
# -----------------------------------------------------

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
   'printDf' : 'printDf',
   'printData' : 'printData',
   'main' : 'main',
   'int' : 'int',
   'float' : 'float',
   'string' : 'string',
   'bool' : 'bool',
   'true' : 'true',
   'false' : 'false',
   'fill' : 'fill'
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

# String regex
def t_cte_string(t):
    r'\"[^\"]*\"'
    return t

# Float regex
def t_cte_float(t):
    r'[-+]?[0-9]+\.[0-9]+([Ee][\+-]?[0-9+])?'
    t.value = float(t.value)
    return t

# Int regex
def t_cte_int(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

# File regex
def t_file(t):
    r'[A-Za-z0-9\_\-]+.csv'
    t.type = reserved.get(t.value, 'file')
    return t

# Id regex
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

# -----------------------------------------------------
# ----------------------- YACC ------------------------
# -----------------------------------------------------

import ply.yacc as yacc

# -----------------------------------------------------
# ----------------- GLOBAL VARIABLES ------------------
# -----------------------------------------------------

functionDirectory = {}  # {functionName : {functionType, [paramTypeList], #parameters, #localvariables, #quadruplecounter, {varTable}} }
                        # varTable -> {varID : {type, address, dimension}}
constantTable = {}      # {constant : {type, address, value} }
dataframeTable = {}     # {dataframeName : 'address': 0, 'tags': {}, 'file': None, 'headers': {}, 'data': [[]]
current_scope = ''      # Current scope in the program
current_type = ''       # Current type being used
current_sign = ''       # Current sign being used
operands = []           # Operands stack
types = []              # Types stack 
operators = []          # Operators stack
quadruples = []         # Quadruples list
jumps = []              # Jumps stack
elseif_jumps = []       # Elseif jumps stack
dimensions = []         # Dimensions stack
current_dim = 0         # Variable for current dimension
cont = 0                # Quadruple counter  
paramCount = 0          # Parameter counter
varCounter = 0          # Local variable counter
callFunc_scopes = []    # Stack of id of function call
pointers = []           # Pointer stack
array_counter = 0       # Value counter array
dim_counter = 0         # Dimension counter for array access
array_location = 0      # Array location during assignment
array_size = 0          # Array size
array_id = ''           # Current array id
array_access_R = 0      # R used for calculations in array access
current_df = ''         # Current dataframe id
funcWithReturn = False  # Defines if current function has a return op
df_print_row = 0        # Define row to print
df_print_col = 0        # Define col to print


# -----------------------------------------------------
# ----------------- MEMORY COUNTERS -------------------
# -----------------------------------------------------

# 2,000 slots per block, dataframes 10,000 
globalVarCount = {}
globalVarCount['bool'] = getInitDir('global', 'bool')
globalVarCount['int'] = getInitDir('global', 'int')
globalVarCount['float'] = getInitDir('global', 'float')
globalVarCount['string'] = getInitDir('global', 'string')

localVarCount = {}

tempVarCount = {}

constVarCount = {}
constVarCount['bool'] = getInitDir('constant', 'bool')
constVarCount['int'] = getInitDir('constant', 'int')
constVarCount['float'] = getInitDir('constant', 'float')
constVarCount['string'] = getInitDir('constant', 'string')


# -----------------------------------------------------
# --------------------- GRAMMARS ----------------------
# -----------------------------------------------------

# Starting grammar
start = 'PROGRAM'

def p_ACCESS_COL(p):
    '''ACCESS_COL : id SA_FIND_DF period col lPar EXP rPar SA_DF_ACCESS_1'''

def p_ACCESS_ROW(p):
    '''ACCESS_ROW : id SA_FIND_DF period row lPar EXP rPar SA_DF_ACCESS_1'''

def p_ASSIGNMENT(p):
    '''ASSIGNMENT : fill id SA_ARR_20 ASSIGNMENT_ARR_COUNT SA_ARR_19 SA_ARR_22 equal SA_EXP_ADD_OP lSqBr ASSIGNMENT_ARR_DIM rSqBr semi_colon
                  | id SA_FIND_ID SA_EXP_1_ID equal SA_EXP_ADD_OP SUPER_EXPRESSION SA_EXP_10 semi_colon
                  | VAR_ARR equal SA_EXP_ADD_OP SUPER_EXPRESSION SA_EXP_10 semi_colon
                  | VAR_ARR equal SA_EXP_ADD_OP CALLFUNC SA_EXP_10 '''

def p_ASSIGNMENT_ARR_COUNT(p):
    '''ASSIGNMENT_ARR_COUNT : lSqBr rSqBr SA_ARR_21 ASSIGNMENT_ARR_COUNT
                            | lSqBr rSqBr SA_ARR_21'''

def p_ASSIGNMENT_ARR_DIM(p):
    '''ASSIGNMENT_ARR_DIM : ASSIGNMENT_ARR_EXP
                          | lSqBr SA_ARR_24 ASSIGNMENT_ARR_EXP SA_ARR_25 rSqBr coma ASSIGNMENT_ARR_DIM
                          | lSqBr SA_ARR_24 ASSIGNMENT_ARR_EXP SA_ARR_25 rSqBr'''

def p_ASSIGNMENT_ARR_EXP(p):
    '''ASSIGNMENT_ARR_EXP : EXP SA_ARR_23 coma ASSIGNMENT_ARR_EXP
                          | EXP SA_ARR_23'''

def p_BIND_COLS(p):
    '''BIND_COLS : cbind lPar id SA_FIND_DF SA_DF_BINDINGS_1 coma ACCESS_COL rPar semi_colon
                 | cbind lPar id SA_FIND_DF SA_DF_BINDINGS_1 coma TABLE_HEADER rPar semi_colon '''

def p_BIND_ROWS(p):
    '''BIND_ROWS : rbind lPar id SA_FIND_DF SA_DF_BINDINGS_1 coma ACCESS_ROW rPar semi_colon '''

def p_BINDINGS(p):
    '''BINDINGS : BIND_ROWS 
                | BIND_COLS'''

def p_BLOCK(p):
    '''BLOCK : BLOCK_STM 
             | BLOCK_STM return SUPER_EXPRESSION SA_RET semi_colon '''

def p_BLOCK_STM(p):
    '''BLOCK_STM : STATEMENT BLOCK_STM 
                 | empty'''

def p_CALLFUNC(p):
    '''CALLFUNC : call id SA_FIND_FUNC_ID lPar SA_CALLFUNC_2 CALLFUNC_PARAMS rPar SA_CALLFUNC_5 semi_colon SA_CALLFUNC_6'''

def p_CALLFUNC_EXP(p):
    '''CALLFUNC_EXP : id SA_FIND_FUNC_ID lPar SA_CALLFUNC_2 CALLFUNC_PARAMS rPar SA_CALLFUNC_5 SA_CALLFUNC_6 SA_CALLFUNC_7'''

def p_CALLFUNC_PARAMS(p):
    '''CALLFUNC_PARAMS : SA_FAKE_BOTTOM EXP SA_FAKE_BOTTOM_REMOVE SA_CALLFUNC_3 coma SA_CALLFUNC_4 CALLFUNC_PARAMS
                       | SA_FAKE_BOTTOM EXP SA_FAKE_BOTTOM_REMOVE SA_CALLFUNC_3
                       | empty'''

def p_CONDITION(p):
    '''CONDITION : if lPar SUPER_EXPRESSION rPar SA_COND_1 lBr BLOCK rBr SA_COND_2
                 | if lPar SUPER_EXPRESSION rPar SA_COND_1 lBr BLOCK rBr elseif SA_COND_4 SA_COND_2 CONDITION_ELIF else SA_COND_3 lBr BLOCK rBr SA_COND_2 SA_COND_5
                 | if lPar SUPER_EXPRESSION rPar SA_COND_1 lBr BLOCK rBr else SA_COND_3 lBr BLOCK rBr SA_COND_2'''

def p_CONDITION_ELIF(p):
    '''CONDITION_ELIF : lPar SUPER_EXPRESSION rPar SA_COND_1 lBr BLOCK rBr elseif SA_COND_4 SA_COND_2 CONDITION_ELIF
                      | lPar SUPER_EXPRESSION rPar SA_COND_1 lBr BLOCK rBr'''

def p_CORR_HEADERS(p):
    '''CORR_HEADERS : correlateHeaders lPar id SA_FIND_DF coma id SA_FIND_DF coma cte_float SA_DF_CORR_HEADERS_1 rPar semi_colon '''

def p_CORR(p):
    '''CORR : correlate lPar id SA_FIND_DF coma id SA_FIND_DF coma cte_float SA_DF_CORR rPar semi_colon '''

def p_CORRELATION(p):
    '''CORRELATION : CORR_HEADERS 
                   | CORR'''

def p_CREATE_DF(p):
    '''CREATE_DF : dataframe lPar id SA_NEW_DF coma lSqBr CREATE_DF_TAGS rSqBr coma file SA_DF_ADD_FILE rPar semi_colon 
                 | dataframe lPar id SA_NEW_DF coma file SA_DF_ADD_FILE rPar semi_colon '''

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
    '''FACTOR : lPar SA_FAKE_BOTTOM SUPER_EXPRESSION SA_FAKE_BOTTOM_REMOVE rPar 
              | plus SA_NEW_SIGN VAR_CTE 
              | minus SA_NEW_SIGN VAR_CTE 
              | SA_NEW_SIGN VAR_CTE '''

def p_FUNCTION(p):
    '''FUNCTION : func void SA_VOID_FUNCTION id SA_NEW_FUNCTION lPar SA_VAR_COUNTERS PARAMETERS rPar colon lBr INSTANTIATE BLOCK SA_FINAL_FUNC_VALUES rBr SA_END_FUNCTION
                | func TYPE id SA_NEW_FUNCTION lPar SA_VAR_COUNTERS PARAMETERS rPar colon lBr INSTANTIATE BLOCK SA_FINAL_FUNC_VALUES rBr SA_END_FUNCTION'''

def p_INSTANTIATE(p):
    '''INSTANTIATE : CREATE_DF INSTANTIATE
                   | VARS INSTANTIATE
                   | empty'''

def p_LOOP(p):
    '''LOOP : while SA_LOOP_1 lPar SUPER_EXPRESSION rPar SA_LOOP_2 lBr BLOCK rBr SA_LOOP_3'''

def p_OPERATION(p):
    '''OPERATION : BINDINGS 
                 | CORRELATION '''

def p_PARAMETERS(p):
    '''PARAMETERS : TYPE id SA_CREATE_PARAMS coma PARAMETERS 
                  | TYPE id SA_CREATE_PARAMS
                  | empty'''
    

def p_PRINT_CELL(p):
    '''PRINT_CELL : printCell id SA_FIND_DF lSqBr EXP SA_DF_PRINTCELL_1 rSqBr lSqBr EXP SA_DF_PRINTCELL_2 rSqBr SA_DF_PRINTCELL_3 semi_colon '''

def p_PRINT_COL(p):
    '''PRINT_COL : printCol SA_DF_PRINTCOL_1 TABLE_HEADER semi_colon
                 | printCol SA_DF_PRINTCOL_1 ACCESS_COL semi_colon '''

def p_PRINT_DATA(p):
    '''PRINT_DATA : print SUPER_EXPRESSION SA_PRINT_DATA semi_colon '''

def p_PRINT_DF(p):
    '''PRINT_DF : printDf id SA_FIND_DF SA_DF_PRINT semi_colon '''

def p_PRINT_DF_DATA(p):
    '''PRINT_DF_DATA : printData id SA_FIND_DF SA_DF_PRINT_DATA semi_colon '''

def p_PRINT_HEADERS(p):
    '''PRINT_HEADERS : printHeaders id SA_FIND_DF SA_DF_PRINTHEADERS_1 semi_colon '''

def p_PRINT_ROW(p):
    '''PRINT_ROW : printRow SA_DF_PRINTROW_1 ACCESS_ROW semi_colon '''

def p_PRINT_TAGS(p):
    '''PRINT_TAGS : printTags id SA_FIND_DF SA_DF_PRINTTAGS_1 semi_colon '''

def p_PRINT(p):
    '''PRINT : PRINT_COL
             | PRINT_TAGS
             | PRINT_DATA
             | PRINT_HEADERS
             | PRINT_CELL
             | PRINT_ROW
             | PRINT_DF
             | PRINT_DF_DATA'''

def p_PROGRAM(p):
    '''PROGRAM : SA_PROGRAM_START INSTANTIATE PROGRAM_FUNCTIONS main SA_MAIN_START colon lBr SA_VAR_COUNTERS INSTANTIATE BLOCK SA_FINAL_FUNC_VALUES rBr SA_END_PROGRAM'''

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
    '''TABLE_HEADER : id SA_FIND_DF money_sign id SA_DF_HEADER'''

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
    '''VAR_ARR : id SA_FIND_ID SA_ARR_15 SA_FAKE_BOTTOM VARS_ARR_ACC SA_ARR_18 SA_FAKE_BOTTOM_REMOVE'''

def p_VARS_ARR_ACC(p):
    '''VARS_ARR_ACC : lSqBr EXP SA_ARR_16 rSqBr SA_ARR_17 VARS_ARR_ACC
                    | lSqBr EXP SA_ARR_16 rSqBr'''

def p_VARS_ARR_INST(p):
    '''VARS_ARR_INST : lSqBr cte_int SA_ARR_12 rSqBr SA_ARR_13 VARS_ARR_INST
                     | lSqBr cte_int SA_ARR_12 rSqBr'''

def p_VAR_CTE(p):
    '''VAR_CTE : VAR_ARR
               | id SA_FIND_ID SA_EXP_1_ID
               | cte_int SA_CREATE_CONST SA_EXP_1_CTE
               | cte_float SA_CREATE_CONST SA_EXP_1_CTE
               | cte_string SA_CREATE_CONST SA_EXP_1_CTE
               | true SA_CREATE_CONST SA_EXP_1_CTE 
               | false SA_CREATE_CONST SA_EXP_1_CTE 
               | CALLFUNC_EXP'''



def p_VARS(p):
    '''VARS : TYPE VARS_ID semi_colon '''

def p_VARS_ID(p):
    '''VARS_ID : id SA_CREATE_VAR coma VARS_ID
               | id SA_CREATE_VAR 
               | id SA_CREATE_VAR SA_ARR_11 VARS_ARR_INST SA_ARR_14 coma VARS_ID
               | id SA_CREATE_VAR SA_ARR_11 VARS_ARR_INST SA_ARR_14'''

# Empty grammar
def p_empty(p):
    'empty :'
    pass

# Error
def p_error(p):
    print("Syntax error at '%s', '%s'" % (p.value, p))
    exit(1)


# -----------------------------------------------------
# ----------------- SEMANTIC ACTIONS ------------------
# -----------------------------------------------------

# File specified in dataframe. 
# Add file name to current dataframe
def p_SA_DF_ADD_FILE(p):
  '''SA_DF_ADD_FILE : empty'''
  # Global variables
  global functionDirectory, cont
  # Get file name
  file = p[-1]
  # Verify if file string is in constants table
  if not constantTable.has_key(str(file)): 
    # Create constant
    constantTable[str(file)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': file}
    # Increase constant variable counter
    constVarCount['string'] += 1
  # Verify if current scope string is in constants table
  if not constantTable.has_key(str(current_scope)): 
    # Create constant
    constantTable[str(current_scope)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': current_scope}
    # Increase constant variable counter
    constVarCount['string'] += 1
  # New special dataframe
  special_df = '[' + str(current_df) + ']'
  # Create quadruple
  newQuadruple(quadruples, getOpCode('Read'), constantTable[str(special_df)]['address'], constantTable[str(current_scope)]['address'], constantTable[str(file)]['address'])
  # Update quadruple counter
  cont += 1
  # Add file name
  dataframeTable[current_scope][current_df]['file'] = constantTable[str(file)]['address']


# Tag specified in dataframe. 
# Add tag to current dataframe
def p_SA_ADD_DF_TAG(p):
  '''SA_ADD_DF_TAG : empty'''
  # Get tag
  tag = p[-1]
  # Verify if new tag already exists
  if dataframeTable[current_scope][current_df]['tags'].has_key(tag):
    # Print error message
    print("Tag already exists. Tag: '%s'" % tag)
    exit(1)
  else:
    # Verify if file string is in constants table
    if not constantTable.has_key(str(tag)): 
      # Create constant
      constantTable[str(tag)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': tag}
      # Increase constant variable counter
      constVarCount['string'] += 1
    # Add new tag
    dataframeTable[current_scope][current_df]['tags'][tag] = constantTable[str(tag)]['address']


# New constant. 
# Add new constant to constantTable. If not found ignore.
def p_SA_CREATE_CONST(p):
  '''SA_CREATE_CONST : empty'''
  # Global variables
  global constantTable
  # Get constant 
  constant = p[-1]
  # Validate if current constant does already exists and create
  if not constantTable.has_key(str(constant)):
    # Bool
    if constant == 'true' or constant == 'false':
      # Define type code
      t = 1
      # Define constant
      if str(constant) == 'true':
        cte = True
      else:
        cte = False
    # Float
    elif isinstance(constant, float):
      # Define constant
      cte = float(constant)
      # Validate curret sign
      if current_sign == '-':
        cte *= -1
        constant = str(cte)
      # Define type code
      t = 3
    # Integer
    elif isinstance(constant, int):
      # Define constant
      cte = int(constant)
      # Validate curret sign
      if current_sign == '-':
        cte *= -1
        constant = str(cte)
      # Define type code
      t = 2
    # String
    elif isinstance(constant, str):
      # Define constant
      cte = str(constant)
      # Define type code
      t = 4
    # Create constant
    constantTable[str(constant)] = {'type': t, 'address': constVarCount[getTypeString(t)], 'val': cte}
    #increase constant variable counter
    constVarCount[getTypeString(t)] += 1


# Parameters are declared in function.
# Add paramaters types to function in function directory and variables to varTable. If not found declare error.
def p_SA_CREATE_PARAMS(p):
  '''SA_CREATE_PARAMS : empty'''
  # Global variables
  global functionDirectory, paramCount, varCounter
  # Get var id
  varID = p[-1]
  # Search for current param function
  if functionDirectory[current_scope]['varTable'].has_key(varID):
    # Print error message
    print("Parameter already exists. Parameter: '%s'" % varID)
    exit(1)
  else:
    # Add param to varTable
    functionDirectory[current_scope]['varTable'][varID] = {'type': getTypeCode(current_type), 'address': localVarCount[current_scope][current_type], 'dimension': []} 
    # Add data type to signature
    functionDirectory[current_scope]['signature'].append(getTypeCode(current_type))
    # Add param new assigned address to dir func
    functionDirectory[current_scope]['paramAddresses'].append(functionDirectory[current_scope]['varTable'][varID]['address'])
    # Increase global variable counter
    localVarCount[current_scope][current_type] += 1
    # Increase parameter counter
    paramCount += 1
    # Increase local variable counter
    varCounter += 1


# New variable is being created. 
# Add new variable to current varTable. If found declare error.
def p_SA_CREATE_VAR(p):
  '''SA_CREATE_VAR : empty'''
  # Global variables
  global varCounter, localVarCount, globalVarCount, current_df
  # Var id
  varID = p[-1]
  # Validate if current variable does already exists in current varTable and global varTable
  if functionDirectory[current_scope]['varTable'].has_key(varID) or functionDirectory['global']['varTable'].has_key(varID):
    # Print error message
    print("Variable already exists. Variable: '%s'" % varID)
    exit(1)
  else:
    # Create variable
    functionDirectory[current_scope]['varTable'][varID] = {'type': getTypeCode(current_type), 'address': 0, 'dimension': []}

    # Define apropiate address to var
    if current_scope == 'global':
      # Assign address
      functionDirectory[current_scope]['varTable'][varID]['address'] = globalVarCount[current_type]
      # Increase global variable counter
      globalVarCount[current_type] += 1
    else:
      # Assign address
      functionDirectory[current_scope]['varTable'][varID]['address'] = localVarCount[current_scope][current_type]
      # Increase global variable counter
      localVarCount[current_scope][current_type] += 1
    # Increase local variable counter
    varCounter += 1


# Function ended 
# Clear function varTable
def p_SA_END_FUNCTION(p):
  '''SA_END_FUNCTION : empty'''
  # Global variables
  global functionDirectory, cont, funcWithReturn
  # Clear function varTable
  functionDirectory[current_scope]['varTable'].clear()
  # Check if previous quadruple is return
  if not funcWithReturn:
    # Create endproc quadruple
    newQuadruple(quadruples, getOpCode('EndProc'), None, None, None)
    # Update quadruple counter
    cont += 1
    # Update return bool
    funcWithReturn = False



# Program ended 
# Clear function dictionary
def p_SA_END_PROGRAM(p):
  '''SA_END_PROGRAM : empty'''
  # Global variables
  global functionDirectory
  # Create end quadruple
  newQuadruple(quadruples, getOpCode('End'), None, None, None)
  # Clear function dictionary
  functionDirectory.clear() 


# Function ended
# Add final values to function directory
def p_SA_FINAL_FUNC_VALUES(p):
  '''SA_FINAL_FUNC_VALUES : empty'''
  # Global variables
  global functionDirectory, varCounter
  # Define parameter count for function
  functionDirectory[current_scope]['parameterCount'] = paramCount
  # Define local variable count for function and reset counter
  functionDirectory[current_scope]['localVariableCount'] = varCounter
  # Reset var counter
  varCounter = 0


# ID is declared
# Verify ids is in var table. If not found declare error
def p_SA_FIND_ID(p):
  '''SA_FIND_ID : empty'''
  # Get id
  varID = p[-1]
  # Search for id in current varTable and in global varTable
  if not (functionDirectory[current_scope]['varTable'].has_key(varID) or functionDirectory['global']['varTable'].has_key(varID)):
    # Print error message
    print("ID does not exist. ID: '%s'" % varID)
    exit(1)


# Dataframe is declared.
# Verify dfs is in df table. If not found declare error.
def p_SA_FIND_DF(p):
  '''SA_FIND_DF : empty'''
  # Get df id
  dfID = p[-1]
  # Search for df
  if not (dataframeTable[current_scope].has_key(dfID) or dataframeTable['global'].has_key(dfID)):
    # Print error message
    print("Dataframe does not exist. Dataframe: '%s'" % dfID)
    exit(1)


# A function is being called.
# Verify ids is in function directory. If not found declare error.
def p_SA_FIND_FUNC_ID(p):
  '''SA_FIND_FUNC_ID : empty'''
  # Get function id
  funcID = p[-1]
  # Search for function id in function directory
  if not funcID in functionDirectory.keys() :
    # Print error message
    print("Function does not exist. Function: '%s'" % funcID)
    exit(1)


# Main function is declared.
# Add main function to function directory
def p_SA_MAIN_START(p):
  '''SA_MAIN_START : empty'''
  # Global variables
  global current_type, current_scope, quadruples, paramCount
  # Define current_type
  current_type = 'void'
  # Define current_scope
  current_scope = 'main'
  # Reset parameter count
  paramCount = 0
  # Get jump
  jump = stackPop(jumps)
  # Fill blank space
  quadruples[jump]['result'] = cont
  # Create main function in function directory
  functionDirectory[current_scope] = {'type': current_type, 'signature': [], 'parameterCount': 0, 'localVariableCount': 0, 'quadCounter': 0, 'paramAddresses': [], 'varTable': {}}
  # Define current quadruple for function
  functionDirectory[current_scope]['quadCounter'] = cont


# New dataframe is being created
# Create new dataframe
def p_SA_NEW_DF(p):
  '''SA_NEW_DF : empty'''
  # Global variables
  global current_type, current_df
  # Define current_type
  current_type = 'dataframe'
  # Get id
  current_df = p[-1]
  # Validate if current dataframe does already exists in current dataframe table and global dataframe table
  if functionDirectory[current_scope]['varTable'].has_key(current_df) or functionDirectory['global']['varTable'].has_key(current_df) or dataframeTable[current_scope].has_key(current_df):
    # Print error message
    print("Variable already exists. Variable: '%s'" % current_df)
    exit(1)
  # Create dataframe
  dataframeTable[current_scope][current_df] = {'tags': {}, 'file': None, 'headers': {}, 'data': [] }
  # New special dataframe
  special_df = '[' + str(current_df) + ']'
  # Verify if dataframe is in constantstable
  if not constantTable.has_key(str(special_df)): 
    # Create constant
    constantTable[str(special_df)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': current_df}
    # Increase constant variable counter
    constVarCount['string'] += 1


# New function is declared.
# Add new function to function directory with id, type add varTable. If not found declare error.
def p_SA_NEW_FUNCTION(p):
  '''SA_NEW_FUNCTION : empty'''
  # Global variables
  global current_scope, paramCount, cont
  # Define current_scope
  current_scope = p[-1]
  # Restart parameter counter
  paramCount = 0
  # Verify if function id already exists
  if functionDirectory.has_key(current_scope):
    # Print error message
    print("Function already exists. Function: '%s'" % current_scope)
    exit(1)
  else:
    # Create new function in function directory
    functionDirectory[current_scope] = {'type': current_type, 'signature': [], 'parameterCount': 0, 'localVariableCount': 0, 'quadCounter': 0, 'paramAddresses': [], 'varTable': {}}
    # Define current quadruple for function
    functionDirectory[current_scope]['quadCounter'] = cont


# Sign defined for variable
# Define current_sign
def p_SA_NEW_SIGN(p):
  '''SA_NEW_SIGN : empty'''
  # Global variables
  global current_sign
  # Get sign
  sign = p[-1]
  # Verify sign
  if (sign == '-'):
    # Define current_sign
    current_sign = '-'
  else:
    # Define current_sign to None
    current_sign = None


# A new porgram is created
# Create function directory
def p_SA_PROGRAM_START(p):
  '''SA_PROGRAM_START : empty'''
  # Global variables
  global functionDirectory, current_type, current_scope, cont
  # Define current_type
  current_type = 'void'
  # Define current_scope
  current_scope = 'global'
  # Create global function in function directory
  functionDirectory[current_scope] = {'type': current_type, 'signature': [], 'parameterCount': 0, 'localVariableCount': 0, 'quadCounter': 0, 'paramAddresses': [], 'varTable': {}}
  # Create first quadruple (jump to main)
  newQuadruple(quadruples, getOpCode('GoTo'), None, None, -1)
  # Update quadruple counter
  cont += 1
  # Push cont to jumps
  stackPush(jumps, cont-1)
  # Prep dataframes
  dataframeTable['global'] =  {}


# Type is declared 
# Define current_type
def p_SA_TYPE(p):
  '''SA_TYPE : empty'''
  # Global variables
  global current_type
  # Define current_type
  current_type = p[-1]


# New function starting
# Define local var counters for function
def p_SA_VAR_COUNTERS(p):
  '''SA_VAR_COUNTERS : empty'''
  # Get current function id
  funcID = current_scope
  # Create function in var counter
  localVarCount[funcID] =  {}
  # Define type counters
  localVarCount[funcID]['bool'] = getInitDir('local', 'bool')
  localVarCount[funcID]['int'] = getInitDir('local', 'int')
  localVarCount[funcID]['float'] = getInitDir('local', 'float')
  localVarCount[funcID]['string'] = getInitDir('local', 'string')
  # Create function in var counter
  tempVarCount[funcID] =  {}
  # Define type counters
  tempVarCount[funcID]['bool'] = getInitDir('temp', 'bool')
  tempVarCount[funcID]['int'] = getInitDir('temp', 'int')
  tempVarCount[funcID]['float'] = getInitDir('temp', 'float')
  tempVarCount[funcID]['string'] = getInitDir('temp', 'string')
  # Dataframe new function
  dataframeTable[funcID] =  {}


# Void function found. 
# Define current_type to void
def p_SA_VOID_FUNCTION(p):
  '''SA_VOID_FUNCTION : empty'''
  # Global variables
  global current_type
  # Define current_type
  current_type = 'void'


# -----------------------------------------------------
# ----------------- SEMANTIC ACTIONS ------------------
# -------------------- EXPRESSIONS --------------------
# -----------------------------------------------------

# Id was declared
# Push id and type to stacks
def p_SA_EXP_1_ID(p):
  '''SA_EXP_1_ID : empty'''
  # Get id
  varID = p[-2]
  # Check if id is in current_scope or global
  if functionDirectory[current_scope]['varTable'].has_key(varID):
    # Get type
    t = functionDirectory[current_scope]['varTable'][varID]['type']
    # Get address
    d = functionDirectory[current_scope]['varTable'][varID]['address']
  else:
    # Get type
    t = functionDirectory['global']['varTable'][varID]['type']
    # Get address
    d = functionDirectory['global']['varTable'][varID]['address']
  # Push
  stackPush(operands, d)
  # Push
  stackPush(types, t)


# Constant was declared
# Push constant and type to stacks
def p_SA_EXP_1_CTE(p):
  '''SA_EXP_1_CTE : empty'''
  # Get id
  varID = p[-2]
  # Check if exists
  if constantTable.has_key(str(varID)):
    # Get type
    t = constantTable[str(varID)]['type']
    # Get address
    d = constantTable[str(varID)]['address']
  elif constantTable.has_key('-' + str(varID)):
    # Get type
    t = constantTable[str('-' + str(varID))]['type']
    # Get address
    d = constantTable[str('-' + str(varID))]['address']
  # Push
  stackPush(operands, d)
  # Push
  stackPush(types, t)


# * or / was declared
# SA EXP 2 - 5
# operators.Push(* or /)
def p_SA_EXP_ADD_OP(p):
  '''SA_EXP_ADD_OP : empty'''
  # Get op
  op = p[-1]
  # Push * or /
  stackPush(operators, op)


# Verify && or || are at top of stack
# Generate corresponding quadruple
def p_SA_EXP_6(p):
  '''SA_EXP_6 : empty'''
  # Global variables
  global cont
  # Top stack
  op = stackTop(operators)
  # if && or || are at top of stack
  temp_op = ['&&', '||']
  if op in temp_op:
    # Get righ and left operands 
    rightOp = stackPop(operands)
    leftOp = stackPop(operands)
    # Get right and left operand types
    rightType = stackPop(types)
    leftType = stackPop(types)
    # Get operator
    operator = stackPop(operators)
    # Validate if operation is valid
    resultType = getResultType(leftType, rightType, operator)
    # Valid operation
    if resultType > 0:
      # Create quadruple
      newQuadruple(quadruples, getOpCode(operator), leftOp, rightOp, tempVarCount[current_scope][getTypeString(resultType)])
      # Update quadruple counter
      cont += 1
      # Push result to operand stack
      stackPush(operands, tempVarCount[current_scope][getTypeString(resultType)])
      # Push type result to type stack
      stackPush(types, resultType)
      # Update tempVar count
      tempVarCount[current_scope][getTypeString(resultType)] += 1
    else:
      # Print error message
      print("Result type mismatch. '%s' '%s' '%s'" % (leftOp, operator, rightOp))
      exit(1)


# Verify [<, >, <=, >=, ==, !=] are at top of stack
# Generate corresponding quadruple
def p_SA_EXP_7(p):
  '''SA_EXP_7 : empty'''
  # Global variables
  global cont
  # Top stack
  op = stackTop(operators)
  # if [<, >, <=, >=, ==, !=] are at top of stack
  temp_op = ['<', '>', '<=', '>=', '==', '!=']
  if op in temp_op:
    # Get righ and left operands 
    rightOp = stackPop(operands)
    leftOp = stackPop(operands)
    # Get right and left operand types
    rightType = stackPop(types)
    leftType = stackPop(types)
    # Get operator
    operator = stackPop(operators)
    # Validate if operation is valid
    resultType = getResultType(leftType, rightType, operator)    
    # Valid operation
    if resultType > 0:
      # Create quadruple
      newQuadruple(quadruples, getOpCode(operator), leftOp, rightOp, tempVarCount[current_scope][getTypeString(resultType)])
      # Update quadruple counter
      cont += 1
      # Push result to operand stack
      stackPush(operands, tempVarCount[current_scope][getTypeString(resultType)])
      # Push type result to type stack
      stackPush(types, resultType)
      # Update tempVar count
      tempVarCount[current_scope][getTypeString(resultType)] += 1
    else:
      # Print error message
      print("Result type mismatch. '%s' '%s' '%s'" % (leftOp, operator, rightOp))
      exit(1)


# Verify + or -  are at top of stack
# Generate corresponding quadruple
def p_SA_EXP_8(p):
  '''SA_EXP_8 : empty'''
  # Global variables
  global cont
  # Top stack
  op = stackTop(operators)
  # if + or -  are at top of stack
  temp_op = ['+', '-']
  if op in temp_op:
    # Get righ and left operands 
    rightOp = stackPop(operands)
    leftOp = stackPop(operands)
    # Get right and left operand types
    rightType = stackPop(types)
    leftType = stackPop(types)
    # Get operator
    operator = stackPop(operators)
    # Validate if operation is valid
    resultType = getResultType(leftType, rightType, operator)
    # Valid operation
    if resultType > 0:
      # Create quadruple
      newQuadruple(quadruples, getOpCode(operator), leftOp, rightOp, tempVarCount[current_scope][getTypeString(resultType)])
      # Update quadruple counter
      cont += 1
      # Push result to operand stack
      stackPush(operands, tempVarCount[current_scope][getTypeString(resultType)])
      # Push type result to type stack
      stackPush(types, resultType)
      # Update tempVar count
      tempVarCount[current_scope][getTypeString(resultType)] += 1
    else:
      # Print error message
      print("Result type mismatch. '%s' '%s' '%s'" % (leftOp, operator, rightOp))
      exit(1)


# Verify * or / are at top of stack
# Generate corresponding quadruple
def p_SA_EXP_9(p):
  '''SA_EXP_9 : empty'''
  # Global variables
  global cont
  # Top stack
  op = stackTop(operators)
  # if * or / are at top of stack
  temp_op = ['*', '/']
  if op in temp_op:
    # Get righ and left operands 
    rightOp = stackPop(operands)
    leftOp = stackPop(operands)
    # Get right and left operand types
    rightType = stackPop(types)
    leftType = stackPop(types)
    # Get operator
    operator = stackPop(operators)
    # Validate if operation is valid
    resultType = getResultType(leftType, rightType, operator)
    # Valid operation
    if resultType > 0:
      # Create quadruple
      newQuadruple(quadruples, getOpCode(operator), leftOp, rightOp, tempVarCount[current_scope][getTypeString(resultType)])
      # Update quadruple counter
      cont += 1
      # Push result to operand stack
      stackPush(operands, tempVarCount[current_scope][getTypeString(resultType)])
      # Push type result to type stack
      stackPush(types, resultType)
      # Update tempVar count
      tempVarCount[current_scope][getTypeString(resultType)] += 1
    else:
      # Print error message
      print("Result type mismatch. '%s' '%s' '%s'" % (leftOp, operator, rightOp))
      exit(1)


# Verify = are at top of stack
# Generate corresponding quadruple
def p_SA_EXP_10(p):
  '''SA_EXP_10 : empty'''
  # Global variables
  global cont
  # Top stack
  op = stackTop(operators)
  # if * or / are at top of stack
  temp_op = ['=']
  if op in temp_op:
    # Get righ and left operands 
    rightOp = stackPop(operands)
    leftOp = stackPop(operands)
    # Get right and left operand types
    rightType = stackPop(types)
    leftType = stackPop(types)
    # Get operator
    operator = stackPop(operators)
    # Validate if operation is valid
    resultType = getResultType(leftType, rightType, operator)
    # Valid operation
    if resultType > 0:
      # Create quadruple
      newQuadruple(quadruples, getOpCode(operator), rightOp, None, leftOp)
      # Update quadruple counter
      cont += 1
    else:
      # Print error message
      print("Result type mismatch. '%s' '%s' '%s'" % (leftOp, operator, rightOp))
      exit(1)


# Parenthesis found in expression
# Add fake bottom to stack
def p_SA_FAKE_BOTTOM(p):
  '''SA_FAKE_BOTTOM : empty'''
  # Add fake bottom to operators
  stackPush(operators, '(')


# Ending parenthesis found in expression
# Remove fake bottom to stack
def p_SA_FAKE_BOTTOM_REMOVE(p):
  '''SA_FAKE_BOTTOM_REMOVE : empty'''
  # Remove fake bottom to operators
  stackPop(operators)


# -----------------------------------------------------
# ----------------- SEMANTIC ACTIONS ------------------
# ------------------- CONDITIONALS --------------------
# -----------------------------------------------------


# Ending parenthesis after conditional expression
# Validate condition and generate quadruples
def p_SA_COND_1(p):
  '''SA_COND_1 : empty'''
  # Global variables
  global cont
  # Get type top
  t = stackPop(types)
  # Validate previous expression is bool
  if t != getTypeCode('bool'):
    # Print error message
    print("Type mismatch. Not a boolean result from expression.")
    exit(1)
  else:
    # Get current operand
    result = stackPop(operands)
    # Create quadruple
    newQuadruple(quadruples, getOpCode('GoToF'), result, None, -1)
    # Update quadruple counter
    cont += 1
    # Push quadruple counter to jumps
    stackPush(jumps, cont-1)


# Ending of Block in conditional expression
# End block, fill blank jump
def p_SA_COND_2(p):
  '''SA_COND_2 : empty'''
  # Get top jump
  end = stackPop(jumps)
  # Fill blank space
  quadruples[end]['result'] = cont

# Else statement
# Generate final quadruple for if statement
def p_SA_COND_3(p):
  '''SA_COND_3 : empty'''
  # Global variables
  global cont
  # Cretae quadruple
  newQuadruple(quadruples, getOpCode('GoTo'), None, None, -1)
  # Update quadruple counter
  cont += 1
  # Get top jump
  jump = stackPop(jumps)
  # Push cont to jumps
  stackPush(jumps, cont-1)
  # Fill blank space
  quadruples[jump]['result'] = cont


# Elseif statement
# Generate quadruple
def p_SA_COND_4(p):
  '''SA_COND_4 : empty'''
  # Global variables
  global cont
  # Cretae quadruple
  newQuadruple(quadruples, getOpCode('GoTo'), None, None, -1)
  # Update quadruple counter
  cont += 1
  # Push cont to jumps
  stackPush(elseif_jumps, cont-1)


# Else statement
# Generate final quadruple for if statement
def p_SA_COND_5(p):
  '''SA_COND_5 : empty'''
  while len(elseif_jumps) > 0:
    # Get top jump
    jump = stackPop(elseif_jumps)
    # Fill blank space
    quadruples[jump]['result'] = cont


# -----------------------------------------------------
# ----------------- SEMANTIC ACTIONS ------------------
# ---------------------- LOOPS ------------------------
# -----------------------------------------------------


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
  # Global variables
  global cont
  # Get type
  t = stackPop(types)
  # Validate previous expression is bool
  if t != getTypeCode('bool'):
    # Print error message
    print("Type mismatch")
    exit(1)
  else:
    # Get current operand
    result = stackPop(operands)
    # Create quadruple
    newQuadruple(quadruples, getOpCode('GoToF'), result, None, 0)
    # Update quadruple counter
    cont += 1
    # Push quadruple counter to jumps
    stackPush(jumps, cont-1)


# End of loop block
# Generate final quadruple for loop
def p_SA_LOOP_3(p):
  '''SA_LOOP_3 : empty'''
  # Global variables
  global cont
  # Get jump
  end = stackPop(jumps)
  # Get jump
  r = stackPop(jumps)
  # Create quadruple
  newQuadruple(quadruples, getOpCode('GoTo'), None, None, r)
  # Update quadruple counter
  cont += 1
  # Fill blank space
  quadruples[end]['result'] = cont


# -----------------------------------------------------
# ----------------- SEMANTIC ACTIONS ------------------
# --------------------- FUNTIONS ----------------------
# -----------------------------------------------------


# Parameter declaration is going to start
# Generate necesary quadruples and variables
def p_SA_CALLFUNC_2(p):
  '''SA_CALLFUNC_2 : empty'''
  # Global variables
  global cont, parameterCount, pointers, callFunc_scopes
  # Function id
  funcID = p[-3]
  # Update current func call id
  stackPush(callFunc_scopes, funcID)
  # Create ERA quadruple
  newQuadruple(quadruples, getOpCode('Era'), funcID, None, None)
  # Update quadruple counter
  cont += 1
  # Reset parameter count
  parameterCount = 1
  # Push to pointer stack
  stackPush(pointers, 0)


# Parameter declared
# Validate parameter
def p_SA_CALLFUNC_3(p):
  '''SA_CALLFUNC_3 : empty'''
  # Global variables
  global cont
  # Get operand
  argument = stackPop(operands)
  # Get type
  argumentType = stackPop(types)
  # Get pointer
  pointer = stackTop(pointers)
  # Get call func scope
  callFunc_scope = stackTop(callFunc_scopes)
  # Verify type with current parameter in pointer
  if argumentType == functionDirectory[callFunc_scope]['signature'][pointer]:
    # Create action quadruple
    newQuadruple(quadruples, getOpCode('Param'), argument, None, functionDirectory[callFunc_scope]['paramAddresses'][pointer])
    # Update quadruple counter
    cont += 1
  else:
    # Print error message
    print("Result type mismatch. Function parameters incorrect. Parameter: '%s'" % argument)
    exit(1)


# Another parameter will be declared
# Update pointer
def p_SA_CALLFUNC_4(p):
  '''SA_CALLFUNC_4 : empty'''
  # Global variables
  global pointers
  # Get  pointer
  pointer = stackPop(pointers)
  # Update pointer
  pointer += 1
  # Push pointer
  stackPush(pointers, pointer)


# Parameters finished
# Verify total parameter count
def p_SA_CALLFUNC_5(p):
  '''SA_CALLFUNC_5 : empty'''
  # Get call func scope
  callFunc_scope = stackTop(callFunc_scopes)
  # Verify if function does not have any parameters
  if functionDirectory[callFunc_scope]['signature']:
    pointer = stackTop(pointers)
    # Verify parameter count
    if pointer+1 != len(functionDirectory[callFunc_scope]['signature']):
      # Print error message
      print("Incorrect parameter count.")
      exit(1)


# Function call finished
# Generate necesary quadruple
def p_SA_CALLFUNC_6(p):
  '''SA_CALLFUNC_6 : empty'''
  # Global variables
  global cont, pointers
  # Pop pointers
  stackPop(pointers)
  # Get function id
  funcID = p[-8]
  # In case the function is in an expression
  if funcID is None:
    funcID = p[-7]
  # Create gosub quadruple
  newQuadruple(quadruples, getOpCode('GoSub'), functionDirectory[funcID]['quadCounter'], None, None)
  # Update quadruple counter
  cont += 1


# Function check if there is return value
# Generate necesary quadruple
def p_SA_CALLFUNC_7(p):
  '''SA_CALLFUNC_7 : empty'''
  # Global Variables
  global cont, callFunc_scopes
  # Get function id
  funcID = p[-8]
  # Get call func scope
  callFunc_scope = stackTop(callFunc_scopes)
  # Get function type
  funcType = functionDirectory[callFunc_scope]['type']
  # Pop callFunc_scopes
  stackPop(callFunc_scopes)
  # Verify that function has a return type
  if datatypeCode[funcType] > 0:
    # Generate assignment quadruple to function value
    newQuadruple(quadruples, getOpCode('='), functionDirectory[funcID]['quadCounter'], None, tempVarCount[current_scope][funcType])
    # Update quadruple counter
    cont += 1
    # Push temporary value to operands
    stackPush(operands, tempVarCount[current_scope][funcType])
    # Push temporary value to types
    stackPush(types, datatypeCode[funcType])
    # Update tempVar count
    tempVarCount[current_scope][funcType] += 1


# Return value
# Generate necesary quadruple
def p_SA_RET(p):
  '''SA_RET : empty'''
  # Global variables
  global cont, funcWithReturn
  # Temporary variables for type validation
  returnType = stackPop(types)
  functionRetType = datatypeCode[functionDirectory[current_scope]['type']]
  # Value to return, result of expression
  returnValue = stackPop(operands)
  # Validate type of expression with return type of function
  if functionRetType == returnType:
    # Create return quadruple
    newQuadruple(quadruples, getOpCode('Return'), None, None, returnValue)
    # Update quadruple counter
    cont += 1
  else:
    print("Return type mismatch. Incorrect return. Function: '%s'" % current_scope)
    exit(1)
  # Define function has a return op
  funcWithReturn = True


# -----------------------------------------------------
# ----------------- SEMANTIC ACTIONS ------------------
# ---------------------- ARRAYS -----------------------
# -----------------------------------------------------

# Array id declared
# Get current array id and add dimension field
def p_SA_ARR_11(p):
  '''SA_ARR_11 : empty'''
  # Global Variables
  global array_id
  # Get array id
  array_id = p[-2]
  # Add dimension to var
  functionDirectory[current_scope]['varTable'][array_id]['dimension'].append({'dim': 0, 'size': 0, 'R': 1})


# Array size declared
# Dimension calculations
def p_SA_ARR_12(p):
  '''SA_ARR_12 : empty'''
  # Get size
  size = p[-1]
  # Get current dim
  current_dim = len(functionDirectory[current_scope]['varTable'][array_id]['dimension'])-1
  # Define array size
  functionDirectory[current_scope]['varTable'][array_id]['dimension'][current_dim]['size'] = size
  # Get R
  R = functionDirectory[current_scope]['varTable'][array_id]['dimension'][current_dim]['R']
  # Calc R
  functionDirectory[current_scope]['varTable'][array_id]['dimension'][current_dim]['R'] = size*R


# New Array dimension declared
# Prepare new dim
def p_SA_ARR_13(p):
  '''SA_ARR_13 : empty'''
  # Get previous dim
  prev_dim = len(functionDirectory[current_scope]['varTable'][array_id]['dimension'])-1
  # Get R
  R = functionDirectory[current_scope]['varTable'][array_id]['dimension'][prev_dim]['R']
  # Add new dimension to var
  functionDirectory[current_scope]['varTable'][array_id]['dimension'].append({'dim': prev_dim+1, 'size': 0, 'R': R})


# Array declaration finished
# Finish calculations
def p_SA_ARR_14(p):
  '''SA_ARR_14 : empty'''
  # Get number of total dimensions
  dim_total = len(functionDirectory[current_scope]['varTable'][array_id]['dimension'])-1
  # Define aux as the total array size
  total_array_size = functionDirectory[current_scope]['varTable'][array_id]['dimension'][dim_total]['R']
  # Define apropiate address to var
  if current_scope == 'global':
    # Increase global variable counter
    globalVarCount[current_type] += total_array_size-1
  else:
    # Increase global variable counter
    localVarCount[current_scope][current_type] += total_array_size-1


# Array access declared
# Verify var
def p_SA_ARR_15(p):
  '''SA_ARR_15 : empty'''
  # Global Variables
  global array_id, array_access_R
  # Get array id
  array_id = p[-2]
  # Verufy var is dimension var
  if not len(functionDirectory[current_scope]['varTable'][array_id]['dimension']) > 0:
    print("Incorrect variable type. Dimensioned variable required.")
    exit(1)
  # Define first dim
  dim = 0
  # Push var to dimensions stack
  stackPush(dimensions, {'varID': array_id, 'dim': dim})
  # Get last dim
  last_dim = len(functionDirectory[current_scope]['varTable'][array_id]['dimension'])-1
  # Define R for next calc
  array_access_R = functionDirectory[current_scope]['varTable'][array_id]['dimension'][last_dim]['R']


# Array access expression declared
# Create quadruples
def p_SA_ARR_16(p):
  '''SA_ARR_16 : empty'''
  # Global Variables
  global array_access_R, cont
  # Get durrent dim
  current_dim = stackTop(dimensions)['dim']
  # Get oprand
  op = stackTop(operands)
  # Define inferior limit
  inf = 0
  # Get superior limit
  sup = functionDirectory[current_scope]['varTable'][array_id]['dimension'][current_dim]['size']
  # Create quadruple
  newQuadruple(quadruples, getOpCode('Ver'), op, inf, sup-1)
  # Update quadruple counter
  cont += 1
  # Check next dim not null
  if current_dim < len(functionDirectory[current_scope]['varTable'][array_id]['dimension'])-1:
    # Get operand
    aux = stackPop(operands)
    # Calc mDim
    mDim = array_access_R / sup
      # Verify if string is in constants table
    if not constantTable.has_key(str(mDim)):
      # Create constant
      constantTable[str(mDim)] = {'type': getTypeCode('int'), 'address': constVarCount['int'], 'val': mDim}
      # Increase constant variable counter
      constVarCount['int'] += 1
    # Create quadruple
    newQuadruple(quadruples, getOpCode('*'), aux, constantTable[str(mDim)]['address'], tempVarCount[current_scope][getTypeString(getTypeCode('int'))])
    # Update quadruple counter
    cont += 1
    # Push to operands
    stackPush(operands, tempVarCount[current_scope][getTypeString(getTypeCode('int'))])
    # Push type
    stackPush(types, getTypeCode('int'))
    # Increase constant variable counter
    tempVarCount[current_scope][getTypeString(getTypeCode('int'))] += 1
    # Update R
    array_access_R = mDim
  # Check current dim is not the first dim
  if current_dim > 0:
    # Get operand
    aux2 = stackPop(operands)
    # Get operand
    aux1 = stackPop(operands)
    # Create quadruple
    newQuadruple(quadruples, getOpCode('+'), aux1, aux2, tempVarCount[current_scope][getTypeString(getTypeCode('int'))])
    # Update quadruple counter
    cont += 1
    # Push to operands
    stackPush(operands, tempVarCount[current_scope][getTypeString(getTypeCode('int'))])
    # Push type
    stackPush(types, getTypeCode('int'))
    # Increase constant variable counter
    tempVarCount[current_scope][getTypeString(getTypeCode('int'))] += 1


# New Array access dimension declared
# Update dim
def p_SA_ARR_17(p):
  '''SA_ARR_17 : empty'''
  # Pop dimension stack
  dim = stackPop(dimensions)
  # Update dim
  dim['dim'] += 1
  # Push dimension
  stackPush(dimensions, dim)


# Array access finished
# Finish access
def p_SA_ARR_18(p):
  '''SA_ARR_18 : empty'''
  # Global Variables
  global cont
  # Get operand
  aux1 = stackPop(operands)
  # Get type
  t = getTypeCode('int')
  # Get base direction
  dir = functionDirectory[current_scope]['varTable'][array_id]['address']
  # Verify dir is in constTable
  if not constantTable.has_key(str(dir)):
    # Create constant
    constantTable[str(dir)] = {'type': getTypeCode('int'), 'address': constVarCount[getTypeString(getTypeCode('int'))], 'val': dir}
    # Increase constant variable counter
    constVarCount[getTypeString(getTypeCode('int'))] += 1
  # Create quadruple
  newQuadruple(quadruples, getOpCode('+'), aux1, constantTable[str(dir)]['address'], tempVarCount[current_scope][getTypeString(getTypeCode('int'))])
  # Update quadruple counter
  cont += 1
  # Cretae special dir
  specialDir = '(' + str(tempVarCount[current_scope][getTypeString(getTypeCode('int'))]) + ')'
  # Push result to operand stack
  stackPush(operands, specialDir)
  # Push type
  stackPush(types, getTypeCode('int'))
  # Update tempVar count
  tempVarCount[current_scope][getTypeString(getTypeCode('int'))] += 1
  # Pop dimensions stack
  stackPop(dimensions)


# Array var declared
# Set current array id
def p_SA_ARR_19(p):
  '''SA_ARR_19 : empty'''
  # Global Variables
  global array_id
  # Set current array id
  array_id = p[-3]
  # Search for id in current varTable and in global varTable
  if not (functionDirectory[current_scope]['varTable'].has_key(array_id) or functionDirectory['global']['varTable'].has_key(array_id)):
    # Print error message
    print("ID does not exist. ID: '%s'" % array_id)
    exit(1)
  # Validate current id is dimensioned var
  if not len(functionDirectory[current_scope]['varTable'][array_id]['dimension']) > 0:
    print("Incorrect variable type. Array variable required.")
    exit(1)


# Array assignment started a = [ ]
# Prepare assignment
def p_SA_ARR_20(p):
  '''SA_ARR_20 : empty'''
  # Global Variables
  global dim_counter, current_dim
  # Reset array size
  dim_counter = 0
  # Set current dim
  current_dim = 0


# Array declaration [] started
# Count[]
def p_SA_ARR_21(p):
  '''SA_ARR_21 : empty'''
  # Global Variables
  global dim_counter
  # Reset array size
  dim_counter += 1


# Array [] finished declared
# Validate correct count
def p_SA_ARR_22(p):
  '''SA_ARR_22 : empty'''
  # Global Variables
  global array_counter, array_location
  # Validate current id is dimensioned var
  print dim_counter
  if not len(functionDirectory[current_scope]['varTable'][array_id]['dimension']) == dim_counter:
    print("Incorrect variable type. Array variable required.")
    exit(1)
  # Det array location
  array_location = 0
  # Reset array counter
  array_counter = 0


# Array values are being assigned
# Create array assignment quadruples
def p_SA_ARR_23(p):
  '''SA_ARR_23 : empty'''
  # Global Variables
  global array_counter, cont, array_size, current_dim, array_location
  # Get base direction
  dir = functionDirectory[current_scope]['varTable'][array_id]['address']
  # Get array count
  array_size = functionDirectory[current_scope]['varTable'][array_id]['dimension'][current_dim-1]['size']
  # Validate limit of array size i not exceeded
  if array_counter < array_size:
    # Get operand
    op = stackPop(operands) 
    # Create quadruple
    newQuadruple(quadruples, getOpCode('='), op, None, dir+array_location)
    # Update quadruple counter
    cont += 1
    # Update array counter
    array_counter += 1
    # Update array location
    array_location += 1
  else:
    print("Wrong array input size.")
    exit(1)


# Array values are being assigned
# Validate dimension count is correct
def p_SA_ARR_24(p):
  '''SA_ARR_24 : empty'''
  # Global Variables
  global current_dim
  # Validate number of dimensions with count
  if not current_dim <= dim_counter:
    print("Wrong array declaration size.")
    exit(1)


# Array values are being assigned
# Update current dim
def p_SA_ARR_25(p):
  '''SA_ARR_25 : empty'''
  # Global Variables
  global current_dim, array_counter
  # Update current dim
  current_dim += 1
  # Reset array counter
  array_counter = 0

# -----------------------------------------------------
# ----------------- SEMANTIC ACTIONS ------------------
# ---------------------- PRINTS -----------------------
# -----------------------------------------------------

# Print declared
# Create print quadruple
def p_SA_PRINT_DATA(p):
  '''SA_PRINT_DATA : empty'''
  # Globals
  global cont
  # Get id
  varID = stackPop(operands)
  # Pop type
  stackPop(types)
  # Create quadruple
  newQuadruple(quadruples, getOpCode('Print'), None, None, varID)
  # Update quadruple counter
  cont += 1


# -----------------------------------------------------
# ----------------- SEMANTIC ACTIONS ------------------
# -------------------- DATAFRAMES ---------------------
# -----------------------------------------------------

# Binding operation declared
# Get df id
def p_SA_DF_BINDINGS_1(p):
  '''SA_DF_BINDINGS_1 : empty'''
  # Globals
  global current_df, cont
  # Get df id
  current_df = p[-2]
  # Get type of bind
  t_bind = p[-4]
  # New special dataframe
  special_df = '[' + str(current_df) + ']'
  # Verify if string is in constants table
  if not constantTable.has_key(str(special_df)):
    # Create constant
    constantTable[str(special_df)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': special_df}
    # Increase constant variable counter
    constVarCount['string'] += 1
    # Verify scope
  if dataframeTable['global'].has_key(current_df):
    scope = 1
  else:
    scope = 2
  if t_bind == 'cbind':
    # Create quadruple
    newQuadruple(quadruples, getOpCode('ColBind'), None, scope, constantTable[special_df]['address'])
  else:
    # Create quadruple
    newQuadruple(quadruples, getOpCode('RowBind'), None, scope, constantTable[special_df]['address'])
  # Update quadruple counter
  cont += 1


# Access to row or column declared
# Create access quadruple
def p_SA_DF_ACCESS_1(p):
  '''SA_DF_ACCESS_1 : empty'''
  # Globals
  global cont
  # Get df id for access
  access_df = p[-7]
  # Get expression result
  exp = stackPop(operands)
  # Get type
  t_exp = stackPop(types)
  # Get row or col
  access_type = p[-4]
  # New special dataframe
  special_df = '[' + str(access_df) + ']'
  # verify scope
  if dataframeTable['global'].has_key(access_df):
    scope = 1
  else:
    scope = 2
  # Check col or row acces
  if access_type == 'row':
    # Create quadruple
    newQuadruple(quadruples, getOpCode('AccessRow'), constantTable[special_df]['address'], scope, exp)
  else:
    # Create quadruple
    newQuadruple(quadruples, getOpCode('AccessCol'), constantTable[special_df]['address'], scope, exp)
  # Update quadruple counter
  cont += 1


# 1 Exp in print cell declared
# Define row
def p_SA_DF_PRINTCELL_1(p):
  '''SA_DF_PRINTCELL_1 : empty'''
  # Globals
  global df_print_row
  # Pop operands
  row = stackPop(operands)
  # Pop types
  stackPop(types)
  # define row to print
  df_print_row = row


# 2 Exp in print cell declared
# Define col
def p_SA_DF_PRINTCELL_2(p):
  '''SA_DF_PRINTCELL_2 : empty'''
  # Globals
  global df_print_col
  # Pop operands
  col = stackPop(operands)
  # Pop types
  stackPop(types)
  # Define row to print
  df_print_col = col
  

# Print cell finished declaring
# Create quadruple
def p_SA_DF_PRINTCELL_3(p):
  '''SA_DF_PRINTCELL_3 : empty'''
  # Globals
  global cont
  # Get df id
  current_df = p[-10]
  # New special dataframe
  special_df = '[' + str(current_df) + ']'
  # Special cel
  special_cell = '[' + str(df_print_row) + ',' + str(df_print_col)+ ']'
  # Verify if string is in constants tabl
  if not constantTable.has_key(str(special_cell)): 
    # Create constant
    constantTable[str(special_cell)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': special_cell}
    # Increase constant variable counter
    constVarCount['string'] += 1
    # Create constant
    constantTable[str(df_print_row)] = {'type': getTypeCode('int'), 'address': constVarCount['int'], 'val': df_print_row}
    # Increase constant variable counter
    constVarCount['int'] += 1
    # Create constant
    constantTable[str(df_print_col)] = {'type': getTypeCode('int'), 'address': constVarCount['int'], 'val': df_print_col}
    # Increase constant variable counter
    constVarCount['int'] += 1
  # Verify scope
  if dataframeTable['global'].has_key(current_df):
    scope = 1
  else:
    scope = 2
  # Create quadruple
  newQuadruple(quadruples, getOpCode('PrintCell'), constantTable[special_df]['address'], scope, constantTable[special_cell]['address'])
  # Update quadruple counter
  cont += 1


# Print col declared
# Create quadruple
def p_SA_DF_PRINTCOL_1(p):
  '''SA_DF_PRINTCOL_1 : empty'''
  # Globals
  global cont
  # Create quadruple
  newQuadruple(quadruples, getOpCode('PrintCol'), None, None, None)
  # Update quadruple counter
  cont += 1


# Print headers declared
# Create quadruple
def p_SA_DF_PRINTHEADERS_1(p):
  '''SA_DF_PRINTHEADERS_1 : empty'''
  # Globals
  global cont
  # Get df id
  current_df = p[-2]
  # New special dataframe
  special_df = '[' + str(current_df) + ']'
  # Verify if string is in constants table
  if not constantTable.has_key(str(special_df)):
    # Create constant
    constantTable[str(special_df)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': special_df}
    # Increase constant variable counter
    constVarCount['string'] += 1
  # Verify scope
  if dataframeTable['global'].has_key(current_df):
    scope = 1
  else:
    scope = 2
  # Create quadruple
  newQuadruple(quadruples, getOpCode('PrintHeaders'), None, scope, constantTable[special_df]['address'])
  # Update quadruple counter
  cont += 1


# Print row declared
# Create quadruple
def p_SA_DF_PRINTROW_1(p):
  '''SA_DF_PRINTROW_1 : empty'''
  # Globals
  global cont
  # Create quadruple
  newQuadruple(quadruples, getOpCode('PrintRow'), None, None, None)
  # Update quadruple counter
  cont += 1


# Print tags declared
# Create quadruple
def p_SA_DF_PRINTTAGS_1(p):
  '''SA_DF_PRINTTAGS_1 : empty'''
  # Globals
  global cont
  # Get df id
  current_df = p[-2]
  # New special dataframe
  special_df = '[' + str(current_df) + ']'
  # verify if string is in constants table
  if not constantTable.has_key(str(special_df)): 
    # Create constant
    constantTable[str(special_df)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': special_df}
    # Increase constant variable counter
    constVarCount['string'] += 1
  # Verify scope
  if dataframeTable['global'].has_key(current_df):
    scope = 1
  else:
    scope = 2
  # Create quadruple
  newQuadruple(quadruples, getOpCode('PrintTags'), None, scope, constantTable[special_df]['address'])
  # Update quadruple counter
  cont += 1


# Print df declared
# Create quadruple
def p_SA_DF_PRINT(p):
  '''SA_DF_PRINT : empty'''
  # Globals
  global cont
  # Get df id
  current_df = p[-2]
  # New special dataframe
  special_df = '[' + str(current_df) + ']'
  # Verify if string is in constants table
  if not constantTable.has_key(str(special_df)): 
    # Create constant
    constantTable[str(special_df)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': special_df}
    # Increase constant variable counter
    constVarCount['string'] += 1
  # Verify scope
  if dataframeTable['global'].has_key(current_df):
    scope = 1
  else:
    scope = 2
  # Create quadruple
  newQuadruple(quadruples, getOpCode('PrintDf'), None, scope, constantTable[special_df]['address'])
  # Update quadruple counter
  cont += 1


# Print df data declared
# Create quadruple
def p_SA_DF_PRINT_DATA(p):
  '''SA_DF_PRINT_DATA : empty'''
  # Globals
  global cont
  # Get df id
  current_df = p[-2]
  # New special dataframe
  special_df = '[' + str(current_df) + ']'
  # Verify if string is in constants table
  if not constantTable.has_key(str(special_df)): 
    # Create constant
    constantTable[str(special_df)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': special_df}
    # Increase constant variable counter
    constVarCount['string'] += 1
  # Verify scope
  if dataframeTable['global'].has_key(current_df):
    scope = 1
  else:
    scope = 2
  # Create quadruple
  newQuadruple(quadruples, getOpCode('PrintDfData'), None, scope, constantTable[special_df]['address'])
  # Update quadruple counter
  cont += 1
  

# Get data using headers declared
# Create quadruple
def p_SA_DF_HEADER(p):
  '''SA_DF_HEADER : empty'''
  # Globals
  global cont
  # Get df id
  current_df = p[-4]
  # Get headerID
  headerID = p[-1]
  # New special dataframe
  special_df = '[' + str(current_df) + ']'
  # Verify if string is in constants tabl
  if not constantTable.has_key(str(headerID)): 
    # Create constant
    constantTable[str(headerID)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': headerID}
    # Increase constant variable counter
    constVarCount['string'] += 1
  # Create quadruple
  newQuadruple(quadruples, getOpCode('AccessCol'), constantTable[special_df]['address'], None, constantTable[headerID]['address'])
  # Update quadruple counter
  cont += 1


# Correlation declared
# Create quadruple
def p_SA_DF_CORR(p):
  '''SA_DF_CORR : empty'''
  # Globals
  global cont
  # Get df id
  current_df1 = p[-7]
  # Get df id
  current_df2 = p[-4]
  # Get constant value
  value = p[-1]
  # New special dataframe
  special_df1 = '[' + str(current_df1) + ']'
  # New special dataframe
  special_df2 = '[' + str(current_df2) + ']'
  # Verify if string is in constants tabl
  if not constantTable.has_key(str(special_df1)): 
    # Create constant
    constantTable[str(special_df1)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': special_df1}
    # Increase constant variable counter
    constVarCount['string'] += 1
    # Verify if string is in constants tabl
  if not constantTable.has_key(str(special_df2)): 
    # Create constant
    constantTable[str(special_df2)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': special_df2}
    # Increase constant variable counter
    constVarCount['string'] += 1
    # Verify if string is in constants tabl
  if not constantTable.has_key(str(value)): 
    # Create constant
    constantTable[str(value)] = {'type': getTypeCode('float'), 'address': constVarCount['float'], 'val': value}
    # Increase constant variable counter
    constVarCount['float'] += 1
  # Create quadruple
  newQuadruple(quadruples, getOpCode('Corr'), constantTable[str(special_df1)]['address'], constantTable[str(special_df2)]['address'], constantTable[str(value)]['address'] )
  # Update quadruple counter
  cont += 1


# Correlation headers declared
# Create quadruple
def p_SA_DF_CORR_HEADERS_1(p):
  '''SA_DF_CORR_HEADERS_1 : empty'''
  # Globals
  global cont
  # Get df id 1
  current_df1 = p[-7]
  # Get df id 2
  current_df2 = p[-4]
  # Get value
  value = p[-1]
  # Verify scope
  if dataframeTable['global'].has_key(current_df):
    scope = 1
  else:
    scope = 2
  # New special dataframe
  special_df1 = '[' + str(current_df1) + ']'
  # New special dataframe
  special_df2 = '[' + str(current_df2) + ']'
  # Verify if string is in constants tabl
  if not constantTable.has_key(str(special_df1)): 
    # Create constant
    constantTable[str(special_df1)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': special_df1}
    # Increase constant variable counter
    constVarCount['string'] += 1
    # Verify if string is in constants tabl
  if not constantTable.has_key(str(special_df2)): 
    # Create constant
    constantTable[str(special_df2)] = {'type': getTypeCode('string'), 'address': constVarCount['string'], 'val': special_df2}
    # Increase constant variable counter
    constVarCount['string'] += 1
    # Verify if string is in constants tabl
  if not constantTable.has_key(str(value)): 
    # Create constant
    constantTable[str(value)] = {'type': getTypeCode('float'), 'address': constVarCount['float'], 'val': value}
    # Increase constant variable counter
    constVarCount['float'] += 1
  # Create quadruple
  newQuadruple(quadruples, getOpCode('CorrHeaders'), constantTable[str(special_df1)]['address'], constantTable[str(special_df2)]['address'], constantTable[str(value)]['address'] )
  # Update quadruple counter
  cont += 1



# Build the parser
yacc.yacc()

# -----------------------------------------------------
# ---------------------- MAIN -------------------------
# -----------------------------------------------------

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
        print(dirProc)
      # Execute virtual machine
      execute(quadruples, globalVarCount, localVarCount, tempVarCount, constVarCount, constantTable, dataframeTable)
      exit(1)
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