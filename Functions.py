# Additional Compiler Functions
# Patricio Sanchez A01191893
# Mauro Amarante A01191893

# -------------------------- INCLUDES ----------------------------------
from Correlation import *
from numbers import Number

# -------------------------- STACK OPERATIONS --------------------------
def stackTop(stack):
	global operands, types, operators
	if len(stack) > 0:
		x = stack[-1]
	else:
		x = None
	return x

def stackPush(stack, x):
	global operands, types, operators
	stack.append(x)

def stackPop(stack):
	global operands, types, operators
	if len(stack) > 0:
		x = stack.pop()
	else:
		x = None
	return x


# -------------------------- QUADRUPLES OPERATIONS --------------------------
def newQuadruple(list, operator, operand1, operand2, result):
	global quadruples
	list.append({'operator':operator, 'operand1':operand1, 'operand2':operand2, 'result':result})

# -------------------------- MEMORY FUNCTIONS -------------------------------
def getInitDir(scope, varType):
	# Globals
	if scope == 'global' and varType == 'bool':
		return 10000
	elif scope == 'global' and varType == 'int':
		return 12000
	elif scope == 'global' and varType == 'float':
		return 14000
	elif scope == 'global' and varType == 'string':
		return 16000
	elif scope == 'global' and varType == 'dataframe':
		return 20000
	# Local
	if scope == 'local' and varType == 'bool':
		return 40000
	elif scope == 'local' and varType == 'int':
		return 42000
	elif scope == 'local' and varType == 'float':
		return 44000
	elif scope == 'local' and varType == 'string':
		return 46000
	elif scope == 'local' and varType == 'dataframe':
		return 50000
	# Temp
	if scope == 'temp' and varType == 'bool':
		return 60000
	elif scope == 'temp' and varType == 'int':
		return 62000
	elif scope == 'temp' and varType == 'float':
		return 64000
	elif scope == 'temp' and varType == 'string':
		return 66000
	elif scope == 'temp' and varType == 'dataframe':
		return 70000
	# Constant
	if scope == 'constant' and varType == 'bool':
		return 80000
	elif scope == 'constant' and varType == 'int':
		return 82000
	elif scope == 'constant' and varType == 'float':
		return 84000
	elif scope == 'constant' and varType == 'string':
		return 86000
		
def getType (address, scope):
  if scope == 'global':
    if between(address, getInitDir('global','bool'), getInitDir('global','int')):
      return 'bool'
    elif between(address, getInitDir('global','int'), getInitDir('global','float')):
      return 'int'
    elif between(address, getInitDir('global','float'), getInitDir('global','string')):
      return 'float'
    elif between(address, getInitDir('global','string'), getInitDir('global','dataframe')):
      return 'string'
    elif between(address, getInitDir('global','dataframe'), getInitDir('local','bool')):
      return 'dataframe'
  elif scope == 'local':
    if between(address, getInitDir('local','bool'), getInitDir('local','int')):
      return 'bool'
    elif between(address, getInitDir('local','int'), getInitDir('local','float')):
      return 'int'
    elif between(address, getInitDir('local','float'), getInitDir('local','string')):
      return 'float'
    elif between(address, getInitDir('local','string'), getInitDir('local','dataframe')):
      return 'string'
    elif between(address, getInitDir('local','dataframe'), getInitDir('temp','bool')):
      return 'dataframe'
  elif scope == 'temp':
    if between(address, getInitDir('temp','bool'), getInitDir('temp','int')):
      return 'bool'
    elif between(address, getInitDir('temp','int'), getInitDir('temp','float')):
      return 'int'
    elif between(address, getInitDir('temp','float'), getInitDir('temp','string')):
      return 'float'
    elif between(address, getInitDir('temp','string'), getInitDir('temp','dataframe')):
      return 'string'
    elif between(address, getInitDir('temp','dataframe'), getInitDir('constant','bool')):
      return 'dataframe'
  elif scope == 'constant':
    if between(address, getInitDir('constant','bool'), getInitDir('constant','int')):
      return 'bool'
    elif between(address, getInitDir('constant','int'), getInitDir('constant','float')):
      return 'int'
    elif between(address, getInitDir('constant','float'), getInitDir('constant','string')):
      return 'float'
    elif between(address, getInitDir('constant', 'string'), 100000):
      return 'string'

def getScope (address):
  if between(address, getInitDir('global', 'bool'), getInitDir('local','bool')):
    return 'global'
  elif between(address, getInitDir('local', 'bool'), getInitDir('temp','bool')):
    return 'local'
  elif between(address, getInitDir('temp', 'bool'), getInitDir('constant','bool')):
    return 'temp'
  elif between(address, getInitDir('constant', 'bool'), 100000):
    return 'constant'
  else:
    print('Address non existent')
    exit(1)

def between (value, low, high):
  return (low <= value < high)

def between_inclusive(value, low, high):
  return (low <= value <= high)

# -------------------------- DATAFRAME FUNCTIONS ----------------------------
def column(dataframe, column):
    return [row[column] for row in dataframe]

# =========================================================
# CORRELATIONS
# =========================================================
def correlateHeaders(headsOne, headsTwo, threshold):
  if headsOne == headsTwo:
    print 'Same headers, perfect correlation'
  else:
    # Correlation check of words, using a pool based method
    one = beginCheck(headsOne)
    two = beginCheck(headsTwo)
    # Divide weights obtained to find possible correlation
    divide = []
    for i in range(len(one)):
      if two[i] == 0 or one[i] == 0:
        divide[i] = 0
      else:
        divide[i] = max((float(one[i])/two[i]), (float(two[i])/one[i]))

    if max(divide) >= threshold:
      print 'Success, correlated, value: ' + str(max(divide))
    else:
      print 'Failure, not correlated, value ' + str(max(divide))

def correlateData(columnOne, headerOne, columnTwo, headerTwo, threshold):
  if not between_inclusive(threshold, 0, 1):
    print 'Correlation threshold must be between 0 and 1'
    exit(1)

  if columnOne == columnTwo:
    correlationPrint(headerOne, headerTwo, 1)
    return 1
  elif isinstance(columnOne[0], numbers.Number) or isinstance(columnTwo[0], numbers.Number):
    # Get averages
    meanOne = float(sum(columnOne))/len(columnOne)
    meanTwo = float(sum(columnTwo))/len(columnTwo)
    # Substract averages
    subsOne = list(map(lambda x: x - meanOne, columnOne))
    subsTwo = list(map(lambda x: x - meanTwo, columnTwo))
    # Calculate subsOne * subsTwo
    multiply = list(map(lambda x,y: x * y, subsOne, subsTwo))
    # Calculate subsOne squared
    squareOne = list(map(lambda x: x**2, subsOne))
    # Calcuate subsTwo squared
    squareTwo = list(map(lambda x: x**2, subsTwo))
    # Calculate correlation
    temp = sqrt(float(squareOne) * squareTwo)
    corr = float(multiply)/temp
    # Nice print
    correlationPrint(headerOne, headerTwo, corr)
    return corr
  else:
    print 'Columns must be numeric, skipping correlation of: ' + headerOne + ', ' + headerTwo

# =========================================================
# SPECIAL PRINTS
# =========================================================

def correlationPrint(headOne, headTwo, corr):
  if corr == 1:
    print 'Perfect positive correlation between ' + headOne + ', ' + headTwo
  elif corr == -1:
    print 'Perfect negative correlation between ' + headOne + ', ' + headTwo
  else:
    print 'Correlation value = ' + str(corr) + ' between ' + headOne + ', ' + headTwo