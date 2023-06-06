from copy import deepcopy
import uuid

# ***************************************
# COLORS
# ***************************************

DARKMODE = True


BODY_MESH_COLOR = "#ff6348"
BODY_MESH_OPACITY = 0.3
BODY_COLOR = "#FC427B"
COG_COLOR = "#32ff7e"
LEG_COLOR = "#EE5A24"  # "#b71540"
SUPPORT_POLYGON_MESH_COLOR = "#3c6382"
SUPPORT_POLYGON_MESH_OPACITY = 0.2
LEGENDS_BG_COLOR = "rgba(44, 62, 80, 0.8)"
AXIS_ZERO_LINE_COLOR = "#079992"
PAPER_BG_COLOR = "#222f3e"
GROUND_COLOR = "#0a3d62"
LEGEND_FONT_COLOR = "#2ecc71"

if not DARKMODE:
    BODY_MESH_COLOR = "#8e44ad"
    BODY_MESH_OPACITY = 0.9
    BODY_COLOR = "#8e44ad"
    COG_COLOR = "#2c3e50"
    HEAD_COLOR = "#8e44ad"
    LEG_COLOR = "#2c3e50"
    SUPPORT_POLYGON_MESH_COLOR = "#ffa801"
    SUPPORT_POLYGON_MESH_OPACITY = 0.3
    LEGENDS_BG_COLOR = "rgba(255, 255, 255, 0.5)"
    AXIS_ZERO_LINE_COLOR = "#ffa801"
    PAPER_BG_COLOR = "white"
    GROUND_COLOR = "rgb(240, 240, 240)"
    LEGEND_FONT_COLOR = "#34495e"

BODY_OUTLINE_WIDTH = 12
LEG_OUTLINE_WIDTH = 15
COG_SIZE = 14
HEAD_SIZE = 14
MARKER_SIZE = 15

X, Y, Z = 0,1,2
AXIS_ORDER_CONVENTION = [X, Y, Z]
# Angles and positions constraints follow the same convention above from AXIS_ORDER_CONVENTION

default_traces = {
  "plane": {
    "name": "Plane",
    "showlegend": True,
    "type": "mesh3d",
    "mode": "lines+markers",
    "opacity": 0.5,
    "color": "#ff6348",
    "x": [],
    "y": [],
    "z": []
  },
  "joint": {
    "name": "Joint",
    "line": {"color": "#2284e6", "width": LEG_OUTLINE_WIDTH},
    "marker": {"size": MARKER_SIZE},
    "mode": "lines+markers",
    "showlegend": False,
    "type": "scatter3d",
    "x": [0],
    "y": [0],
    "z": [0]
  },
  "axis": {
    "name": "Axis",
    "line": {"color": "#2284e6", "width": LEG_OUTLINE_WIDTH},
    "marker": {"size": MARKER_SIZE},
    "mode": "lines+markers",
    "showlegend": False,
    "type": "scatter3d",
    "x": [0],
    "y": [0],
    "z": [0]
  }
}
