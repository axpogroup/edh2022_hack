import geopandas as gpd
import gemgis as gg
from scipy.spatial import ConvexHull, convex_hull_plot_2d

thresholds=[300, 600]

gdf = gpd.read_file('../../Data/SWISSBUILDINGS3D_2_0_CHLV95LN02_1150-11.dxf')


def getPoints(gdf):
    geom = gdf["geometry"]
    return [v for g in geom for v in g.exterior.coords]

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

gdf["points"] = gdf.apply(getPoints, axis=1)
gdf["volume"] = gdf.apply(computeVolumeHull, axis=1)
gdf["z_ground"] = gdf.apply(getGround, axis=1)
gdf["bounding_box"] = gdf.apply(getBoundingBox, axis=1)
gdf["ground_center"] = gdf.apply(getGroundCenter, axis=1)

cleaned_df = gdf.loc[:,["volume", "bounding_box", "ground_center", "Layer", "EntityHandle"]]
cleaned_df.to_csv("volume_and_locations.csv")
