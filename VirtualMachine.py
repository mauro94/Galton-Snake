from Cube import *
from GaltonSnake import *
from Memory import *
import csv

def virtualMachine (functions, quadruples, global_variables, local_variables, temp_variables, const_variables):
  # Memory stuff

  # Quadruple counter
  quad_count = 0

  # Iterate all quadruples
  while (quad_count <= len(quadruples)):
    # Get current instruction
    q = quadruples[quad_count]

    # Get values of operands and result address
    leftOp = q['operand1']
    rightOp = q['operand2']
    resultAddress = q['resultAddress']

    # Arithmetic
    # Addition
    if q['operator'] == '+':
      # Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue + rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    # Substraction
    elif q['operator'] == '-':
      # Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue - rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    # Multiplication
    elif q['operator'] == '*':
      # Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue * rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    # Division
    elif q['operator'] == '/':
      # Get value from memory
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
      # Get value from memory
      leftOpValue = getValue(leftOp)

      # Store value in memory
      setValue(leftOpValue, resultAddress)

    # Comparison
    # <, >, <=, >=, ==, !=, &&, ||
    elif q['operator'] == '<':
      # Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue < rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '>':
      # Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue > rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '<=':
      # Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue <= rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '>=':
      # Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue >= rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '==':
      # Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue == rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '!=':
      # Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue != rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '||':
      # Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue or rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    elif q['operator'] == '&&':
      # Get value from memory
      leftOpValue = getValue(leftOp)
      rightOpValue = getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue and rightOpValue

      # Store value in memory
      setValue(resultValue, resultAddress)

    #Arrays
    elif q['operator'] == 'Ver':
      value = getValue(leftOp)
      lower_lim = getValue(rightOp)
      upper_lim = getValue(resultAddress)

      if between(value, lower_lim, upper_lim + 1):
        return True
      else:
        print('Index out of bounds')
        exit(1)

    # Printing
    elif q['operator'] == 'print':
      leftOpValue = getValue(leftOp)

      print(leftOpValue)

    # Other operators
    # Param
    # elif q['operator'] == 'param':

    # Return
    # elif q['operator'] == 'Return':

    # GoSub
    elif q['operator'] == 'GoSub':
      # Get target quadruple
      target = resultAddress
      # Modify quadruple counter to return to target quad
      quad_count = target - 1

    # GotoF
    elif q['operator'] == 'GoToF':
      # Get conditional result
      result = getValue(leftOp)
      # Get target quadruple
      target = resultAddress
      # Modify quadruple counter to return to target quad
      if result:
        quad_count = target - 1

    # Goto
    elif q['operator'] == 'GoTo':
      # Get target quadruple
      target = resultAddress
      # Modify quadruple counter to return to target quad
      quad_count = target - 1

    # ERA
    # elif q['operator'] == 'era':
    # TODO: create memory of new function
    # TODO: check if there is existing memory of !main function

    # Read
    elif q['operator'] == 'read':
      # Get filename
      filename = getValue(resultAddress)

      # Read csv file
      with open(filename, 'rb') as csvfile:
        matrix = csv.reader(csvfile, delimiter=' ', quotechar='|')

      print matrix

      # TODO: check what matrix is and store in memory
      # TODO: generate memory for DF

    # ENDPROC
    # elif q['operator'] == 'EndProc':

    # END
    # elif q['operator'] == 'End'

    else:
      print('Unknown operator')
      exit(1)

    quad_count += 1

# Temporary functions
# This will be implemented in memory
def getValue(address):
  print(address)

def setValue(value, address):
  print(value)
  print(address)