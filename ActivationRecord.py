from Functions import *

class ActivationRecord:
  def __init__(self, local_variables, temp_variables):
    # Local variables
    self.local_bools      = range(local_variables['bool'] - getInitDir('local','bool'))
    self.local_ints       = range(local_variables['int'] - getInitDir('local','int'))
    self.local_floats     = range(local_variables['float'] - getInitDir('local','float'))
    self.local_strings    = range(local_variables['string'] - getInitDir('local','string'))
    self.local_dataframes = range(local_variables['dataframe'] - getInitDir('local','dataframe'))

    # Temporary variables
    self.temp_bools      = range(temp_variables['bool'] - getInitDir('temp','bool'))
    self.temp_ints       = range(temp_variables['int'] - getInitDir('temp','int'))
    self.temp_floats     = range(temp_variables['float'] - getInitDir('temp','float'))
    self.temp_strings    = range(temp_variables['string'] - getInitDir('temp','string'))
    self.temp_dataframes = range(temp_variables['dataframe'] - getInitDir('temp', 'dataframe'))

  def getValue(self, address):
    scope = getScope(address)

    if scope == 'local':
      # Get type
      varType = getType(address, scope)
      # Get list[address - initial_size]
      if varType == 'bool':
        value = self.local_bools[address - getInitDir('local','bool')]
      elif varType == 'int':
        value = self.local_ints[address - getInitDir('local','int')]
      elif varType == 'float':
        value = self.local_floats[address - getInitDir('local','float')]
      elif varType == 'string':
        value = self.local_strings[address - getInitDir('local','string')]
      # Return
      return value
    elif scope == 'temp':
      # Get type
      varType = getType(address, scope)
      # Get list[address - initial size]
      if varType == 'bool':
        value = self.temp_bools[address - getInitDir('temp','bool')]
      elif varType == 'int':
        value = self.temp_ints[address - getInitDir('temp','int')]
      elif varType == 'float':
        value = self.temp_floats[address - getInitDir('temp','float')]
      elif varType == 'string':
        value = self.temp_strings[address - getInitDir('temp','string')]
      # Return
      return value
    else:
      print 'Unknown address on getting value'
      # exit(1)

  def setValue(self, value, address):
    scope = getScope(address)
    
    if scope == 'local':
      # Get type
        varType = getType(address, scope)
        # Get list[address - initial size]
        if varType == 'bool':
          self.local_bools[address - getInitDir('local','bool')] = value
        elif varType == 'int':
          self.local_ints[address - getInitDir('local','int')] = value
        elif varType == 'float':
          self.local_floats[address - getInitDir('local','float')] = value
        elif varType == 'string':
          self.local_strings[address - getInitDir('local','string')] = value
    elif scope == 'temp':
      # Get type
        varType = getType(address, scope)
        # Get list[address - initial size]
        if varType == 'bool':
          self.temp_bools[address - getInitDir('temp','bool')] = value
        elif varType == 'int':
          self.temp_ints[address - getInitDir('temp','int')] = value
        elif varType == 'float':
          self.temp_floats[address - getInitDir('temp','float')] = value
        elif varType == 'string':
          self.temp_strings[address - getInitDir('temp','string')] = value
    else:
      print 'Unknown address on setting value'
      # exit(1)