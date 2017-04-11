from Cube import *
from GaltonSnake import *
from Memory import *

def virtualMachine (functions, quadruples, global_variables, local_variables, temp_variables, const_variables):
  #Memory stuff

  for q in quadruples:
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