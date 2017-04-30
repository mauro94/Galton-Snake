from Functions import *

class ActivationRecord:
  def __init__(self, local_variables, temp_variables):
    # Local variables
    self.local_bools      = [None] * (local_variables['bool'] - getInitDir('local','bool'))
    self.local_ints       = [None] * (local_variables['int'] - getInitDir('local','int'))
    self.local_floats     = [None] * (local_variables['float'] - getInitDir('local','float'))
    self.local_strings    = [None] * (local_variables['string'] - getInitDir('local','string'))
    # self.local_dataframes = [None] * (local_variables['dataframe'] - getInitDir('local','dataframe'))
    self.local_dataframes = {}

    # Temporary variables
    self.temp_bools      = [None] * (temp_variables['bool'] - getInitDir('temp','bool'))
    self.temp_ints       = [None] * (temp_variables['int'] - getInitDir('temp','int'))
    self.temp_floats     = [None] * (temp_variables['float'] - getInitDir('temp','float'))
    self.temp_strings    = [None] * (temp_variables['string'] - getInitDir('temp','string'))
    # self.temp_dataframes = [None] * (temp_variables['dataframe'] - getInitDir('temp', 'dataframe'))

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


# =========================================================
# DATAFRAMES
# =========================================================

  # =======================================================
  # CREATION
  # =======================================================

  def createDataframe(self, dataframe, title):
    self.local_dataframes[title] = dataframe

  # =======================================================
  # ACCESS
  # =======================================================

  def accessRow(self, title, row):
    return self.local_dataframes[title]['data'][row]

  def accessCol(self, title, col):
    return self.local_dataframes[title]['data'][:,col]

  def accessDf(self, title):
    return self.local_dataframes[title]

  def accessTags(self, title):
    return self.local_dataframes[title]['tags']

  def accessCell(self, title, row, col):
    return self.local_dataframes[title]['data'][row][col]

  def accessData(self, title):
    return self.local_dataframes[title]['data']

  def accessHeaders(self, title):
    return self.local_dataframes[title]['headers']

  # =======================================================
  # DYNAMIC BIZZ
  # =======================================================

  # def bindRows(self, df1, df2, row1, row2, scope):


  # Dataframe memory management
  # def generateMemory(self, dataframe, address):
  #   # Calculate offset / size
  #   offset = 0;
  #   end_address = address + offset

  #   # Check if df is TOO BIG
  #   if not between(end_address, getInitDir('local', 'dataframe'), getInitDir('temp', 'bool')):
  #     print 'Memory limit reached'
  #     exit(1)

  # def bindRowDataframe(self, row1, row2):
  #   print 'Bind rows'

  # def bindColDataframe(self, col1, col2):
  #   print 'Bind columns'

  # def reallocateMemory(self, dataframe):
  #   print 'Reallocate memory'

  # TODO: understand get value for data frames