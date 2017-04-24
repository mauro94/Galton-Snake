from Cube import *
from GaltonSnake import *
from VirtualMachine import *
from Functions import *

# Initial memory addresses
initial_global_bool = 10000
initial_global_int = 12000
initial_global_float = 14000
initial_global_string = 16000
initial_global_dataframe = 20000

initial_local_bool = 40000
initial_local_int = 42000
initial_local_float = 44000
initial_local_string = 46000
initial_local_dataframe = 50000

initial_temp_bool = 60000
initial_temp_int = 62000
initial_temp_float = 64000
initial_temp_string = 66000
initial_temp_dataframe = 70000

initial_constant_bool = 80000
initial_constant_int = 82000
initial_constant_float = 84000
initial_constant_string = 86000

class Memory:
  """docstring for Memory"""
  def __init__(self, name, global_variables, local_variables, temp_variables, const_variables):
    # Name for the memory object
    self.name = name

    # Creating lists with the amount of variables needed to be stored
    # Global variables
    self.global_bools      = range(global_variables['bool'] - initial_global_bool)
    self.global_ints       = range(global_variables['int'] - initial_global_int)
    self.global_floats     = range(global_variables['float'] - initial_global_float)
    self.global_strings    = range(global_variables['string'] - initial_global_string)
    # self.global_dataframes = range(global_variables['dataframe'] + 1)

    # Local variables
    self.local_bools      = range(local_variables['bool'] - initial_local_bool)
    self.local_ints       = range(local_variables['int'] - initial_local_int)
    self.local_floats     = range(local_variables['float'] - initial_local_float)
    self.local_strings    = range(local_variables['string'] - initial_local_string)
    # self.local_dataframes = range(local_variables['dataframe'] + 1)    

    # Temporary variables
    self.temp_bools      = range(temp_variables['bool'] - initial_temp_bool)
    self.temp_ints       = range(temp_variables['int'] - initial_temp_int)
    self.temp_floats     = range(temp_variables['float'] - initial_temp_float)
    self.temp_strings    = range(temp_variables['string'] - initial_temp_string)
    # self.temp_dataframes = range(temp_variables['dataframe'])
    
    # Constants
    self.const_bools      = range(const_variables['bool'] - initial_constant_bool)
    self.const_ints       = range(const_variables['int'] - initial_constant_int)
    self.const_floats     = range(const_variables['float'] - initial_constant_float)
    self.const_strings    = range(const_variables['string'] - initial_constant_string)
    # self.const_dataframes = range(const_variables['dataframe'] + 1)

    # Memory Stack
    self.memory_stack = []

  # Get value
  def getValue(self, address):
    scope = getScope(address)

    if scope == 'global':
      # Get type
      varType = getType(address, scope)
      # Get list[address - initial size]
      if varType == 'bool':
        value = self.global_bools[address - initial_global_bool]
      elif varType == 'int':
        value = self.global_ints[address - initial_global_int]
      elif varType == 'float':
        value = self.global_floats[address - initial_global_float]
      elif varType == 'string':
        value = self.global_strings[address - initial_global_string]
      # Return
      return value
    elif scope == 'local':
      # Get type
      varType = getType(address, scope)
      # Get list[address - initial size]
      if varType == 'bool':
        value = self.local_bools[address - initial_local_bool]
      elif varType == 'int':
        value = self.local_ints[address - initial_local_int]
      elif varType == 'float':
        value = self.local_floats[address - initial_local_float]
      elif varType == 'string':
        value = self.local_strings[address - initial_local_string]
      # Return
      return value
    elif scope == 'temp':
      # Get type
      varType = getType(address, scope)
      # Get list[address - initial size]
      if varType == 'bool':
        value = self.temp_bools[address - initial_temp_bool]
      elif varType == 'int':
        value = self.temp_ints[address - initial_temp_int]
      elif varType == 'float':
        value = self.temp_floats[address - initial_temp_float]
      elif varType == 'string':
        value = self.temp_strings[address - initial_temp_string]
      # Return
      return value
    elif scope == 'constant':
      # Get type
      varType = getType(address, scope)
      # Get list[address - initial size]
      if varType == 'bool':
        value = self.const_bools[address - initial_constant_bool]
      elif varType == 'int':
        value = self.const_ints[address - initial_constant_int]
      elif varType == 'float':
        value = self.const_floats[address - initial_constant_float]
      elif varType == 'string':
        value = self.const_strings[address - initial_constant_string]
      # Return
      return value

  #Set value
  def setValue(self, value, address):
    scope = getScope(address)

    if scope == 'global':
      # Get type
      varType = getType(address, scope)
      # Get list[address - initial size]
      if varType == 'bool':
        self.global_bools[address - initial_global_bool] = value
        return True
      elif varType == 'int':
        self.global_ints[address - initial_global_int] = value
        return True
      elif varType == 'float':
        self.global_floats[address - initial_global_float] = value
        return True
      elif varType == 'string':
        self.global_strings[address - initial_global_string] = value
        return True
      else:
        return False
    elif scope == 'local':
      # Get type
        varType = getType(address, scope)
        # Get list[address - initial size]
        if varType == 'bool':
          self.local_bools[address - initial_local_bool] = value
          return True
        elif varType == 'int':
          self.local_ints[address - initial_local_int] = value
          return True
        elif varType == 'float':
          self.local_floats[address - initial_local_float] = value
          return True
        elif varType == 'string':
          self.local_strings[address - initial_local_string] = value
          return True
        else:
          return False
    elif scope == 'temp':
      # Get type
        varType = getType(address, scope)
        # Get list[address - initial size]
        if varType == 'bool':
          self.temp_bools[address - initial_temp_bool] = value
          return True
        elif varType == 'int':
          self.temp_ints[address - initial_temp_int] = value
          return True
        elif varType == 'float':
          self.temp_floats[address - initial_temp_float] = value
          return True
        elif varType == 'string':
          self.temp_strings[address - initial_temp_string] = value
          return True
        else:
          return False
  
  # Initialize constants in memory
  def initialize_constants(self, constants):
    # Iterate all constants
    for key, value in constants.items():
      if value['type'] == 1:
        self.const_bools[value['address'] - initial_constant_bool] = value['val']
      elif value['type'] == 2:
        self.const_ints[value['address'] - initial_constant_int] = value['val']
      elif value['type'] == 3:
        self.const_floats[value['address'] - initial_constant_float] = value['val']
      elif value['type'] == 4:
        self.const_strings[value['address'] - initial_constant_string] = value['val']

    # print self.const_ints

