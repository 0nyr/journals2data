# this script test journals2data api!

# measure execution time
#    + https://datatofish.com/measure-time-to-run-python-script/ 
import time
start_time = time.time()

# run at ".." level
from context import get_python_run_context
get_python_run_context()

import journals2data
from journals2data import data
from journals2data import console
from journals2data import utils

# debug module imports
if utils.Global.DEBUG:
    import os
    print(
        "Python Current Working directory = " + str(os.getcwd())
    )


# test journals2data
collector = journals2data.DataCollector()
collector.scrap()



# get script execution time
execution_time = (time.time() - start_time)
print('Execution time in seconds: ' + str(execution_time))