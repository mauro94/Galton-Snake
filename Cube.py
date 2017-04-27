# Semantic Cube
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
  'string' : 4,
  'stringArray' : 44,
  'dataframe' : 5,
  'dataframeArray' : 55
}

# Operation code
opCode = {
  # relop_gr
  100 : '>',
  # relop_ls
  101 : '<',
  # relop_grequal
  102 : '>=',
  # relop_lsequal
  103 : '<=',
  # relop_equals
  104 : '==',
  # relop_notequal
  105 : '!=',
  # relop_and
  106 : '&&',
  # relop_or
  107 : '||',
  # equal
  108 : '=',
  # plus
  109 : '+',
  # minus
  110 : '-',
  # times
  111 : '*',
  # divide
  112 : '/'
}

cube = {}

# Assignment
cube['bool=bool'] = datatypeCode['bool']
cube['int=int'] = datatypeCode['int']
cube['int=float'] = datatypeCode['int']
cube['float=float'] = datatypeCode['float']
cube['float=int'] = datatypeCode['float']
cube['string=string'] = datatypeCode['string']
cube['dataframe=dataframe'] = datatypeCode['dataframe']

# Sum
cube['int+int'] = datatypeCode['int']
cube['int+float'] = datatypeCode['float']
cube['float+int'] = datatypeCode['float']
cube['float+float'] = datatypeCode['float']
cube['string+string'] = datatypeCode['string']

# Substraction
cube['int-int'] = datatypeCode['int']
cube['int-float'] = datatypeCode['float']
cube['float-int'] = datatypeCode['float']
cube['float-float'] = datatypeCode['float']

# Multiplication
cube['int*int'] = datatypeCode['int']
cube['int*float'] = datatypeCode['float']
cube['float*int'] = datatypeCode['float']
cube['float*float'] = datatypeCode['float']

# Divison
cube['int/int'] = datatypeCode['int']
cube['int/float'] = datatypeCode['float']
cube['float/int'] = datatypeCode['float']
cube['float/float'] = datatypeCode['float']

# Less than
cube['int<int'] = datatypeCode['bool']
cube['int<float'] = datatypeCode['bool']
cube['float<int'] = datatypeCode['bool']
cube['float<float'] = datatypeCode['bool']

# Greater than
cube['int>int'] = datatypeCode['bool']
cube['int>float'] = datatypeCode['bool']
cube['float>int'] = datatypeCode['bool']
cube['float>float'] = datatypeCode['bool']

# Less than/equal
cube['int<=int'] = datatypeCode['bool']
cube['int<=float'] = datatypeCode['bool']
cube['float<=int'] = datatypeCode['bool']
cube['float<=float'] = datatypeCode['bool']

# Greater than/equal
cube['int>=int'] = datatypeCode['bool']
cube['int>=float'] = datatypeCode['bool']
cube['float>=int'] = datatypeCode['bool']
cube['float>=float'] = datatypeCode['bool']

# Equal
cube['bool==bool'] = datatypeCode['bool']
cube['int==int'] = datatypeCode['bool']
cube['int==float'] = datatypeCode['bool']
cube['float==int'] = datatypeCode['bool']
cube['float==float'] = datatypeCode['bool']
cube['dataframe==dataframe'] = datatypeCode['bool']

# Not equal
cube['bool!=bool'] = datatypeCode['bool']
cube['int!=int'] = datatypeCode['bool']
cube['int!=float'] = datatypeCode['bool']
cube['float!=int'] = datatypeCode['bool']
cube['float!=float'] = datatypeCode['bool']
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
    return 'string'
  elif type == 44: 
    return 'stringArray'
  elif type == 5:
    return 'dataframe'
  elif type == 55: 
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

def getOperationCode(operator):
  return opCode[operator]