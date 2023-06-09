import os
import json
from figure_template import HEXAPOD_FIGURE, VTest_1, VTest_2, VTest_3, models_vertices
BASE_FIGURE = HEXAPOD_FIGURE

class PlotlyPlotter:
  def __init__(self):
    pass

  @staticmethod
  def export_trace(figure, logs_path="./logs/", postfix=""):
    if not os.path.exists(logs_path):
      os.makedirs(logs_path)
    postfix = f"_{postfix}" if postfix != "" else ""
    with open(f"trace_log{postfix}.json", "w") as f:
      json.dump(figure, f, indent=2)
      
  @staticmethod
  def change_camera_view(fig, relayout_data):
    if relayout_data and "scene.camera" in relayout_data:
        camera = relayout_data["scene.camera"]
        fig["layout"]["scene"]["camera"] = camera

  @staticmethod
  def _draw_scene(fig, machine=None):
    # Change range of view for all axes
    #   RANGE = machine.sum_of_dimensions()
    RANGE = 700
    AXIS_RANGE = [-RANGE, RANGE]

    z_start = -10
    fig["layout"]["scene"]["xaxis"]["range"] = AXIS_RANGE
    fig["layout"]["scene"]["yaxis"]["range"] = AXIS_RANGE
    fig["layout"]["scene"]["zaxis"]["range"] = [z_start, (RANGE - z_start) * 2]
