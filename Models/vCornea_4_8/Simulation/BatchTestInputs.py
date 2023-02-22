# Defining parameters that will be used GLOBALY in the simulation steppable file
# Initializer Dictionary
__param_desc__ = {}

# List of Parameters to change

__param_desc__["PARAMETER_NAME"] = "(optional) PARAMETER DESCRIPTION"

# PARAMETER VALUE
PARAMETER_NAME = 1  # Best to use one since the batch execution uses the multiplier function 
                    # meaning the number you define in batch_exec.py file will be the actual 
                    # tested parameter

__param_desc__["PARAMETER_NAME2"] = "(optional) PARAMETER2 DESCRIPTION"

PARAMETER_NAME2 = 1

__param_desc__["PARAMETER_NAME3"] = "(optional) PARAMETER3 DESCRIPTION"

PARAMETER_NAME3 = 1
