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
      titleOne = memory.getValue(leftOp)
      titleTwo = memory.getValue(rightOp)
      one = memory.getDataframe(titleOne)
      two = memory.getDataframe(titleTwo)
      threshold = memory.getValue(resultAddress)

      # Fancy print
      print 'Correlate - ' + titleOne + ', ' + titleTwo

      # Correlation values acumulator
      totalCorrelation = 0

      if not len(one['data']) == len(two['data']):
        print 'Matrices need to have same number of columns for correlation to be calculated'
        exit(1)

      # Transpose matrix to get columns
      columnsOne = zip(*one['data'])
      columnsTwo = zip(*two['data'])

      # Iterate all columns to get correlations
      for i in range(len(columnsOne)):
        colOne = columnsOne[i]
        colTwo = columnsTwo[i]
        headOne = one['headers'][i]
        headTwo = two['headers'][i]
        correlateData(colOne, headOne, colTwo, headTwo, threshold)
        print ''

      # average = totalCorrelation/len(columnsOne)

      # if average > threshold:
      #   print 'Data is correlated, value: ' + str(average)
      # else:
      #   print 'Data is not correlated, value: ' + str(average)

    elif operator == 'CorrHeaders':
      titleOne = memory.getValue(leftOp)
      one = memory.getDataframe(titleOne)
      titleTwo = memory.getValue(rightOp)
      two = memory.getDataframe(titleTwo)
      threshold = memory.getValue(resultAddress)

      print 'Correlate Headers from: ' + titleOne + ', ' + titleTwo
      correlateHeaders(one['headers'], two['headers'], threshold)
      print ''

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
      # Validate column size to see if it matches
      sizeOne = memory.getColSize(taker, 1)
      sizeTwo = memory.getColSize(giver, 1)
      # Access Row to append
      row = memory.accessRow(giver, row_num, 1)
      # Check if size is the same
      if sizeOne == sizeTwo:
        # BIND ROW
        memory.appendRow(taker, row, 1)
      else:
        print 'Column size does not match, cannot bind row'
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
      # Validate row size to see if it matches
      sizeOne = memory.getRowSize(taker, 1)
      sizeTwo = memory.getRowSize(giver, 1)
      # Access column to append
      column = memory.accessCol(giver, col_num, 1)
      if sizeOne == sizeTwo:
        # BIND COLUMN
        memory.appendColumn(taker, column, 1)
      else:
        print 'Row size does not match, cannot bind column'
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
      scope = q['operand2']
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
      print 'Print Column ' + str(col_num) + ' from ' + title
      print column
      print ''

    elif operator == 'PrintRow':
      # Go to access row quad
      quad_count = quad_count + 1
      # Get access values
      q = quadruples[quad_count]
      title = memory.getValue(q['operand1'])
      scope = q['operand2']
      row_num = memory.getValue(q['result'])
      # Access row from memory
      row = memory.accessRow(title, row_num, scope)
      # Print
      print 'Print Row ' + str(row_num) + ' from ' + title
      print row
      print ''

    elif operator == 'PrintDf':
      # Go to access data frame quad
      title = memory.getValue(resultAddress)
      scope = q['operand2']
      # Access whole df
      df = memory.accessDf(title, scope)
      # PRINT
      print 'Printing dataframe'
      # Better printing
      print 'Title: ' + title
      print 'Headers: ', df['headers']
      print 'Tags: ',
      for key in df['tags']:
        print key,
      print ''
      print 'Data:'
      for i in df['data']:
        for j in i:
          print j, '\t',
        print ''
      print ''

    elif operator == 'PrintCell':
      # Go to access data frame quad
      # Get access values
      title = memory.getValue(leftOp)
      scope = q['operand2']
      row_col = memory.getValue(resultAddress)
      # Get real values
      row = row_col.split(',')[0][1:]
      col = row_col.split(',')[1][0:-1]
      row = memory.getValue(int(row))
      col = memory.getValue(int(col))
      # Access whole df
      cell = memory.accessCell(title, scope, row, col)
      # PRINT
      print 'Print Cell [' + str(row) + ', ' + str(col) + '] from ' + title
      print cell 
      print ''   

    elif operator == 'PrintDfData':
      # Go to access data frame quad
      # Get access values
      title = memory.getValue(resultAddress)
      scope = q['operand2']
      # Access whole df
      data = memory.accessData(title, scope)
      # PRINT
      print 'Print Data from ' + title
      for i in data:
        for j in i:
          print j, '\t',
        print ''
      print ''

    elif operator == 'PrintHeaders':
      # Get access values
      title = memory.getValue(resultAddress)
      scope = q['operand2']
      # Access whole df
      headers = memory.accessHeaders(title, scope)
      # PRINT
      print 'Headers from ' + title
      print headers

    elif operator == 'PrintTags':
      # Get access values
      title = memory.getValue(resultAddress)
      scope = q['operand2']
      # Access whole df
      tags = memory.accessTags(title, scope)
      # PRINT
      print 'Tags from ' + title
      print tags
      print ''
      
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
        dataframes[scope][title]['headers'] = row[1:]

        while True:
          try:
            row = reader.next()[1:]
            dataframes[scope][title]['data'].append(row)
          except csv.Error:
            print "CSV error: error on creating dataframe"
          except StopIteration:
            break

      # Check if df is global or local
      memory.createDataframe(dataframes[scope][title], scope, title)

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
      print('Unknown operator')
      exit(1)

    quad_count += 1