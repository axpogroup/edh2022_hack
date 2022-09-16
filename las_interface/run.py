import sys
from pathlib import Path
from typing import List
from typing import Optional


import numpy as np
import pylas
from os import path

las_dir: str = '/Users/matthiasburger/git/data'


with pylas.open(path.join(las_dir, '2662_1217.las')) as file:
    line = file.read()
    print(line.points_data.array)
