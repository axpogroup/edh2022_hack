import laspy
from laspy.lasdata import LasData
from laspy import ScaleAwarePointRecord
import numpy as np
from os import path
import plotly.express as px
import pandas as pd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import plotly.graph_objects as go


class LasPointCloud:
    def __init__(self, las: LasData):
        self.las = las
        self.x_scale = self.las.header.scales[0]
        self.x_offset = self.las.header.offsets[0]
        self.y_scale = self.las.header.scales[1]
        self.y_offset = self.las.header.offsets[1]
        self.z_scale = self.las.header.scales[2]
        self.z_offset = self.las.header.offsets[2]

    @classmethod
    def read(cls, path: str):
        las = laspy.read(path)
        return cls(las)

    def as_df(self, points):
        return pd.DataFrame.from_dict(
            {
                "x": (points.X * self.x_scale) + self.x_offset,
                "y": (points.Y * self.y_scale) + self.y_offset,
                "z": (points.Z * self.z_scale) + self.z_offset,
                "classification": points.classification.array,
            }
        )

    def in_rect(self, x0, x1, y0, y1):
        x0 = (x0 - self.x_offset) / self.x_scale
        x1 = (x1 - self.x_offset) / self.x_scale
        y0 = (y0 - self.y_offset) / self.y_scale
        y1 = (y1 - self.y_offset) / self.y_scale
        points = self.las.points[
            (self.las.X >= x0)
            & (self.las.X <= x1)
            & (self.las.Y >= y0)
            & (self.las.Y <= y1)
        ]
        return points

    def in_polygon(self, polygon: Polygon):
        x0, y0, x1, y1 = polygon.bounds
        points = self.in_rect(x0, x1, y0, y1)
        df = self.as_df(points)
        filter = [polygon.contains(Point(p["x"], p["y"])) for i, p in df.iterrows()]
        return df[filter]


if __name__ == "__main__":
    las = LasPointCloud.read("data/2665_1259.las")

    pol = [
        (2665708, 1259855),
        (2665759, 1259855),
        (2665759, 1259895),
        (2665708, 1259895),
    ]
    pol = Polygon(pol)

    df = las.in_polygon(pol)

    df_building = df[df.classification == 6]

    points = df_building[["x", "y", "z"]]
    hull = ConvexHull(points)
    hp = hull.points

    fig = px.scatter_3d(df, x="x", y="y", z="z", color="classification")

    fig.add_trace(
        go.Mesh3d(
            x=hp[:, 0], y=hp[:, 1], z=hp[:, 2], color="blue", opacity=0.5, alphahull=0
        )
    )
    fig.show()

    ax = df.plot.scatter("x", "y", c="classification")
    plt.show()

    ...
