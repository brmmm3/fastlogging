AST Optimizer
=============

The AST optimizer provides 3 different optimization strategies:
 - Insert command line with **if** condition before logging call (reduce tuple and dict creation and function calls).
 - Replace level constants by their values (reduce object lookups).
 - Remove logging calls (reduce overhead to zero).

An example for using the AST optimizer can be found in **examples/benchmark.py**.

Global optimize members
-----------------------

::

 OptimizeAst    The base class for all methods below.
 Optimize       A decorator for optimizing a code block.
 OptimizeObj    A function for optimizing a Python object.
 OptimizeModule A function for optimizing a Python module.
 OptimizeFile   A function for optimizing a Python file.
 WritePycFile   A function for writing byte compiled Python code to a .pyc file.

Optimize
--------

An example for using the decorator is shown below. On the console you'll only see the warning message.

.. code-block:: Python

    from fastlogging import LogInit, INFO, Optimize

    logger = LogInit(console=True)

    @Optimize(globals(), "logger", remove=INFO)
    def bar():
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")

    bar()

Or you can call OptimizeObj to create an optimized copy of function **bar()** in a separate object.

.. code-block:: Python

    from fastlogging import LogInit, INFO, Optimize

    logger = LogInit(console=True)

    def bar():
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")

    optBar = OptimizeObj(globals(), bar, "logger", remove=INFO)
    optBar()

Or you can call OptimizeFile to load an optimized copy of a python file into a Python object.

.. code-block:: Python

    from fastlogging import LogInit, INFO, OptimizeFile

    logger = LogInit(console=True)

    optBar = OptimizeFile(globals(), "opt_test.py", "logger", remove=INFO)
    optBar.bar()
