from Cube import *
from GaltonSnake import *
from Memory import *
from Functions import *
import csv

def execute (quadruples, globalVarCount, localVarCount, tempVarCount, constVarCount, constants, dataframes):
  # For testing purposes
  print 'Virtual Machine -----------------------------'

  # Memory map
  memory = Memory('memory', globalVarCount, localVarCount, tempVarCount, constVarCount)
  memory.initializeConstants(constants)

  # Create memory for main function
  try:
    main = memory.createActivationRecord(localVarCount['main'], tempVarCount['main'])
  except KeyError:
    print 'Main function not declared'
    exit(1)

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
    elif operator == 'Corr':
      print 'Correlate'

    elif operator == 'CorrHeaders':
      print 'Correlate headers'

    elif operator == 'RowBind':
       # Title of dataframe that gets data
      taker = memory.getValue(resultAddress)
      # Go to access col quad
      quad_count = quad_count + 1
      # Get access values
      q = quadruples[quad_count]
      # Get dataframe giving data
      giver = memory.getValue(q['operand1'])
      # Get the row number
      row_num = memory.getValue(q['result'])
      # Validate row size to see if it matches
      sizeOne = memory.getRowSize(taker, 1)
      row = memory.accessRow(giver, row_num, 1)
      if sizeOne == len(row):
        # BIND ROW
        memory.appendRow(taker, row, 1)
      else:
        print 'Row size does not match'
        exit(1)  

    elif operator == 'ColBind':
      # Title of dataframe that gets data
      taker = memory.getValue(resultAddress)
      # Go to access col quad
      quad_count = quad_count + 1
      # Get access values
      q = quadruples[quad_count]
      # Get dataframe giving data
      giver = memory.getValue(q['operand1'])
      # Get the col number
      col_num = memory.getValue(q['result'])
      # Validate column size to see if it matches
      sizeOne = memory.getColSize(taker, 1)
      column = memory.accessCol(giver, col_num, 1)
      if sizeOne == len(column):
        # BIND COLUMN
        memory.appendColumn(taker, column, 1)
      else:
        print 'Column size does not match'
        exit(1)        

# =========================================================
# Printing
# =========================================================

    elif operator == 'Print':
      value = memory.getValue(resultAddress)

      print(value)

    # Printing dataframes

    elif operator == 'PrintCol':
      # Go to access row quad
      quad_count = quad_count + 1
      # Get access values
      q = quadruples[quad_count]
      title = memory.getValue(q['operand1'])
      scope = 1
      # TODO: get column num based on headers of this df
      col_num = memory.getValue(q['result'])
      if isinstance(col_num, str):
        try:
          col_num = dataframes[title]['headers'].index(col_num)
        except ValueError:
          pass
      # Access row from memory
      column = memory.accessCol(title, col_num, scope)
      # Print
      print column

    elif operator == 'PrintRow':
      # Go to access row quad
      quad_count = quad_count + 1
      # Get access values
      q = quadruples[quad_count]
      title = memory.getValue(q['operand1'])
      scope = 1
      row_num = memory.getValue(q['result'])
      # Access row from memory
      row = memory.accessRow(title, row_num, scope)
      # Print
      print row

    elif operator == 'PrintDf':
      # Go to access data frame quad
      title = memory.getValue(resultAddress)
      scope = 1
      # Access whole df
      df = memory.accessDf(title, scope)
      # PRINT
      print df

    elif operator == 'PrintCell':
      # Go to access data frame quad
      # Get access values
      title = memory.getValue(leftOp)
      scope = 1
      row_col = memory.getValue(resultAddress)
      # Get real values
      row = row_col.split(',')[0][1:]
      col = row_col.split(',')[1][0:-1]
      row = memory.getValue(int(row))
      col = memory.getValue(int(col))
      # Access whole df
      cell = memory.accessCell(title, scope, row, col)
      # PRINT
      print cell    

    elif operator == 'PrintDfData':
      # Go to access data frame quad
      # Get access values
      title = memory.getValue(resultAddress)
      scope = 1
      # Access whole df
      data = memory.accessData(title, scope)
      # PRINT
      print data

    elif operator == 'PrintHeaders':
      # Get access values
      title = memory.getValue(resultAddress)
      scope = 1
      # Access whole df
      headers = memory.accessHeaders(title, scope)
      # PRINT
      print headers

    elif operator == 'PrintTags':
      # Get access values
      title = memory.getValue(resultAddress)
      scope = 1
      # Access whole df
      tags = memory.accessTags(title, scope)
      # PRINT
      print tags

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

# =========================================================
# Input
# =========================================================

    elif operator == 'Read':
      # Get filename
      filename = memory.getValue(resultAddress)
      title = memory.getValue(leftOp)
      scope = memory.getValue(rightOp)

      # Read csv file
      with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)

        row = reader.next()
        dataframes[title]['headers'] = row[1:]

        while True:
          try:
            row = reader.next()[1:]
            dataframes[title]['data'].append(row)
          except csv.Error:
            print "CSV error: error on creating dataframe"
          except StopIteration:
            break

      # Check if df is global or local
      memory.createDataframe(dataframes[scope][title], title)

# =========================================================
# Procedure end
# =========================================================
    elif operator == 'EndProc':
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