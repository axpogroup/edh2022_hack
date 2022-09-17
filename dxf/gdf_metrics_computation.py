from scipy.spatial import ConvexHull

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

def computeMetrics(gdf):
    gdf["points"] = gdf.apply(getPoints, axis=1)
    gdf["volume"] = gdf.apply(computeVolumeHull, axis=1)
    gdf["z_ground"] = gdf.apply(getGround, axis=1)
    gdf["bounding_box"] = gdf.apply(getBoundingBox, axis=1)
    gdf["ground_center"] = gdf.apply(getGroundCenter, axis=1)
    return gdf