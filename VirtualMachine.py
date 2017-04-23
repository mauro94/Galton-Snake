from Cube import *
from GaltonSnake import *
from Memory import *

def virtualMachine (functions, quadruples, global_variables, local_variables, temp_variables, const_variables):
  # Memory stuff

  # Iterate all quadruples
  for q in quadruples:
    # Get values of operands and result address
    leftOp = q['operand1']
    rightOp = q['operand2']
    resultAddress = q['resultAddress']

    #Arithmetic
    # Addition
    if q['operator'] == '+':
      #Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue + rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    # Substraction
    elif q['operator'] == '-':
      #Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue - rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    # Multiplication
    elif q['operator'] == '*':
      #Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue * rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    # Division
    elif q['operator'] == '/':
      #Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

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
      #Get value from memory
      leftOpValue = getValue(leftOp)

      # Store value in memory
      setValue(leftOpValue, resultAddress)

    # Comparison
    # <, >, <=, >=, ==, !=, &&, ||
    elif q['operator'] == '<':
      #Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue < rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '>':
      #Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue > rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '<=':
      #Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue <= rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '>=':
      #Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue >= rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '==':
      #Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue == rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '!=':
      #Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue != rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '||':
      #Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue or rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '&&':
      #Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue and rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    # Other operators
    # Param
    elif q['operator'] == 'param':

    # Return
    elif q['operator'] == 'Return':

    # GoSub
    elif q['operator'] == 'GoSub':

    # GotoF
    elif q['operator'] == 'GoToF':

    # Goto
    elif q['operator'] == 'GoTo':

    # ERA
    elif q['operator'] == 'era':

    # Print
    # elif q['operator'] == 'print'

    # Read
    # elif q['operator'] == 'read'

    # ENDPROC
    elif q['operator'] == 'EndProc':

    # END
    # elif q['operator'] == 'End'

    else:
      print('Unknown operator')
      exit(1)

# Temporary functions
# This will be implemented in memory
def getValue(address):
  print(address)

def setValue(value, address):
  print(value)
  print(address)