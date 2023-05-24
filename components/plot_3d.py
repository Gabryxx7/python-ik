from figure_template import HEXAPOD_FIGURE
from dash import dcc
from dash import html
from copy import deepcopy
from style_settings import NUMBER_INPUT_STYLE
from pyquaternion import Quaternion

GRAPH_ID = "graph-kinematics"
BASE_FIGURE = deepcopy(HEXAPOD_FIGURE)
plot3d = dcc.Graph(id=GRAPH_ID, figure=BASE_FIGURE,style={'height': '100vh', 'width': '100%'})

class Point():
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

class MachinePlotter:
  def __init__(self):
      pass

  @staticmethod
  def update(fig, quaternion=None):
      MachinePlotter._draw_machine(fig, quaternion)
      MachinePlotter._draw_scene(fig, quaternion)

  @staticmethod
  def change_camera_view(fig, camera):
      # camera = { 'up': {'x': 0, 'y': 0, 'z': 0},
      #        'center': {'x': 0, 'y': 0, 'z': 0},
      #           'eye': {'x': 0, 'y': 0, 'z': 0)}}
      fig["layout"]["scene"]["camera"] = camera

  @staticmethod
  def _draw_machine(fig, quaternion=None):
    body_idx = 0
    legs_idx = [4,5,6,7,8,9]
    # quaternion[0] = 1.0 # setting w to 1
    q = Quaternion(quaternion)
    # # Body
    #   points = machine.body.vertices + [machine.body.vertices[0]]
    #   points = []
    #   points.append(Point(0,0,0))
    #   points.append(Point(0,10,0))
    #   points.append(Point(0,10,10))
    #   # Body Surface Mesh
    #   fig["data"][0]["x"] = [point[] for point in points]
    #   fig["data"][0]["y"] = [point.y for point in points]
    #   fig["data"][0]["z"] = [point.z for point in points]

    # Body Outline
    # points_xyz = [p for p in zip(fig["data"][body_idx]["x"], fig["data"][body_idx]["y"], fig["data"][body_idx]["z"])]
    # print(points_xyz)
    # print(points_xyz)
    axes = ["x", "y", "z"]
    for data_idx in range(0, len(fig["data"])):
        for i in range(0, 3):
          axis = axes[i]
          fig["data"][data_idx][axis] = deepcopy(BASE_FIGURE["data"][data_idx][axis])
        points_xyz = [p for p in zip(fig["data"][data_idx]["x"], fig["data"][data_idx]["y"], fig["data"][data_idx]["z"])]
        # print(f"PRE: {points_xyz}")
        points_xyz = [q.rotate(p) for p in points_xyz]
        # print(f"POST: {points_xyz}\n")
        for i in range(0, 3):
          axis = axes[i]
          fig["data"][data_idx][axis] = [p[i] for p in points_xyz]

    #   fig["data"][2]["x"] = [machine.body.cog.x]
    #   fig["data"][2]["y"] = [machine.body.cog.y]
    #   fig["data"][2]["z"] = [machine.body.cog.z]

    #   fig["data"][3]["x"] = [machine.body.head.x]
    #   fig["data"][3]["y"] = [machine.body.head.y]
    #   fig["data"][3]["z"] = [machine.body.head.z]

    # for idx in legs_idx:
    #     fig["data"][idx]["x"] = [point.x for point in points]
    #     fig["data"][idx]["y"] = [point.y for point in points]
    #     fig["data"][idx]["z"] = [point.z for point in points]
        # print("Drawing")
        
    # for n, leg in zip(range(4, 10), machine.legs):
    #     points = leg.all_points
    #     fig["data"][n]["x"] = [point.x for point in points]
    #     fig["data"][n]["y"] = [point.y for point in points]
    #     fig["data"][n]["z"] = [point.z for point in points]

    # Machine Support Polygon
    # Draw a mesh for body contact on ground
    dz = -1  # Mesh must be slightly below ground
    # ground_contacts = machine.ground_contacts
    # fig["data"][10]["x"] = [point.x for point in ground_contacts]
    # fig["data"][10]["y"] = [point.y for point in ground_contacts]
    # fig["data"][10]["z"] = [(point.z + dz) for point in ground_contacts]

  @staticmethod
  def _draw_scene(fig, machine=None):
    # Change range of view for all axes
    #   RANGE = machine.sum_of_dimensions()
    RANGE =  400
    AXIS_RANGE = [-RANGE, RANGE]

    z_start = -10
    fig["layout"]["scene"]["xaxis"]["range"] = AXIS_RANGE
    fig["layout"]["scene"]["yaxis"]["range"] = AXIS_RANGE
    fig["layout"]["scene"]["zaxis"]["range"] = [z_start, (RANGE - z_start) * 2]

    #   axis_scale = machine.front / 2

    #   # Draw the machine local frame
    #   cog = machine.body.cog
    #   x_axis = machine.x_axis
    #   y_axis = machine.y_axis
    #   z_axis = machine.z_axis

    #   fig["data"][11]["x"] = [cog.x, cog.x + axis_scale * x_axis.x]
    #   fig["data"][11]["y"] = [cog.y, cog.y + axis_scale * x_axis.y]
    #   fig["data"][11]["z"] = [cog.z, cog.z + axis_scale * x_axis.z]

    #   fig["data"][12]["x"] = [cog.x, cog.x + axis_scale * y_axis.x]
    #   fig["data"][12]["y"] = [cog.y, cog.y + axis_scale * y_axis.y]
    #   fig["data"][12]["z"] = [cog.z, cog.z + axis_scale * y_axis.z]

    #   fig["data"][13]["x"] = [cog.x, cog.x + axis_scale * z_axis.x]
    #   fig["data"][13]["y"] = [cog.y, cog.y + axis_scale * z_axis.y]
    #   fig["data"][13]["z"] = [cog.z, cog.z + axis_scale * z_axis.z]

    #   # Scale the global coordinate frame
    #   fig["data"][14]["x"] = [0, axis_scale]
    #   fig["data"][14]["y"] = [0, 0]
    #   fig["data"][14]["z"] = [0, 0]

    #   fig["data"][15]["x"] = [0, 0]
    #   fig["data"][15]["y"] = [0, axis_scale]
    #   fig["data"][15]["z"] = [0, 0]

    #   fig["data"][16]["x"] = [0, 0]
    #   fig["data"][16]["y"] = [0, 0]
    #   fig["data"][16]["z"] = [0, axis_scale]
