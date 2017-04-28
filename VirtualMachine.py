from Cube import *
from GaltonSnake import *
from Memory import *
from Functions import *
import csv

def execute (quadruples, globalVarCount, localVarCount, tempVarCount, constVarCount, constants):
  # For testing purposes
  print 'Virtual Machine -----------------------------'

  # Memory map
  memory = Memory('memory', globalVarCount, localVarCount, tempVarCount, constVarCount)
  memory.initializeConstants(constants)

  # TODO: Initialize AR - main
  # Push to stack

  # Quadruple counter
  quad_count = 0

  # Iterate all quadruples
  while (quad_count <= len(quadruples)):
    # Get current instruction
    q = quadruples[quad_count]

    # Get values of operands and result address
    leftOp = q['operand1']
    rightOp = q['operand2']
    resultAddress = q['result']
    operator = getOperation(q['operator'])

    # print (q['operator'], leftOp, rightOp, resultAddress)

    # Arithmetic
    # Addition
    if q['operator'] == '+':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue + rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    # Substraction
    elif q['operator'] == '-':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue - rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    # Multiplication
    elif q['operator'] == '*':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue * rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    # Division
    elif q['operator'] == '/':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      if rightOpValue != 0:
        resultValue = leftOpValue / rightOpValue

        # Store value in memory
        memory.setValue(resultValue, resultAddress)

      else:
        print('Division by 0')
        exit(1)

    # Assignment
    elif q['operator'] == '=':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)

      # Store value in memory
      memory.setValue(leftOpValue, resultAddress)

    # Comparison
    # <, >, <=, >=, ==, !=, &&, ||
    elif q['operator'] == '<':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue < rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    elif q['operator'] == '>':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue > rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    elif q['operator'] == '<=':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue <= rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    elif q['operator'] == '>=':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue >= rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    elif q['operator'] == '==':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue == rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    elif q['operator'] == '!=':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue != rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    elif q['operator'] == '||':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue or rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    elif q['operator'] == '&&':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue and rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    #Arrays
    elif q['operator'] == 'Ver':
      value = memory.getValue(leftOp)
      lower_lim = memory.getValue(rightOp)
      upper_lim = memory.getValue(resultAddress)

      if between(value, lower_lim, upper_lim + 1):
        return True
      else:
        print('Index out of bounds')
        exit(1)

    # Printing
    elif q['operator'] == 'print':
      value = memory.getValue(resultAddress)

      print(value)

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
      result = memory.getValue(leftOp)
      # Get target quadruple
      target = resultAddress
      # Modify quadruple counter to return to target quad
      if not result:
        quad_count = target - 1

    # Goto
    elif q['operator'] == 'GoTo':
      # Get target quadruple
      target = resultAddress
      # Modify quadruple counter to return to target quad
      quad_count = target - 1

    # ERA
    # elif q['operator'] == 'era':
    # TODO: create AR of new function
    # TODO: push to stack

    # Read
    elif q['operator'] == 'read':
      # Get filename
      filename = memory.getValue(resultAddress)

      # Read csv file
      with open(filename, 'rb') as csvfile:
        matrix = csv.reader(csvfile, delimiter=' ', quotechar='|')

      print matrix

    # TODO: check what matrix is and store in memory
    # TODO: generate memory for DF

    # ENDPROC
    # elif q['operator'] == 'EndProc':

    # END
    elif q['operator'] == 'end':
      # TODO: check if anything else is needed here
      exit(1)

    else:
      print('Unknown operator')
      exit(1)

    quad_count += 1