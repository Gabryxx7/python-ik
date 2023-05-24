from style_settings import (
    BODY_MESH_COLOR,
    BODY_MESH_OPACITY,
    BODY_COLOR,
    BODY_OUTLINE_WIDTH,
    COG_COLOR,
    COG_SIZE,
    HEAD_SIZE,
    LEG_COLOR,
    LEG_OUTLINE_WIDTH,
    SUPPORT_POLYGON_MESH_COLOR,
    SUPPORT_POLYGON_MESH_OPACITY,
    LEGENDS_BG_COLOR,
    AXIS_ZERO_LINE_COLOR,
    PAPER_BG_COLOR,
    GROUND_COLOR,
    LEGEND_FONT_COLOR,
)
MARKER_SIZE = 15

X_AXIS = 0
Y_AXIS = 1
Z_AXIS = 2

model_structure = {
  "plane": {
    "parts": ["plane"]
  },
  "arm_1": {
    "parts": ["arm_1_piston", "arm_1_arm"]
  }
}

PISTON_HEIGHT = 200.0
PLANE_INITIAL_HEIGHT = PISTON_HEIGHT*1.5
V1 = [100.0, 100.0, PLANE_INITIAL_HEIGHT]
ARM1_XY = [V1[0]+25, V1[1]]
V2 = [-100.0, 100.0, PLANE_INITIAL_HEIGHT]
ARM2_XY = [V2[0]-25, V2[1]]
V3 = [0.0, -100.0, PLANE_INITIAL_HEIGHT*0.7]
ARM3_XY = [V3[0], V3[1]-25]

models_vertices = {
  "plane": [
      V1,
      V2,
      V3,
      V1
    ],
  "arm_1_piston": [
      [ARM1_XY[0], ARM1_XY[1], 0.0],
      [ARM1_XY[0], ARM1_XY[1], PISTON_HEIGHT],
    ],
  "arm_1_arm": [
      [ARM1_XY[0], ARM1_XY[1], PISTON_HEIGHT*0.5],
      [V1[0], V1[1], V1[2]],
    ],
  "arm_2_piston": [
      [ARM2_XY[0], ARM2_XY[1], 0.0],
      [ARM2_XY[0], ARM2_XY[1], PISTON_HEIGHT],
    ],
  "arm_2_arm": [
      [ARM2_XY[0], ARM2_XY[1], PISTON_HEIGHT*0.5],
      [V2[0], V2[1], V2[2]],
    ],
  "arm_3_piston": [
      [ARM3_XY[0], ARM3_XY[1], 0.0],
      [ARM3_XY[0], ARM3_XY[1], PISTON_HEIGHT],
    ],
  "arm_3_arm": [
      [ARM3_XY[0], ARM3_XY[1], PISTON_HEIGHT*0.5],
      [V3[0], V3[1], V3[2]],
    ]
}

