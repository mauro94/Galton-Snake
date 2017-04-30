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
  '>' : 100,
  # relop_ls
  '<' : 101,
  # relop_grequal
  '>=' : 102,
  # relop_lsequal
  '<=' : 103,
  # relop_equals
  '==' : 104,
  # relop_notequal
  '!=' : 105,
  # relop_and
  '&&' : 106,
  # relop_or
  '||' : 107,
  # equal
  '=' : 108,
  # plus
  '+' : 109,
  # minus
  '-' : 110,
  # times
  '*' : 111,
  # divide
  '/' : 112,
  # GoTo
  'GoTo' : 200,
  # GoToF
  'GoToF' : 201,
  # Return
  'Return' : 202,
  # EndProc
  'EndProc' : 203,
  # end
  'End' : 204,
  # era
  'Era' : 205,
  # param
  'Param' : 206,
  # GoSub
  'GoSub' : 207,
  # Ver
  'Ver' : 208,
  # Print
  'Print' : 209,
  # Read File
  'Read' : 300,
  # Access column
  'AccessCol' : 301,
  # Access row
  'AccessRow' : 302,
  # Print cell
  'PrintCell' : 303,
  # Print cell
  'PrintCol' : 304,
  # Print cell
  'PrintHeaders' : 305,
  # Print cell
  'PrintRow' : 306,
  # Print tags
  'PrintTags' : 306
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

def getOpString (op):
  if op == 100:
    return '>'
  elif op == 101: 
    return '<'
  elif op == 102: 
    return '>='
  elif op == 103: 
    return '<='
  elif op == 104:
    return '=='
  elif op == 105: 
    return '!='
  elif op == 106: 
    return '&&'
  elif op == 107: 
    return '||'
  elif op == 108:
    return '='
  elif op == 109: 
    return '+'
  elif op == 110: 
    return '-'
  elif op == 111: 
    return '*'
  elif op == 112: 
    return '/'
  elif op == 200: 
    return 'GoTo'
  elif op == 201: 
    return 'GoToF'
  elif op == 202: 
    return 'Return'
  elif op == 203: 
    return 'EndProc'
  elif op == 204: 
    return 'End'
  elif op == 205: 
    return 'Era'
  elif op == 206: 
    return 'Param'
  elif op == 207: 
    return 'GoSub'
  elif op == 208: 
    return 'Ver'
  elif op == 209: 
    return 'Print'
  elif op == 300:
    return 'Read'
  elif op == 301:
    return 'AccessCol'
  elif op == 302:
    return 'AccessRow'
  elif op == 303:
    return 'PrintCell'
  elif op == 304:
    return 'PrintCol'
  elif op == 305:
    return 'PrintHeaders'
  elif op == 306:
    return 'PrintRow'
  elif op == 307:
    return 'PrintTags' 

def getOpCode (op):
  if op == '>':
    return opCode['>']
  elif op == '<': 
    return opCode['<']
  elif op == '>=': 
    return opCode['>=']
  elif op == '<=': 
    return opCode['<=']
  elif op == '==':
    return opCode['==']
  elif op == '!=': 
    return opCode['!=']
  elif op == '&&': 
    return opCode['&&']
  elif op == '||': 
    return opCode['||']
  elif op == '=':
    return opCode['=']
  elif op == '+': 
    return opCode['+']
  elif op == '-': 
    return opCode['-']
  elif op == '*': 
    return opCode['*']
  elif op == '/': 
    return opCode['/']
  elif op == 'GoTo': 
    return opCode['GoTo']
  elif op == 'GoToF': 
    return opCode['GoToF']
  elif op == 'Return': 
    return opCode['Return']
  elif op == 'EndProc': 
    return opCode['EndProc']
  elif op == 'End': 
    return opCode['End']
  elif op == 'Era': 
    return opCode['Era']
  elif op == 'Param': 
    return opCode['Param']
  elif op == 'GoSub': 
    return opCode['GoSub']
  elif op == 'Ver': 
    return opCode['Ver']
  elif op == 'Print': 
    return opCode['Print']
  elif op == 'Read':
    return opCode['Read']
  elif op == 'AccessCol': 
    return opCode['AccessCol']
  elif op == 'AccessRow':
    return opCode['AccessRow']
  elif op == 'PrintCell':
    return opCode['PrintCell']
  elif op == 'PrintCol':
    return opCode['PrintCol']
  elif op == 'PrintHeaders':
    return opCode['PrintHeaders']
  elif op == 'PrintRow':
    return opCode['PrintRow']
  elif op == 'PrintTags':
    return opCode['PrintTags']

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