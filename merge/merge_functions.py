#import building_classifier
import pandas as pd
import numpy as np
import json
import geopandas as gpd
import scipy

def computeAdvancedClass(gbr, distanceThreshold):
    if gbr.dist > distanceThreshold:
        return gbr.building_type
    if gbr.building_type == 'UNKNOWN':#building_classifier.BuildingType.UNKNOWN:
        return 'UNKNOWN'#building_classifier.BuildingType.UNKNOWN
    if gbr.building_type == 'NON_RESIDENTIAL':#building_classifier.BuildingType.NON_RESIDENTIAL:
        return 'NON_RESIDENTIAL'#building_classifier.BuildingType.NON_RESIDENTIAL
    if gbr.building_type == 'RESIDENTIAL':#building_classifier.BuildingType.RESIDENTIAL:
        if gbr.volume < 300:
            return 'RESIDENTIAL_12M'
        else:
            return 'RESIDENTIAL_15M'
    if gbr.building_type == 'AGRICULTURAL':#building_classifier.BuildingType.AGRICULTURAL:
        if gbr.volume < 600:
            return 'AGRICULTURAL_15M'
        else:
            return 'AGRICULTURAL_20M'

def merge(csv_gbr_input_filename, csv_dxf_input_filename, csv_gbr_output_filename):
    df_gbr = pd.read_csv(csv_gbr_input_filename)
    df_gbr["ground_center"] = df_gbr[["coordinate_lat", "coordinate_lon"]].values.tolist()

    df_dxf = pd.read_csv(csv_dxf_input_filename, converters={
        "ground_center": json.loads,
        "bounding_box": json.loads
    })

    points_gbr = [[p[0], p[1]] for p in df_gbr.ground_center]
    points_dxf = [[p[0], p[1]] for p in df_dxf.ground_center]
    gbr_x_dfx_dist = scipy.spatial.distance.cdist(points_gbr, points_dxf)

    map_gbr_dist = np.amin(gbr_x_dfx_dist, axis=1)
    map_gbr_col = np.apply_along_axis(lambda arr: np.where(arr == np.amin(arr))[0][0], 1, gbr_x_dfx_dist)
    df_gbr["dist"] = map_gbr_dist
    df_gbr["dxf_index"] = map_gbr_col
    df_gbr["dxf_volume"] = df_dxf.loc[df_gbr.dxf_index, "volume"].tolist()
    df_gbr["dxf_ground_center"] = df_dxf.loc[df_gbr.dxf_index, "ground_center"].tolist()

    df_gbr["advancedCategory"] = df_gbr.apply(computeAdvancedClass, axis=1, distanceThreshold=10)

    df_gbr.to_csv(csv_gbr_output_filename)