new_data = [
  {
    "name": "body mesh",
    "showlegend": True,
    "type": "mesh3d",
    "opacity": BODY_MESH_OPACITY,
    "color": BODY_MESH_COLOR,
    "x": [p[X_AXIS] for p in models_vertices['plane']],
    "y": [p[Y_AXIS] for p in models_vertices['plane']],
    "z": [p[Z_AXIS] for p in models_vertices['plane']],
  },
  {
    "line": {"color": BODY_COLOR, "opacity": 0.8, "width": BODY_OUTLINE_WIDTH},
    "name": "body",
    "showlegend": True,
    "mode": "lines",
    "type": "scatter3d",
    "x": [p[X_AXIS] for p in models_vertices['plane']],
    "y": [p[Y_AXIS] for p in models_vertices['plane']],
    "z": [p[Z_AXIS] for p in models_vertices['plane']]
  },
  {
    "line": {"color": LEG_COLOR, "width": LEG_OUTLINE_WIDTH*2},
    "mode": "lines",
    "name": "Leg 1",
    "showlegend": False,
    "type": "scatter3d",
    "legendgroup": "Leg 1",
    "x": [p[X_AXIS] for p in models_vertices['arm_1_piston']],
    "y": [p[Y_AXIS] for p in models_vertices['arm_1_piston']],
    "z": [p[Z_AXIS] for p in models_vertices['arm_1_piston']]
  },
  {
    "line": {"color": LEG_COLOR, "opacity": 1.0, "width": LEG_OUTLINE_WIDTH},
    "marker": {"size": MARKER_SIZE},
    "name": "Leg_1_arm",
    "mode": "lines+markers",
    "showlegend": False,
    "type": "scatter3d",
    "legendgroup": "Leg 1",
    "x": [p[X_AXIS] for p in models_vertices['arm_1_arm']],
    "y": [p[Y_AXIS] for p in models_vertices['arm_1_arm']],
    "z": [p[Z_AXIS] for p in models_vertices['arm_1_arm']]
  },
  {
    "line": {"color": LEG_COLOR, "width": LEG_OUTLINE_WIDTH*2},
    "mode": "lines",
    "name": "Leg 2",
    "showlegend": False,
    "type": "scatter3d",
    "legendgroup": "Leg 2",
    "x": [p[X_AXIS] for p in models_vertices['arm_2_piston']],
    "y": [p[Y_AXIS] for p in models_vertices['arm_2_piston']],
    "z": [p[Z_AXIS] for p in models_vertices['arm_2_piston']]
  },
  {
    "line": {"color": LEG_COLOR, "opacity": 1.0, "width": LEG_OUTLINE_WIDTH},
    "marker": {"size": MARKER_SIZE},
    "name": "Leg_2_arm",
    "mode": "lines+markers",
    "showlegend": False,
    "type": "scatter3d",
    "legendgroup": "Leg 2",
    "x": [p[X_AXIS] for p in models_vertices['arm_2_arm']],
    "y": [p[Y_AXIS] for p in models_vertices['arm_2_arm']],
    "z": [p[Z_AXIS] for p in models_vertices['arm_2_arm']]
  },
  {
    "line": {"color": LEG_COLOR, "width": LEG_OUTLINE_WIDTH*2},
    "mode": "lines",
    "name": "Leg 3",
    "showlegend": False,
    "type": "scatter3d",
    "legendgroup": "Leg 3",
    "x": [p[X_AXIS] for p in models_vertices['arm_3_piston']],
    "y": [p[Y_AXIS] for p in models_vertices['arm_3_piston']],
    "z": [p[Z_AXIS] for p in models_vertices['arm_3_piston']]
  },
  {
    "line": {"color": LEG_COLOR, "opacity": 1.0, "width": LEG_OUTLINE_WIDTH},
    "marker": {"size": MARKER_SIZE},
    "name": "Leg_3_arm",
    "mode": "lines+markers",
    "showlegend": False,
    "type": "scatter3d",
    "legendgroup": "Leg 3",
    "x": [p[X_AXIS] for p in models_vertices['arm_3_arm']],
    "y": [p[Y_AXIS] for p in models_vertices['arm_3_arm']],
    "z": [p[Z_AXIS] for p in models_vertices['arm_3_arm']]
  },
  {
      "line": {"color": "#e64722", "width": 2},
      "name": "x direction",
      "showlegend": False,
      "mode": "lines",
      "opacity": 1.0,
      "type": "scatter3d",
      "x": [0, 200],
      "y": [0, 0],
      "z": [0, 0],
  },
  {
      "line": {"color": "#4de622", "width": 2},
      "name": "y direction",
      "showlegend": False,
      "mode": "lines",
      "opacity": 1.0,
      "type": "scatter3d",
      "x": [0, 0],
      "y": [0, 200],
      "z": [0, 0],
  },
  {
      "line": {"color": "#2284e6", "width": 2},
      "name": "z direction",
      "showlegend": False,
      "mode": "lines",
      "opacity": 1.0,
      "type": "scatter3d",
      "x": [0, 0],
      "y": [0, 0],
      "z": [0, 200],
  },
]

HEXAPOD_FIGURE = {
    "data": new_data,
    "layout": {
        "paper_bgcolor": PAPER_BG_COLOR,
        "hovermode": "closest",
        "legend": {
            "x": 0,
            "y": 0,
            "bgcolor": LEGENDS_BG_COLOR,
            "font": {"family": "courier", "size": 12, "color": LEGEND_FONT_COLOR},
        },
        "margin": {"b": 20, "l": 10, "r": 10, "t": 20},
        "scene": {
            "aspectmode": "manual",
            "aspectratio": {"x": 1, "y": 1, "z": 1},
            "camera": {
                "center": {
                    "x": 0.0348603742736399,
                    "y": 0.16963779995083,
                    "z": -0.394903376555686,
                },
                "eye": {
                    "x": 0.193913968006015,
                    "y": 0.45997575676993,
                    "z": -0.111568465000231,
                },
                "up": {"x": 0, "y": 0, "z": 1},
            },
            "xaxis": {
                "nticks": 1,
                "range": [-100, 100],
                "zerolinecolor": AXIS_ZERO_LINE_COLOR,
                "showbackground": False,
            },
            "yaxis": {
                "nticks": 1,
                "range": [-100, 100],
                "zerolinecolor": AXIS_ZERO_LINE_COLOR,
                "showbackground": False,
            },
            "zaxis": {
                "nticks": 1,
                "range": [0, 200],
                "zerolinecolor": AXIS_ZERO_LINE_COLOR,
                "showbackground": True,
                "backgroundcolor": GROUND_COLOR,
            },
        },
    },
}
