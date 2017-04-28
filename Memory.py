from Cube import *
from GaltonSnake import *
from VirtualMachine import *
from Functions import *

class Memory:
  """docstring for Memory"""
  def __init__(self, name, global_variables, local_variables, temp_variables, const_variables):
    # Name for the memory object
    self.name = name

    # Creating lists with the amount of variables needed to be stored
    # Global variables
    self.global_bools      = range(global_variables['bool'] - getInitDir('global', 'bool'))
    self.global_ints       = range(global_variables['int'] - getInitDir('global', 'int'))
    self.global_floats     = range(global_variables['float'] - getInitDir('global', 'float'))
    self.global_strings    = range(global_variables['string'] - getInitDir('global', 'string'))
    self.global_dataframes = range(global_variables['dataframe'] - getInitDir('global', 'dataframe'))

    # Constants
    self.const_bools      = range(const_variables['bool'] - getInitDir('constant', 'bool'))
    self.const_ints       = range(const_variables['int'] - getInitDir('constant', 'int'))
    self.const_floats     = range(const_variables['float'] - getInitDir('constant', 'float'))
    self.const_strings    = range(const_variables['string'] - getInitDir('constant', 'string'))

    # Memory Stack
    self.memory_stack = []

  # Generate function memory
  # And push on to stack
  def createActiveRecord(self, function, local_count, temp_count):
    ar = ActivationRecord(function, local_count, temp_count)
    stackPush(self.memory_stack, ar)

  # Remove function memory on top of stack
  def removeActivationRecord(self):
    stackPop(self.memory_stack)

  # Get value
  def getValue(self, address):
    scope = getScope(address)

    if scope == 'global':
      # Get type
      varType = getType(address, scope)
      # Get list[address - initial size]
      if varType == 'bool':
        value = self.global_bools[address - getInitDir('global','bool')]
      elif varType == 'int':
        value = self.global_ints[address - getInitDir('global','int')]
      elif varType == 'float':
        value = self.global_floats[address - getInitDir('global','float')]
      elif varType == 'string':
        value = self.global_strings[address - getInitDir('global','string')]
      # Return
      return value
    elif scope == 'local':
      activationRecord = stackTop(self.memory_stack)
      value = activationRecord.getValue(address)
      # Return
      return value
    elif scope == 'temp':
      activationRecord = stackTop(self.memory_stack)
      value = activationRecord.getValue(address)
      # Return
      return value
    elif scope == 'constant':
      # Get type
      varType = getType(address, scope)
      # Get list[address - initial size]
      if varType == 'bool':
        value = self.const_bools[address - getInitDir('constant','bool')]
      elif varType == 'int':
        value = self.const_ints[address - getInitDir('constant','int')]
      elif varType == 'float':
        value = self.const_floats[address - getInitDir('constant','float')]
      elif varType == 'string':
        value = self.const_strings[address - getInitDir('constant','string')]
      # Return
      return value

  # Get array value
  # def getArrayValue(self, value, address):

  # Set value
  def setValue(self, value, address):
    scope = getScope(address)

    if scope == 'global':
      # Get type
      varType = getType(address, scope)
      # Get list[address - initial size]
      if varType == 'bool':
        self.global_bools[address - getInitDir('global','bool')] = value
        return True
      elif varType == 'int':
        self.global_ints[address - getInitDir('global','int')] = value
        return True
      elif varType == 'float':
        self.global_floats[address - getInitDir('global','float')] = value
        return True
      elif varType == 'string':
        self.global_strings[address - getInitDir('global','string')] = value
        return True
      else:
        return False
    elif scope == 'local':
      # Get function memory
      activationRecord = stackTop(self.memory_stack)
      # Get true / false if value was modified and return
      result = activationRecord.setValue(value, address)
      return result
    elif scope == 'temp':
      # Get function memory
      activationRecord = stackTop(self.memory_stack)
      # Get true / false if value was modified and return
      result = activationRecord.setValue(value, address)
      return result

  # Set array value
  # def setArrayValue
  
  # Initialize constants in memory
  def initializeConstants(self, constants):
    # Iterate all constants
    for key, value in constants.items():
      if value['type'] == 1:
        self.const_bools[value['address'] - getInitDir('constant','bool')] = value['val']
      elif value['type'] == 2:
        self.const_ints[value['address'] - getInitDir('constant','int')] = value['val']
      elif value['type'] == 3:
        self.const_floats[value['address'] - getInitDir('constant','float')] = value['val']
      elif value['type'] == 4:
        self.const_strings[value['address'] - getInitDir('constant','string')] = value['val']

    # print self.const_ints
