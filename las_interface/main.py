import sys
from pathlib import Path
from typing import List
from typing import Optional


import numpy as np
import pylas
from os import path

las_dir: str = '/Users/matthiasburger/git/edh2022_hack/data'

def recursive_split(x_min, y_min, x_max, y_max, max_x_size, max_y_size):
    x_size = x_max - x_min
    y_size = y_max - y_min

    if x_size > max_x_size:
        left = recursive_split(x_min, y_min, x_min + (x_size // 2), y_max, max_x_size, max_y_size)
        right = recursive_split(x_min + (x_size // 2), y_min, x_max, y_max, max_x_size, max_y_size)
        return left + right
    elif y_size > max_y_size:
        up = recursive_split(x_min, y_min, x_max, y_min + (y_size // 2), max_x_size, max_y_size)
        down = recursive_split(x_min, y_min + (y_size // 2), x_max, y_max, max_x_size, max_y_size)
        return up + down
    else:
        return [(x_min, y_min, x_max, y_max)]


size = (50, 50)
points_per_iter = 10**6


with pylas.open(path.join(las_dir, '2662_1217.las')) as file:

    sub_bounds = recursive_split(
        file.header.x_min,
        file.header.y_min,
        file.header.x_max,
        file.header.y_max,
        size[0],
        size[1]
    )

    count = 0
    for points in file.chunk_iterator(points_per_iter):
        print(f"{count / file.header.point_count * 100}%")

        x, y = points.x.copy(), points.y.copy()

        point_piped = 0

        for i, (x_min, y_min, x_max, y_max) in enumerate(sub_bounds):
            mask = (x >= x_min) & (x <= x_max) & (y >= y_min) & (y <= y_max)

            if np.any(mask):
                print(mask)

            point_piped += np.sum(mask)
            if point_piped == len(points):
                break
        count += len(points)
    print(f"{count / file.header.point_count * 100}%")