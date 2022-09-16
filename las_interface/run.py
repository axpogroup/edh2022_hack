import pylas
from os import path

las_dir: str = '/Users/matthiasburger/git/data'


dimension_dictionary = dict()


class PointsData:
    def __init__(self, coordinates):

        self.x: int = coordinates[dimension_dictionary['X']]
        self.y: int = coordinates[dimension_dictionary['Y']]
        self.z: int = coordinates[dimension_dictionary['Z']]
        self.classification: int = coordinates[dimension_dictionary['classification']]

    def __repr__(self):
        return '%s' % str(self.__dict__)


with pylas.open(path.join(las_dir, '2662_1217.las')) as file:
    dimension_names = pylas.point.format.PointFormat(file.header.point_format_id).dimension_names

    index = 0
    for dimension_name in dimension_names:
        dimension_dictionary[dimension_name] = index
        index += 1

    line = file.read()

    for point in line.points_data.array:
        d_set = PointsData(point)
        print(dimension_dictionary)
        print(point)
        print(d_set)
        exit(0)

