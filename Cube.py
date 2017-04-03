# Seamtnic Cube
# Patricio Sanchez A01191893
# Mauro Amarante A01191893

# Data type codes
datatypeCode = {
  'void' : 0,
  'bool' : 1,
  'boolArray' : 11,
  'int' : 2,
  'intArray' : 22,
  'float' : 3,
  'floatArray' : 33,
  'char' : 4,
  'charArray' : 44,
  'string' : 5,
  'stringArray' : 55,
  'dataframe' : 6,
  'dataframeArray' : 66
}

# Operation code
opCode = {
  'relop_gr' : 100,
  'relop_ls' : 101,
  'relop_grequal' : 102,
  'relop_lsequal' : 103,
  'relop_lsequal' : 104,
  'relop_equals' : 105,
  'relop_notequal' : 106,
  'relop_and' : 107,
  'relop_or' : 108,
  'equal' : 109,
  'plus' : 110,
  'minus' : 111,
  'times' : 112,
  'divide' : 113
}

# 20,000 slots per block
# Global memory
initial_global_bool = 10000
initial_global_int = 13333
initial_global_float = 16666
initial_global_char = 19999
initial_global_string = 23332
initial_global_dataframe = 26665

# Local memory
initial_local_bool = 30000
initial_local_int = 33333
initial_local_float = 36666
initial_local_char = 49999
initial_local_string = 43332
initial_local_dataframe = 46665

# Temporal memory
initial_temp_bool = 50000
initial_temp_int = 53333
initial_temp_float = 56666
initial_temp_char = 59999
initial_temp_string = 63332
initial_temp_dataframe = 66665


# Constant memory
initial_constant_bool = 70000
initial_constnt_int = 73333
initial_constant_float = 76666
initial_constant_char = 79999
initial_constant_string = 83332
initial_constant_dataframe = 86665

cube = {}

# Assignment
cube['bool=bool'] = datatypeCode['bool']
cube['int=int'] = datatypeCode['int']
cube['int=float'] = datatypeCode['int']
cube['int=char'] = datatypeCode['int']
cube['float=float'] = datatypeCode['float']
cube['float=int'] = datatypeCode['float']
cube['char=char'] = datatypeCode['char']
cube['char=int'] = datatypeCode['char']
cube['string=string'] = datatypeCode['string']
cube['dataframe=dataframe'] = datatypeCode['dataframe']

# Sum
cube['int+int'] = datatypeCode['int']
cube['int+float'] = datatypeCode['float']
cube['int+char'] = datatypeCode['int']
cube['float+int'] = datatypeCode['float']
cube['float+float'] = datatypeCode['float']
cube['char+char'] = datatypeCode['int']
cube['char+int'] = datatypeCode['int']
cube['string+string'] = datatypeCode['string']

# Substraction
cube['int-int'] = datatypeCode['int']
cube['int-float'] = datatypeCode['float']
cube['int-char'] = datatypeCode['int']
cube['float-int'] = datatypeCode['float']
cube['float-float'] = datatypeCode['float']
cube['char-char'] = datatypeCode['int']
cube['char-int'] = datatypeCode['int']

# Multiplication
cube['int*int'] = datatypeCode['int']
cube['int*float'] = datatypeCode['float']
cube['int*char'] = datatypeCode['int']
cube['float*int'] = datatypeCode['float']
cube['float*float'] = datatypeCode['float']
cube['char*char'] = datatypeCode['int']
cube['char*int'] = datatypeCode['int']

# Divison
cube['int/int'] = datatypeCode['int']
cube['int/float'] = datatypeCode['float']
cube['int/char'] = datatypeCode['int']
cube['float/int'] = datatypeCode['float']
cube['float/float'] = datatypeCode['float']
cube['char/char'] = datatypeCode['int']
cube['char/int'] = datatypeCode['int']

# Less than
cube['int<int'] = datatypeCode['bool']
cube['int<float'] = datatypeCode['bool']
cube['int<char'] = datatypeCode['bool']
cube['float<int'] = datatypeCode['bool']
cube['float<float'] = datatypeCode['bool']
cube['char<char'] = datatypeCode['bool']
cube['char<int'] = datatypeCode['bool']

