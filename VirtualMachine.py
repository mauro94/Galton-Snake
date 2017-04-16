from Cube import *
from GaltonSnake import *
from Memory import *

def virtualMachine (functions, quadruples, global_variables, local_variables, temp_variables, const_variables):
  #Memory stuff

  for q in quadruples:
    #Arithmetic
    # Addition
    if q['operator'] == '+':
      leftOperand = q['operand1']
      rightOperand = q['operand2']
      result = q['result']

      # Store value in memory

    # Substraction
    elif q['operator'] == '-':
      leftOperand = q['operand1']
      rightOperand = q['operand2']
      result = q['result']

      # Store value in memory

    # Multiplication
    elif q['operator'] == '*':
      leftOperand = q['operand1']
      rightOperand = q['operand2']
      result = q['result']

      # Store value in memory

    # Division
    elif q['operator'] == '/':
      leftOperand = q['operand1']
      rightOperand = q['operand2']
      result = q['result']

      # Store value in memory

    # Assignment
    elif q['operator'] == '=':
      leftOperand = q['operand1']
      result = q['result']

      # Store value in memory

    # Comparison
    # <, >, <=, >=, ==, !=, &&, ||
    elif q['operator'] == '<':
      leftOperand = q['operand1']
      rightOperand = q['operand2']
      result = q['result']

    elif q['operator'] == '>':
      leftOperand = q['operand1']
      rightOperand = q['operand2']
      result = q['result']

    elif q['operator'] == '<=':
      leftOperand = q['operand1']
      rightOperand = q['operand2']
      result = q['result']

    elif q['operator'] == '>=':
      leftOperand = q['operand1']
      rightOperand = q['operand2']
      result = q['result']

    elif q['operator'] == '==':
      leftOperand = q['operand1']
      rightOperand = q['operand2']
      result = q['result']

    elif q['operator'] == '!=':
      leftOperand = q['operand1']
      rightOperand = q['operand2']
      result = q['result']

    elif q['operator'] == '||':
      leftOperand = q['operand1']
      rightOperand = q['operand2']
      result = q['result']

    elif q['operator'] == '&&':
      leftOperand = q['operand1']
      rightOperand = q['operand2']
      result = q['result']

    # Other operators
    # Param
    elif q['operator'] == 'param':
      leftOperand = q['operand1']
      result = q['result']

    # Return
    elif q['operator'] == 'Return':
      leftOperand = q['operand1']
      result = q['result']

    # GoSub
    elif q['operator'] == 'GoSub':
      leftOperand = q['operand1']

    # GotoF
    elif q['operator'] == 'GoToF':
      leftOperand = q['operand1']
      result = q['result']

    # Goto
    elif q['operator'] == 'GoTo':
      result = q['result']

    # ERA
    elif q['operator'] == 'era':
      leftOperand = q['operand1']

    # Print
    # elif q['operator'] == 'print'

    # Read
    # elif q['operator'] == 'read'

    # ENDPROC
    elif q['operator'] == 'EndProc':

    # END
    # elif q['operator'] == 'End'