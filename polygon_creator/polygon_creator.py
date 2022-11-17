import plotly.graph_objects as go
import numpy as np
import shapely.geometry as shgeo
import matplotlib.pyplot as plt

POINTS = [(2655011.0, 1217198.5), (2655986.0, 1217333.5), (2655996.0, 1217338.5), (2656521.0, 1217473.5), (2657006.0, 1217523.5),(2657976.0, 1217373.5)]
PADDING = 100
'''
def rad_to_deg(rad: float) -> float:
    return rad/(np.pi*2)*360

def bounding_points_ends(p0: tuple[float], init_angle: float) -> list[tuple]:
    angles = [init_angle + np.pi/2, init_angle + np.pi*3/4, init_angle + np.pi, init_angle + np.pi*5/4, init_angle + np.pi*3/2]
    points = []
    for angle in angles:
        p1 = [np.cos(angle)*padding, np.sin(angle)*padding]
        p2 = [sum(x) for x in zip(p0, p1)]
        points.append(p2)
    return points

def bounding_points_middle(p0: tuple[float], p1: tuple[float], p2: tuple[float]):
    incoming_angle = calculate_angle(p0, p1)
    outgoing_angle = calculate_angle(p2, p1)
    half_angle1 = (incoming_angle + outgoing_angle) / 2
    half_angle2 = half_angle1 + np.pi
    p_new1 = [np.cos(half_angle1)*padding, np.sin(half_angle1)*padding]
    p_new2 = [sum(x) for x in zip(p_new1, p1)]
    p_new3 = [np.cos(half_angle2)*padding, np.sin(half_angle2)*padding]
    p_new4 = [sum(x) for x in zip(p_new3, p1)]
    return [p_new2, p_new4]

def get_scatter(points) -> go.Scatter:
    x_coords = list(map(lambda coord: coord[0], points))
    y_coords = list(map(lambda coord: coord[1], points))
    scatterline = go.Scatter(x=x_coords, y=y_coords, mode='markers')
    return scatterline

def calculate_angle(point1, point2):
    return np.arctan2(point1[1]-point2[1], point1[0]-point2[0])

first_angle = calculate_angle(POINTS[1], POINTS[0])
last_angle = calculate_angle(POINTS[-2], POINTS[-1])
start_box_points = bounding_points_ends(POINTS[0], first_angle)
end_box_points = bounding_points_ends(POINTS[-1], last_angle)

middle_box_points = []
for idx in range(1, len(POINTS)-1):
    middle_box_points += bounding_points_middle(POINTS[idx-1], POINTS[idx], POINTS[idx+1])

scatter1 = get_scatter(POINTS)
scatter2 = get_scatter(start_box_points)
scatter3 = get_scatter(end_box_points)
scatter4 = get_scatter(middle_box_points)

fig = go.Figure(data=[scatter1, scatter2, scatter3, scatter4])
fig.show()
'''



line = shgeo.LineString(POINTS)
surrounding_polygon = line.buffer(PADDING, cap_style=3, join_style=3)



x, y = surrounding_polygon.exterior.xy

print(list(zip(x, y)))



plt.plot(x, y)
plt.plot(*line.xy)
plt.show()