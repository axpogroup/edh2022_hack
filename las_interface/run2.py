import laspy
import numpy as np
from os import path

las_dir: str = '/Users/matthiasburger/git/data'


las = laspy.read(path.join(las_dir, '2662_1217.las'))

dimension_names = list(las.point_format.dimension_names)
dimension_dictionary = dict()
index = 0
for dimension_name in dimension_names:
    dimension_dictionary[dimension_name] = index

class PointsData:
    def __init__(self, data):

        self.x: int = data[dimension_dictionary['X']]
        self.y: int = data[dimension_dictionary['Y']]
        self.z: int = data[dimension_dictionary['Z']]
        self.classification: int = data[dimension_dictionary['classification']]

    def __repr__(self):
        return '%s' % str(self.__dict__)



for line in las:
    #print(line.x.array)
    #exit(0)
    p = PointsData(line)


# classifications = list(las.classification)
# print(classifications)