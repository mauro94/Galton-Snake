from Cube import *
from GaltonSnake import *
from Memory import *

def virtualMachine (functions, quadruples, global_variables, local_variables, temp_variables, const_variables):
  #Memory stuff

  for q in quadruples:
    #Arithmetic
    # Addition
    if q['operator'] == '+':
      leftOpAddress = q['operand1']
      rightOpAddress = q['operand2']
      resultAddress = q['resultAddress']

      #Get value from memory
      leftOpValue = getValue(leftOpAddress)
      rightOpValue = getValue(rightOpAddress)

      # Perform operation
      resultValue = leftOpValue + rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    # Substraction
    elif q['operator'] == '-':
      leftOpAddress = q['operand1']
      rightOpAddress = q['operand2']
      resultAddress = q['resultAddress']

      #Get value from memory
      leftOpValue = getValue(leftOpAddress)
      rightOpValue = getValue(rightOpAddress)

      # Perform operation
      resultValue = leftOpValue - rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    # Multiplication
    elif q['operator'] == '*':
      leftOpAddress = q['operand1']
      rightOpAddress = q['operand2']
      resultAddress = q['resultAddress']

      #Get value from memory
      leftOpValue = getValue(leftOpAddress)
      rightOpValue = getValue(rightOpAddress)

      # Perform operation
      resultValue = leftOpValue * rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    # Division
    elif q['operator'] == '/':
      leftOpAddress = q['operand1']
      rightOpAddress = q['operand2']
      resultAddress = q['resultAddress']

      #Get value from memory
      leftOpValue = getValue(leftOpAddress)
      rightOpValue = getValue(rightOpAddress)

      # Perform operation
      if rightOpValue != 0:
        resultValue = leftOpValue / rightOpValue

        # Store value in memory
        setValue(resultValue, resultAddress)

      else:
        print('Division by 0')
        exit(1)

    # Assignment
    elif q['operator'] == '=':
      leftOpAddress = q['operand1']
      resultAddress = q['resultAddress']

      #Get value from memory
      leftOpValue = getValue(leftOpAddress)

      # Store value in memory
      setValue(leftOpValue, resultAddress)

    # Comparison
    # <, >, <=, >=, ==, !=, &&, ||
    elif q['operator'] == '<':
      leftOpAddress = q['operand1']
      rightOpAddress = q['operand2']
      resultAddress = q['resultAddress']

      #Get value from memory
      leftOpValue = getValue(leftOpAddress)
      rightOpValue = getValue(rightOpAddress)

      # Perform operation
      resultValue = leftOpValue < rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '>':
      leftOpAddress = q['operand1']
      rightOpAddress = q['operand2']
      resultAddress = q['resultAddress']

      #Get value from memory
      leftOpValue = getValue(leftOpAddress)
      rightOpValue = getValue(rightOpAddress)

      # Perform operation
      resultValue = leftOpValue > rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '<=':
      leftOpAddress = q['operand1']
      rightOpAddress = q['operand2']
      resultAddress = q['resultAddress']

      #Get value from memory
      leftOpValue = getValue(leftOpAddress)
      rightOpValue = getValue(rightOpAddress)

      # Perform operation
      resultValue = leftOpValue <= rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '>=':
      leftOpAddress = q['operand1']
      rightOpAddress = q['operand2']
      resultAddress = q['resultAddress']

      #Get value from memory
      leftOpValue = getValue(leftOpAddress)
      rightOpValue = getValue(rightOpAddress)

      # Perform operation
      resultValue = leftOpValue >= rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '==':
      leftOpAddress = q['operand1']
      rightOpAddress = q['operand2']
      resultAddress = q['resultAddress']

      #Get value from memory
      leftOpValue = getValue(leftOpAddress)
      rightOpValue = getValue(rightOpAddress)

      # Perform operation
      resultValue = leftOpValue == rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '!=':
      leftOpAddress = q['operand1']
      rightOpAddress = q['operand2']
      resultAddress = q['resultAddress']

      #Get value from memory
      leftOpValue = getValue(leftOpAddress)
      rightOpValue = getValue(rightOpAddress)

      # Perform operation
      resultValue = leftOpValue != rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '||':
      #Get value from memory
      leftOpValue = getValue(leftOpAddress)
      rightOpValue = getValue(rightOpAddress)

      # Perform operation
      resultValue = leftOpValue or rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '&&':
      #Get value from memory
      leftOpValue = getValue(leftOpAddress)
      rightOpValue = getValue(rightOpAddress)

      # Perform operation
      resultValue = leftOpValue and rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    # Other operators
    # Param
    elif q['operator'] == 'param':
      leftOpAddress = q['operand1']
      resultAddress = q['resultAddress']

    # Return
    elif q['operator'] == 'Return':
      leftOpAddress = q['operand1']
      resultAddress = q['resultAddress']

    # GoSub
    elif q['operator'] == 'GoSub':
      leftOpAddress = q['operand1']

    # GotoF
    elif q['operator'] == 'GoToF':
      leftOpAddress = q['operand1']
      resultAddress = q['resultAddress']

    # Goto
    elif q['operator'] == 'GoTo':
      resultAddress = q['resultAddress']

    # ERA
    elif q['operator'] == 'era':
      leftOpAddress = q['operand1']

    # Print
    # elif q['operator'] == 'print'

    # Read
    # elif q['operator'] == 'read'

    # ENDPROC
    elif q['operator'] == 'EndProc':

    # END
    # elif q['operator'] == 'End'

# Temporary functions
# This will be implemented in memory
def getValue(address):
  print(address)

def setValue(value, address):
  print(value)
  print(address)