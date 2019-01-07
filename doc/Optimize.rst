AST Optimizer
=============

The AST optimizer provides 3 different optimization strategies:
 - Place command line with **if** condition before logging call (reduce tuple and dict creation and function calls).
 - Replace level constants by their values (reduce object lookups).
 - Remove logging calls (reduce overhead to zero).

