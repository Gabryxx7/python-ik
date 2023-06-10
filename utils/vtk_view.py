import random

import dash
import dash_vtk
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State


VTK_SLIDER_ID = "slider-resolution"
VTK_CHECKLIST_ID = "capping-checklist"
VTK_ID = "vtk-kinematics"
VTK_ALG_ID = "vtk-algorithm"

interactorSettings=[
  {
    'button': 1,
    'action': 'Rotate',
  }, {
    'button': 2,
    'action': 'Pan',
  }, {
    'button': 3,
    'action': 'Zoom',
    'scrollEnabled': True,
  }, {
    'button': 1,
    'action': 'Pan',
    'shift': True,
  }, {
    'button': 1,
    'action': 'Zoom',
    'alt': True,
  }, {
    'button': 1,
    'action': 'ZoomToMouse',
    'control': True,
  }, {
    'button': 1,
    'action': 'Roll',
    'alt': True,
    'shift': True,
  }
]

# Add hover info: https://github.com/plotly/dash-vtk/blob/master/demos/pyvista-terrain-following-mesh/app.py
# https://dash.plotly.com/vtk/click-hover

# DARK_BG_HTML = #222f3e
# DARK_BG_RGB = [34/255, 47/255, 62/255]

default_geom_objs = [
  {
    'id':'line2',
    'vtkClass': 'vtkLineSource',
    'color': [0,0,1],
    'state': {
      'point1': [-0.5, 1, 1],
      'point2': [5, 0, 1],
      'resolution': 60
    }
  },
  {
    'id':'line1',
    'vtkClass': 'vtkLineSource',
    'color': [1,0,0],
    'state': {
      'point1': [-1, 1, 0],
      'point2': [-5, 0, 1],
      'resolution': 60
    }
  },
]

bounds = 500
orientation = [45,0,45]

def get_vtk_view(geom_objs):
  # geom_objs = default_geom_objs
  geoms = []
  for geom_obj in geom_objs:
    actor = geom_obj.get('actor', {})
    properties = geom_obj.get('property', {})
    state = geom_obj.get('state', {})
    properties["edgeVisibility"] = True
    properties["lineWidth"] = 10
    # print(f"Appending geom {geom_obj}")
    geom_alg = dash_vtk.Algorithm(
                id=geom_obj['id'],
                vtkClass=geom_obj['vtkClass'],
                # state={'point1': geom_obj['state']['point1'], 'point2': geom_obj['state']['point2'], 'resolution': geom_obj['state']['resolution']},
                state=state,
            )
    # geoms.append(geom_alg)
    geom_container = dash_vtk.GeometryRepresentation(
          id="repr_"+geom_obj['id'],
          children=[geom_alg],
          actor=actor,
          property=properties
        )
    geoms.append(geom_container)


  axis_geom_placeholder = dash_vtk.Algorithm(
                id="test",
                vtkClass="vtkCubeSource",
                state={
                  'xLength': bounds,
                  'yLength': bounds,
                  'zLength': bounds,
                  'center':  [0,0,bounds/2]})
  geoms.append(dash_vtk.GeometryRepresentation(
            id="vtk-axis",
            children=[axis_geom_placeholder],
            mapper={'scalarRange': [-bounds,bounds]},
            actor={
              # 'orientation': orientation
              # 'position': [0,-bounds/2,0],
              # 'origin': [0,-bounds/2, 0]
            },
            property={
              'opacity': 0
            },
            showCubeAxes=True,
            cubeAxesStyle={
              "gridLines": True,
              "axisLabels": ["X", "Y", "Z"],
              "axisTitlePixelOffset": 50.0,
              "axisTextStyle": {
                'fontColor': '#079992',
                'fontStyle': 'bold',
                'fontSize': 16,
                'fontFamily': 'Fira Code'
              },
              "tickLabelPixelOffset": 20.0,
              "tickTextStyle": {
                'fontColor': '#079992',
                'fontStyle': 'normal',
                'fontSize': 12,
                'fontFamily': 'Fira Code'
              },
            },
        ))
    
  vtk_view = dash_vtk.View(
      id=VTK_ID,
      background=[34/255, 47/255, 62/255], 
      pickingModes=["click"],
      children=geoms,
      cameraPosition=[0.9,0.9,0.25],
      cameraViewUp=[0,0,1],
      interactorSettings=interactorSettings
  )

  # vtk_controls = dbc.Card(
  #   [
  #     dbc.CardHeader("Controls"),
  #     dbc.CardBody(
  #         [
  #             html.P("Resolution:"),
  #             dcc.Slider(
  #                 id=VTK_SLIDER_ID,
  #                 min=10,
  #                 max=100,
  #                 step=1,
  #                 value=60,
  #                 marks={10: "10", 100: "100"},
  #             ),
  #             html.Br(),
  #             dbc.Checklist(
  #                 options=[{"label": "Capping", "value": "capping"}],
  #                 value=[],
  #                 id=VTK_CHECKLIST_ID,
  #                 switch=True,
  #             ),
  #         ]
  #     ),
  #   ]
  # )
  return vtk_view
