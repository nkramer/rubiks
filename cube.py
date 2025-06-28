
# Online Python - IDE, Editor, Compiler, Interpreter
import random

#x = ["L", "L'", "R", "R'"]
x = "L L' R R'".split(" ")
path = [random.choice(x) for i in range(20)]
print( " ".join(path) )

import numpy as np
