from Cube import *
from GaltonSnake import *
from VirtualMachine import *

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
    self.global_chars      = range(global_variables['char'] + 1)
    # self.global_strings    = range(global_variables['string'])
    # self.global_dataframes = range(global_variables['dataframe'])

    # Local variables
    self.local_bools      = range(local_variables['bool'] + 1)
    self.local_ints       = range(local_variables['int'] + 1)
    self.local_floats     = range(local_variables['float'] + 1)
    self.local_chars      = range(local_variables['char'] + 1)
    # self.local_strings    = range(local_variables['string'] + 1)
    # self.local_dataframes = range(local_variables['dataframe'] + 1)    

    # Temporary variables
    self.temp_bools      = range(temp_variables['bool'] + 1)
    self.temp_ints       = range(temp_variables['int'] + 1)
    self.temp_floats     = range(temp_variables['float'] + 1)
    self.temp_chars      = range(temp_variables['char'] + 1)
    # self.temp_strings    = range(temp_variables['string'] + 1)
    # self.temp_dataframes = range(temp_variables['dataframe'] + 1)
    
    # Constants
    self.const_bools      = range(const_variables['bool'] + 1)
    self.const_ints       = range(const_variables['int'] + 1)
    self.const_floats     = range(const_variables['float'] + 1)
    self.const_chars      = range(const_variables['char'] + 1)
    # self.const_strings    = range(const_variables['string'] + 1)
    # self.const_dataframes = range(const_variables['dataframe'] + 1)

  # Function to check values between
  def between (value, low, high):
    return (low >= value && value < high)