# Memory helper functions
# Get type based on address
def getType (address, scope):
  if scope == 'global':
    if between(address, initial_global_bool, initial_global_int):
      return 'bool'
    elif between(address, initial_global_int, initial_global_float):
      return 'int'
    elif between(address, initial_global_float, initial_global_string):
      return 'float'
    elif between(address, initial_global_string, initial_global_dataframe):
      return 'string'
    elif between(address, initial_global_dataframe, initial_local_bool):
      return 'dataframe'
  elif scope == 'local':
    if between(address, initial_local_bool, initial_local_int):
      return 'bool'
    elif between(address, initial_local_int, initial_local_float):
      return 'int'
    elif between(address, initial_local_float, initial_local_string):
      return 'float'
    elif between(address, initial_local_string, initial_local_dataframe):
      return 'string'
    elif between(address, initial_local_dataframe, initial_temp_bool):
      return 'dataframe'
  elif scope == 'temp':
    if between(address, initial_temp_bool, initial_temp_int):
      return 'bool'
    elif between(address, initial_temp_int, initial_temp_float):
      return 'int'
    elif between(address, initial_temp_float, initial_temp_string):
      return 'float'
    elif between(address, initial_temp_string, initial_temp_dataframe):
      return 'string'
    elif between(address, initial_temp_dataframe, initial_temp_bool):
      return 'dataframe'
  elif scope == 'constant':
    if between(address, initial_constant_bool, initial_constant_int):
      return 'bool'
    elif between(address, initial_constant_int, initial_constant_float):
      return 'int'
    elif between(address, initial_constant_float, initial_constant_string):
      return 'float'
    elif between(address, initial_constant_string, 100000):
      return 'string'

# Get scope based on address
def getScope (address):
  if between(address, initial_global_bool, initial_local_bool):
    return 'global'
  elif between(address, initial_local_bool, initial_temp_bool):
    return 'local'
  elif between(address, initial_temp_bool, initial_constant_bool):
    return 'temp'
  # TODO: define a memory limit
  elif between(address, initial_constant_bool, 100000):
    return 'constant'
  else:
    print('Address non existent')

# Function to check values between
def between (value, low, high):
  return (low <= value < high)