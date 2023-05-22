# ********************
# This module updates the figure dictionary
# that plotly uses to draw the 3d graph
# it takes in a machine model, and the figure to update
# you can also update the camera view with it by passing a camera dictionary
# ********************

class Point():
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

class MachinePlotter:
  def __init__(self):
      pass

  @staticmethod
  def update(fig, machine=None):
      MachinePlotter._draw_machine(fig)
    #   MachinePlotter._draw_scene(fig, machine)

  @staticmethod
  def change_camera_view(fig, camera):
      # camera = { 'up': {'x': 0, 'y': 0, 'z': 0},
      #        'center': {'x': 0, 'y': 0, 'z': 0},
      #           'eye': {'x': 0, 'y': 0, 'z': 0)}}
      fig["layout"]["scene"]["camera"] = camera

  @staticmethod
  def _draw_machine(fig, machine=None):
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
    fig["data"][1]["x"] = fig["data"][0]["x"]
    fig["data"][1]["y"] = fig["data"][0]["y"]
    fig["data"][1]["z"] = fig["data"][0]["z"]
    print("Drawing")

    #   fig["data"][2]["x"] = [machine.body.cog.x]
    #   fig["data"][2]["y"] = [machine.body.cog.y]
    #   fig["data"][2]["z"] = [machine.body.cog.z]

    #   fig["data"][3]["x"] = [machine.body.head.x]
    #   fig["data"][3]["y"] = [machine.body.head.y]
    #   fig["data"][3]["z"] = [machine.body.head.z]

    #   for n, leg in zip(range(4, 10), machine.legs):
    #       points = leg.all_points
    #       fig["data"][n]["x"] = [point.x for point in points]
    #       fig["data"][n]["y"] = [point.y for point in points]
    #       fig["data"][n]["z"] = [point.z for point in points]

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
    RANGE =  100
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
