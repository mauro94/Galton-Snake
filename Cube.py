# Seamtnic Cube
# Patricio Sanchez A01191893
# Mauro Amarante A01191893

datatypes = {
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

cube = {}

# Assignment
cube['bool=bool'] = datatypes['bool']
cube['int=int'] = datatypes['int']
cube['int=float'] = datatypes['int']
cube['int=char'] = datatypes['int']
cube['float=float'] = datatypes['float']
cube['float=int'] = datatypes['float']
cube['char=char'] = datatypes['char']
cube['char=int'] = datatypes['char']
cube['string=string'] = datatypes['string']
cube['dataframe=dataframe'] = datatypes['dataframe']

# Sum
cube['int+int'] = datatypes['int']
cube['int+float'] = datatypes['float']
cube['int+char'] = datatypes['int']
cube['float+int'] = datatypes['float']
cube['float+float'] = datatypes['float']
cube['char+char'] = datatypes['int']
cube['char+int'] = datatypes['int']
cube['string+string'] = datatypes['string']

# Substraction
cube['int-int'] = datatypes['int']
cube['int-float'] = datatypes['float']
cube['int-char'] = datatypes['int']
cube['float-int'] = datatypes['float']
cube['float-float'] = datatypes['float']
cube['char-char'] = datatypes['int']
cube['char-int'] = datatypes['int']

# Multiplication
cube['int*int'] = datatypes['int']
cube['int*float'] = datatypes['float']
cube['int*char'] = datatypes['int']
cube['float*int'] = datatypes['float']
cube['float*float'] = datatypes['float']
cube['char*char'] = datatypes['int']
cube['char*int'] = datatypes['int']

# Divison
cube['int/int'] = datatypes['int']
cube['int/float'] = datatypes['float']
cube['int/char'] = datatypes['int']
cube['float/int'] = datatypes['float']
cube['float/float'] = datatypes['float']
cube['char/char'] = datatypes['int']
cube['char/int'] = datatypes['int']

# Less than
cube['int<int'] = datatypes['bool']
cube['int<float'] = datatypes['bool']
cube['int<char'] = datatypes['bool']
cube['float<int'] = datatypes['bool']
cube['float<float'] = datatypes['bool']
cube['char<char'] = datatypes['bool']
cube['char<int'] = datatypes['bool']

# Greater than
cube['int>int'] = datatypes['bool']
cube['int>float'] = datatypes['bool']
cube['int>char'] = datatypes['bool']
cube['float>int'] = datatypes['bool']
cube['float>float'] = datatypes['bool']
cube['char>char'] = datatypes['bool']
cube['char>int'] = datatypes['bool']

# Less than/equal
cube['int<=int'] = datatypes['bool']
cube['int<=float'] = datatypes['bool']
cube['int<=char'] = datatypes['int']
cube['float<=int'] = datatypes['bool']
cube['float<=float'] = datatypes['bool']
cube['char<=char'] = datatypes['bool']
cube['char<=int'] = datatypes['bool']

# Greater than/equal
cube['int>=int'] = datatypes['bool']
cube['int>=float'] = datatypes['bool']
cube['int>=char'] = datatypes['bool']
cube['float>=int'] = datatypes['bool']
cube['float>=float'] = datatypes['bool']
cube['char>=char'] = datatypes['bool']
cube['char>=int'] = datatypes['bool']

# Equal
cube['bool==bool'] = datatypes['bool']
cube['int==int'] = datatypes['bool']
cube['int==float'] = datatypes['bool']
cube['int==char'] = datatypes['bool']
cube['float==int'] = datatypes['bool']
cube['float==float'] = datatypes['bool']
cube['char==char'] = datatypes['bool']
cube['char==int'] = datatypes['bool']
cube['dataframe==dataframe'] = datatypes['bool']

# Not equal
cube['bool!=bool'] = datatypes['bool']
cube['int!=int'] = datatypes['bool']
cube['int!=float'] = datatypes['bool']
cube['int!=char'] = datatypes['bool']
cube['float!=int'] = datatypes['bool']
cube['float!=float'] = datatypes['bool']
cube['char!=char'] = datatypes['bool']
cube['char!=int'] = datatypes['bool']
cube['dataframe!=dataframe'] = datatypes['bool']

# And
cube['bool&&bool'] = datatypes['bool']

# Or
cube['bool||bool'] = datatypes['bool']

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

def getResultType(operand1, operand2, operator):
  one = getTypeString(operand1)
  two = getTypeString(operand2)
  op = operator

  result = one + op + two

  if not result in cube.keys():
    return -1
  else:
    return cube[result]