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
    self.global_bools      = range(global_variables['bool'] + 1)
    self.global_ints       = range(global_variables['int'] + 1)
    self.global_floats     = range(global_variables['float'] + 1)
    self.global_strings    = range(global_variables['string'] + 1)
    # self.global_dataframes = range(global_variables['dataframe'] + 1)

    # Local variables
    self.local_bools      = range(local_variables['bool'] + 1)
    self.local_ints       = range(local_variables['int'] + 1)
    self.local_floats     = range(local_variables['float'] + 1)
    self.local_strings    = range(local_variables['string'] + 1)
    # self.local_dataframes = range(local_variables['dataframe'] + 1)    

    # Temporary variables
    self.temp_bools      = range(temp_variables['bool'] + 1)
    self.temp_ints       = range(temp_variables['int'] + 1)
    self.temp_floats     = range(temp_variables['float'] + 1)
    self.temp_strings    = range(temp_variables['string'] + 1)
    # self.temp_dataframes = range(temp_variables['dataframe'] + 1)
    
    # Constants
    self.const_bools      = range(const_variables['bool'] + 1)
    self.const_ints       = range(const_variables['int'] + 1)
    self.const_floats     = range(const_variables['float'] + 1)
    self.const_strings    = range(const_variables['string'] + 1)
    # self.const_dataframes = range(const_variables['dataframe'] + 1)

    # Memory Stack
    self.memory_stack = []

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
    # TODO: check if necessary to get constant type

  # Get scope based on address
  def getScope (address):
    if between(address, initial_global_bool, initial_local_bool):
      return 'global'
    elif between(address, initial_local_bool, initial_temp_bool):
      return 'local'
    elif between(address, initial_temp_bool, initial_constant_bool):
      return 'temp'
    # TODO: define a memory limit
    elif between(address, initial_constant_bool, mem_limit):
      return 'constant'
    else:
      print('Address non existent')

  # Get value
  def getValue(address):
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

    # elif scope == 'constant':

  #Set value
  def setValue(value, address):
    scope = getScope(address)

    if scope == 'global':
      # Get type
      varType = getType(address, scope)
      # Get list[address - initial size]
      if varType == 'bool':
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

    # elif scope == 'constant'

  # Function to check values between
  def between (value, low, high):
    return (low <= value < high)