# Greater than
cube['int>int'] = datatypeCode['bool']
cube['int>float'] = datatypeCode['bool']
cube['int>char'] = datatypeCode['bool']
cube['float>int'] = datatypeCode['bool']
cube['float>float'] = datatypeCode['bool']
cube['char>char'] = datatypeCode['bool']
cube['char>int'] = datatypeCode['bool']

# Less than/equal
cube['int<=int'] = datatypeCode['bool']
cube['int<=float'] = datatypeCode['bool']
cube['int<=char'] = datatypeCode['int']
cube['float<=int'] = datatypeCode['bool']
cube['float<=float'] = datatypeCode['bool']
cube['char<=char'] = datatypeCode['bool']
cube['char<=int'] = datatypeCode['bool']

# Greater than/equal
cube['int>=int'] = datatypeCode['bool']
cube['int>=float'] = datatypeCode['bool']
cube['int>=char'] = datatypeCode['bool']
cube['float>=int'] = datatypeCode['bool']
cube['float>=float'] = datatypeCode['bool']
cube['char>=char'] = datatypeCode['bool']
cube['char>=int'] = datatypeCode['bool']

# Equal
cube['bool==bool'] = datatypeCode['bool']
cube['int==int'] = datatypeCode['bool']
cube['int==float'] = datatypeCode['bool']
cube['int==char'] = datatypeCode['bool']
cube['float==int'] = datatypeCode['bool']
cube['float==float'] = datatypeCode['bool']
cube['char==char'] = datatypeCode['bool']
cube['char==int'] = datatypeCode['bool']
cube['dataframe==dataframe'] = datatypeCode['bool']

# Not equal
cube['bool!=bool'] = datatypeCode['bool']
cube['int!=int'] = datatypeCode['bool']
cube['int!=float'] = datatypeCode['bool']
cube['int!=char'] = datatypeCode['bool']
cube['float!=int'] = datatypeCode['bool']
cube['float!=float'] = datatypeCode['bool']
cube['char!=char'] = datatypeCode['bool']
cube['char!=int'] = datatypeCode['bool']
cube['dataframe!=dataframe'] = datatypeCode['bool']

# And
cube['bool&&bool'] = datatypeCode['bool']

# Or
cube['bool||bool'] = datatypeCode['bool']

def getTypeString (type):
  if type == 1:
    return 'bool'
  elif type == 11: 
    return 'boolArray'
  elif type == 2: 
    return 'int'
  elif type == 22: 
    return 'intArray'
  elif type == 3:
    return 'float'
  elif type == 33: 
    return 'floatArray'
  elif type == 4:
    return 'char'
  elif type == 44: 
    return 'charArray'
  elif type == 5: 
    return 'string'
  elif type == 55: 
    return 'stringArray'
  elif type == 6:
    return 'dataframe'
  elif type == 66: 
    return 'dataframeArray'

def getTypeCode (type):
  if type == 'bool':
    return datatypeCode['bool']
  elif type == 'boolArray': 
    return datatypeCode['boolArray']
  elif type == 'int': 
    return datatypeCode['int']
  elif type == 'intArray': 
    return datatypeCode['intArray']
  elif type == 'float':
    return datatypeCode['float']
  elif type == 'floatArray': 
    return datatypeCode['floatArray']
  elif type == 'char':
    return datatypeCode['char']
  elif type == 'charArray': 
    return datatypeCode['charArray']
  elif type == 'string': 
    return datatypeCode['string']
  elif type == 'stringArray': 
    return datatypeCode['stringArray']
  elif type == 'dataframe':
    return datatypeCode['dataframe']
  elif type == 'dataframeArray': 
    return datatypeCode['dataframeArray']

def getResultType(operand1, operand2, operator):
  one = getTypeString(operand1)
  two = getTypeString(operand2)
  op = operator

  result = one + op + two

  if not result in cube.keys():
    return -1
  else:
    return cube[result]