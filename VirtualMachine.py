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

  # Create memory for main function
  memory.createActivationRecord(localVarCount['main'], tempVarCount['main'])

  # Quadruple counter
  quad_count = 0

  # Pending quads
  pending_quads = []

  # Iterate all quadruples
  while (quad_count <= len(quadruples)):
    # Get current instruction
    q = quadruples[quad_count]

    # Get values of operands and result address
    leftOp = q['operand1']
    rightOp = q['operand2']
    resultAddress = q['result']
    operator = getOpString(q['operator'])

    print (q['operator'], leftOp, rightOp, resultAddress)

    # Arithmetic
    # Addition
    if operator == '+':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue + rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    # Substraction
    elif operator == '-':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue - rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    # Multiplication
    elif operator == '*':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue * rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    # Division
    elif operator == '/':
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
    elif operator == '=':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)

      # Store value in memory
      memory.setValue(leftOpValue, resultAddress)

    # Comparison
    # <, >, <=, >=, ==, !=, &&, ||
    elif operator == '<':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue < rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    elif operator == '>':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue > rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    elif operator == '<=':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue <= rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    elif operator == '>=':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue >= rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    elif operator == '==':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue == rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    elif operator == '!=':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue != rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    elif operator == '||':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue or rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    elif operator == '&&':
      # Get value from memory
      leftOpValue = memory.getValue(leftOp)
      rightOpValue = memory.getValue(rightOp)

      # Perform operation
      resultValue = leftOpValue and rightOpValue

      # Store value in memory
      memory.setValue(resultValue, resultAddress)

    #Arrays
    elif operator == 'Ver':
      value = memory.getValue(leftOp)
      lower_lim = memory.getValue(rightOp)
      upper_lim = memory.getValue(resultAddress)

      if between(value, lower_lim, upper_lim + 1):
        return True
      else:
        print('Index out of bounds')
        exit(1)

    # Printing
    elif operator == 'Print':
      value = memory.getValue(resultAddress)

      print(value)

    # Other operators
    # Param
    # elif operator == 'param':

    # Return
    # elif operator == 'Return':

    # GoSub
    elif operator == 'GoSub':
      # Push quadruple to temporal stack
      stackPush(pending_quads, quad_count + 1)
      # Modify quadruple counter to return to target quad
      quad_count = leftOp - 1

    # GotoF
    elif operator == 'GoToF':
      # Get conditional result
      result = memory.getValue(leftOp)
      # Get target quadruple
      target = resultAddress
      # Modify quadruple counter to return to target quad
      if not result:
        quad_count = target - 1

    # Goto
    elif operator == 'GoTo':
      # Get target quadruple
      target = resultAddress
      # Modify quadruple counter to return to target quad
      quad_count = target - 1

    # ERA
    elif operator == 'Era':
      # Create memory for any function
      memory.createActivationRecord(localVarCount[leftOp], tempVarCount[leftOp])

    # Read
    elif operator == 'Read':
      # Get filename
      filename = memory.getValue(resultAddress)

      # Read csv file
      with open(filename, 'rb') as csvfile:
        matrix = csv.reader(csvfile, delimiter=' ', quotechar='|')

      print matrix

    # TODO: check what matrix is and store in memory
    # TODO: generate memory for DF

    # ENDPROC
    elif operator == 'EndProc':
      # TODO: MANAGE RETURN OF INVESTMENT!!
      # INVEST IN MEMES!!
      memory.removeActivationRecord()
      quad_count = stackPop(pending_quads) - 1

    # END
    elif operator == 'End':
      memory.removeActivationRecord()
      exit(1)

    else:
      print operator
      print q['operator']
      print('Unknown operator')
      exit(1)

    quad_count += 1