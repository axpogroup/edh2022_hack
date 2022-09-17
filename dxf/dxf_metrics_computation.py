from scipy.spatial import ConvexHull
import geopandas as gpd
import pandas as pd

def getPoints(gdf):
    geom = gdf["geometry"]
    return [v for g in geom.geoms for v in g.exterior.coords]

def computeVolumeHull(gdf):
    hull = ConvexHull(gdf["points"])
    return hull.volume

def getGround(gdf):
    return min([v[2] for v in gdf["points"]])

def getBoundingBox(gdf):
    geom = gdf["geometry"]
    xmin = geom.bounds[0]
    ymin = geom.bounds[1]
    xmax = geom.bounds[2]
    ymax = geom.bounds[3]
    zs = [v[2] for v in gdf["points"]]
    return [[xmin, ymin, min(zs)], [xmax, ymax, max(zs)]]

def getGroundCenter(gdf):
    bb = gdf["bounding_box"]
    return [(bb[1][0]+bb[0][0])*1/2, (bb[1][1]+bb[0][1])*1/2, gdf["z_ground"]]

def convertPoly(poly):
    return [[v[0], v[1], v[2]] for v in poly.exterior.coords]

def getGroundPolygon(gdf):
    geom = gdf["geometry"]
    groundPoly  = []
    for poly in geom.geoms:
        isGrounded = [v[2] == gdf["z_ground"] for v in poly.exterior.coords]
        if isGrounded:
            groundPoly.append(convertPoly(poly))
    return groundPoly


def computeMetrics(gdf):
    gdf["points"] = gdf.apply(getPoints, axis=1)
    gdf["volume"] = gdf.apply(computeVolumeHull, axis=1)
    gdf["z_ground"] = gdf.apply(getGround, axis=1)
    gdf["bounding_box"] = gdf.apply(getBoundingBox, axis=1)
    gdf["ground_polygons"] = gdf.apply(getGroundPolygon, axis=1)
    gdf["ground_center"] = gdf.apply(getGroundCenter, axis=1)
    return gdf

def computeAll(dxf_filenames, output_csv_filename):
    gdfs = []
    for dxf_filename in dxf_filenames:
        gdf = gpd.read_file(dxf_filename)
        gdf = computeMetrics(gdf)
        gdfs.append(gdf)
    gdf_merged = pd.concat(gdfs)

    cleaned_df = gdf_merged.loc[:, ["volume", "bounding_box", "ground_center", "ground_polygons", "Layer", "EntityHandle"]]
    cleaned_df.to_csv(output_csv_filename)
    cleaned_df
