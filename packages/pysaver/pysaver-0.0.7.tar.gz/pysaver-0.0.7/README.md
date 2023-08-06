# Pysaver

## A utility to save the python REPL history to an external file.


### Installation

    python3 -m pip install pysaver


### Usage

**Save everything**

    import pysaver

Saves entire REPL history to the file saved_repl_history.py in the current directory.

**Save everything but you are in the REPL and you don't have pysaver installed**

    from pip._internal import main as pip
    pip(['install', 'pysaver'])
    import pysaver

**Save some or all history to a specified file**

    from pysaver import repl_history
    repl_history(num_lines=-1, file_name="saved_repl_history.py")

This is the default, saves all REPL history to the default file name in the current directory.

    repl_history(num_lines=10, file_name="my_history.py")

This saves last 10 lines to my_history.py.


