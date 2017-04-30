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
    self.global_bools      = [None] * (global_variables['bool'] - getInitDir('global', 'bool'))
    self.global_ints       = [None] * (global_variables['int'] - getInitDir('global', 'int'))
    self.global_floats     = [None] * (global_variables['float'] - getInitDir('global', 'float'))
    self.global_strings    = [None] * (global_variables['string'] - getInitDir('global', 'string'))
    # self.global_dataframes = [None] * (global_variables['dataframe'] - getInitDir('global', 'dataframe'))
    self.global_dataframes = {}

    # Constants
    self.const_bools      = [None] * (const_variables['bool'] - getInitDir('constant', 'bool'))
    self.const_ints       = [None] * (const_variables['int'] - getInitDir('constant', 'int'))
    self.const_floats     = [None] * (const_variables['float'] - getInitDir('constant', 'float'))
    self.const_strings    = [None] * (const_variables['string'] - getInitDir('constant', 'string'))

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
      value = self.getValue(int(address[1:-1]))
      # Check if value address has a value
      value_address = self.getValue(value)
      if not value_address == None:
        return value_address
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
      # Check if pointer already has a value
      pointer_address = self.getValue(int(address[1:-1]))
      # Check if it is an address
      if pointer_address > getInitDir('global', 'bool'):
        self.setValue(value, pointer_address)
      # Set value of pointer
      else:
        self.setValue(value, int(address[1:-1]))
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

# =========================================================
# DATAFRAME MEMORY
# =========================================================

  # =======================================================
  # CREATION
  # =======================================================

  def createDataframe(self, dataframe, title):
    self.global_dataframes[title] = dataframe

  # =======================================================
  # ACCESS
  # =======================================================

  def accessRow (self, title, row, scope):
    if scope == 1:
      return self.global_dataframes[title]['data'][row]
    else:
      activationRecord = stackTop(self.memory_stack)
      return activationRecord.accessRow(title, row)

  def accessCol (self, title, col, scope):
    if scope == 1:
      return column(self.global_dataframes[title]['data'], col)
    else:
      activationRecord = stackTop(self.memory_stack)
      return activationRecord.accessCol(title, col)

  def accessDf (self, title, scope):
    if scope == 1:
      return self.global_dataframes[title]
    else:
      activationRecord = stackTop(self.memory_stack)
      return activationRecord.accessDf(title)

  def accessTags (self, title, scope):
    if scope == 1:
      keyArr = []
      for key, value in self.global_dataframes[title]['tags'].items():
        keyArr.append(key[1:-1])
      return keyArr
    else:
      activationRecord = stackTop(self.memory_stack)
      return activationRecord.accessTags(title)

  def accessCell (self, title, scope, row, col):
    if scope == 1:
      return self.global_dataframes[title]['data'][row][col]
    else:
      activationRecord = stackTop(self.memory_stack)
      return activationRecord.accessCell(title, row, col)

  def accessData (self, title, scope):
    if scope == 1:
      return self.global_dataframes[title]['data']
    else:
      activationRecord = stackTop(self.memory_stack)
      return activationRecord.accessData(title)

  def accessHeaders (self, title, scope):
    if scope == 1:
      return self.global_dataframes[title]['headers']
    else:
      activationRecord = stackTop(self.memory_stack)
      return activationRecord.accessHeaders(title)

  # =======================================================
  # CORRELATIONS
  # =======================================================

  def correlateTags (self):
    print 'Correlate Tags'

  def correlateData (self):
    print 'Correlate Data'
    
  # =======================================================
  # DYNAMIC BIZZ
  # =======================================================

  # Dataframe memory management
  # def generateMemory(self, dataframe, address):
  #   # Calculate offset / size
  #   offset = 0;
  #   end_address = address + offset

  #   scope = getScope(address)

  #   if scope == 'global':
  #     # Check if dataframe is TOO big
  #     if not between(end_address, getInitDir('global', 'dataframe'), getInitDir('local', 'bool')):
  #       print 'Memory limit reached'
  #       exit(1)

  #     # MAKE MEMORY GREAT AGAIN!

  #   elif scope == 'local':
  #     activationRecord = stackTop(self.memory_stack)
  #     activationRecord.generateMemory(dataframe, address)

  # def bindRowDataframe(self, row1, row2):
  #   print 'Bind rows'

  # def bindColDataframe(self, col1, col2):
  #   print 'Bind columns'

  # def reallocateMemory(self, address, old_size, new_size):
  #   scope = getScope(address)

  #   if scope == 'global':
  #     location = address - getInitDir('global', 'dataframe')
  #     # New data allocation
  #     for i in range(new_size):
  #       self.global_dataframes.append(self.global_dataframes[location+i])

  #     new_location = address + len(self.global_dataframes) - location

  #     # Point to new data
  #     for i in range(old_size):
  #       self.global_dataframes[location+i] = '(' + str(new_location + i) + ')'

  # TODO: understand get value for data frames