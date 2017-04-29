from Cube import *
from GaltonSnake import *
from VirtualMachine import *
from Functions import *
from ActivationRecord import *

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
  def createActivationRecord(self, local_count, temp_count):
    return ActivationRecord(local_count, temp_count)

  # Change activation record
  def changeActivationRecord(self, activationRecord):
    stackPush(self.memory_stack, activationRecord)

  # Remove function memory on top of stack
  def removeActivationRecord(self):
    stackPop(self.memory_stack)

  # Get value
  def getValue(self, address):
    if isinstance(address, basestring):
      value = self.getValue(address[1:-1])
      return value

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

  # Set value
  def setValue(self, value, address):
    if isinstance(address, basestring):
      self.setValue(value, address[1:-1])
      return

    scope = getScope(address)

    if scope == 'global':
      # Get type
      varType = getType(address, scope)
      # Get list[address - initial size]
      if varType == 'bool':
        self.global_bools[address - getInitDir('global','bool')] = value
      elif varType == 'int':
        self.global_ints[address - getInitDir('global','int')] = value
      elif varType == 'float':
        self.global_floats[address - getInitDir('global','float')] = value
      elif varType == 'string':
        self.global_strings[address - getInitDir('global','string')] = value
    elif scope == 'local':
      # Get function memory
      activationRecord = stackTop(self.memory_stack)
      # Get true / false if value was modified and return
      activationRecord.setValue(value, address)
    elif scope == 'temp':
      # Get function memory
      activationRecord = stackTop(self.memory_stack)
      # Get true / false if value was modified and return
      activationRecord.setValue(value, address)
  
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
