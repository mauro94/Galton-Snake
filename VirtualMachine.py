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
  main = memory.createActivationRecord(localVarCount['main'], tempVarCount['main'])
  memory.changeActivationRecord(main)

  # Quadruple counter
  quad_count = 0

  # Pending quads
  pending_quads = []

  # Pending return value
  return_value = 0

  # Call stack
  call_stack = []

  # Iterate all quadruples
  while (quad_count < len(quadruples)):
    # Get current instruction
    q = quadruples[quad_count]

    # Get values of operands and result address
    leftOp = q['operand1']
    rightOp = q['operand2']
    resultAddress = q['result']
    operator = getOpString(q['operator'])

    # print (q['operator'], leftOp, rightOp, resultAddress)

# =========================================================
# Arithmetic
# =========================================================
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

# =========================================================
# Comparison
# =========================================================

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

# =========================================================
# Arrays
# =========================================================

    elif operator == 'Ver':
      value = memory.getValue(leftOp)
      lower_lim = rightOp
      upper_lim = resultAddress

      if not between(value, lower_lim, upper_lim + 1):
        print('Index out of bounds')
        exit(1)

# =========================================================
# Dataframes
# =========================================================

    # Correlations
    elif operator == 'Correlate':
      print 'Correlate'

    elif operator == 'Corr_Headers':
      print 'Correlate headers'

# =========================================================
# Printing
# =========================================================

    elif operator == 'Print':
      value = memory.getValue(resultAddress)

      print(value)

    # Printing dataframes

    elif operator == 'Print_Col':
      print 'Col'

    elif operator == 'Print_Row':
      print 'Row'

    elif operator == 'Print_DF':
      print 'Dataframe'

    elif operator == 'Print_Cell':
      print 'Print_Cell'

    elif operator == 'Print_Data':
      print 'Print_Data'

    elif operator == 'Print_Headers':
      print 'Print_Headers'

    elif operator == 'Print_Tags':
      print 'Print_Tags'

# =========================================================
# Functions
# =========================================================

    # Param
    elif operator == 'Param':
      # Get value from current mem stack
      value = memory.getValue(leftOp)
      # HACKY AF
      stackPush(memory.memory_stack, stackTop(call_stack))
      memory.setValue(value, resultAddress)
      stackPop(memory.memory_stack)

    # Return
    elif operator == 'Return':
      # Temporal return value
      return_value = memory.getValue(resultAddress)
      # Remove activation record
      memory.removeActivationRecord()
      # Get to return assign quad
      quad_count = stackPop(pending_quads)
      # Assign value
      # Get current instruction
      q = quadruples[quad_count]
      # Get values of operands and result address
      resultAddress = q['result']
      memory.setValue(return_value, resultAddress)

    # GoSub
    elif operator == 'GoSub':
      # Push quadruple to temporal stack
      stackPush(pending_quads, quad_count + 1)
      # Modify quadruple counter to return to target quad
      quad_count = leftOp - 1
      # Change activation record
      ar = stackPop(call_stack)
      stackPush(memory.memory_stack, ar)

# =========================================================
# Go To operators
# =========================================================

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

# =========================================================
# Memory
# =========================================================
    elif operator == 'Era':
      # Create memory for any function
      ar = memory.createActivationRecord(localVarCount[leftOp], tempVarCount[leftOp])
      # Push to call stack
      stackPush(call_stack, ar)

    elif operator == 'Prep':
      # Create memory for dataframe
      # TODO: get dataframe info
      # DATAFRAMES!!
      print 'Prep'


# =========================================================
# Input
# =========================================================

    elif operator == 'Read':
      # Get filename
      filename = memory.getValue(resultAddress)

      # Read csv file
      with open(filename, 'rb') as csvfile:
        matrix = csv.reader(csvfile, delimiter=' ', quotechar='|')

      print matrix

      # Add every column to a new matrix element
      # for m in matrix:


    # TODO: check what matrix is and store in memory
    # TODO: generate memory for DF

# =========================================================
# Procedure end
# =========================================================
    elif operator == 'EndProc':
      memory.removeActivationRecord()
      quad_count = stackPop(pending_quads) - 1

    # END
    elif operator == 'End':
      memory.removeActivationRecord()
      # exit(1)

    else:
      print operator
      print q['operator']
      print('Unknown operator')
      exit(1)

    quad_count += 1