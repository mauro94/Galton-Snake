#Cubo Semantico
# Patricio Sanchez A01191893
# Mauro Amarante A01191893

datatypes = {
  'void':0,
  'bool':1,
  'boolArray':11,
  'int':2,
  'intArray':22,
  'float':3
  'floatArray':33,
  'char':4,
  'string':44,
  'dataframe':5
}

cube = {}

#Asignar
cube['bool=bool'] = datatypes['bool']
cube['int=int'] = datatypes['int']
#cube['float=int'] = datatypes['float']
#cube['int=float'] = datatypes['int']
cube['float=float'] = datatypes['float']
cube['char=char'] = datatypes['char']
cube['dataframe=dataframe'] = datatypes['dataframe']

#Suma
cube['int+int'] = datatypes['int']
cube['float+int'] = datatypes['float']
cube['int+float'] = datatypes['float']
cube['float+float'] = datatypes['float']
#cube['char+char'] = datatypes['int']

#Resta
cube['int-int'] = datatypes['int']
cube['float-int'] = datatypes['float']
cube['int-float'] = datatypes['float']
cube['float-float'] = datatypes['float']
#cube['char-char'] = datatypes['int']

#Multiplicación
cube['int*int'] = datatypes['int']
cube['float*int'] = datatypes['float']
cube['int*float'] = datatypes['float']
cube['float*float'] = datatypes['float']

#Divisón
cube['int/int'] = datatypes['int']
cube['float/int'] = datatypes['float']
cube['int/float'] = datatypes['float']
cube['float/float'] = datatypes['float']

#Menor que
cube['int<int'] = datatypes['bool']
cube['float<int'] = datatypes['bool']
cube['int<float'] = datatypes['bool']
cube['float<float'] = datatypes['bool']
cube['char<char'] = datatypes['bool']

#Mayor que
cube['int>int'] = datatypes['bool']
cube['float>int'] = datatypes['float']
cube['int>float'] = datatypes['bool']
cube['float>float'] = datatypes['bool']
cube['char>char'] = datatypes['bool']

#Menor igual
cube['int<=int'] = datatypes['bool']
cube['float<=int'] = datatypes['bool']
cube['int<=float'] = datatypes['bool']
cube['float<=float'] = datatypes['bool']
cube['char<=char'] = datatypes['bool']

#Mayor igual
cube['int>=int'] = datatypes['bool']
cube['float>=int'] = datatypes['bool']
cube['int>=float'] = datatypes['bool']
cube['float>=float'] = datatypes['bool']
cube['char>=char'] = datatypes['bool']

#Comparación
cube['bool==bool'] = datatypes['bool']
cube['int==int'] = datatypes['bool']
cube['float==int'] = datatypes['bool']
cube['int==float'] = datatypes['bool']
cube['float==float'] = datatypes['bool']
cube['char==char'] = datatypes['bool']
cube['dataframe==dataframe'] = datatypes['bool']

#No Igual
cube['bool!=bool'] = datatypes['bool']
cube['int!=int'] = datatypes['bool']
cube['float!=int'] = datatypes['bool']
cube['int!=float'] = datatypes['bool']
cube['float!=float'] = datatypes['bool']
cube['char!=char'] = datatypes['bool']
cube['dataframe!=dataframe'] = datatypes['bool']

def typeString (type):
  if type == 1:
    return 'bool'
  else if type == 2: 
    return 'int'
  else if type == 3:
    return 'float'
  else if type == 4:
    return 'char'
  else if type == 5:
    return 'dataframe'

def getType(operand1, operand2, operator):
  one = typeString(operand1)
  two = typeString(operand2)
  op = typeString(operator)
  return cube[one+op+two]