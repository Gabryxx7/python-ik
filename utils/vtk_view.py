import random

import dash
import dash_vtk
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State


VTK_SLIDER_ID = "slider-resolution"
VTK_CHECKLIST_ID = "capping-checklist"
VTK_ID = "vtk-kinematics"
VTK_ALG_ID = "vvtk-algorithm"

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
vtk_view = dash_vtk.View(
    id=VTK_ID,
    background=[34/255, 47/255, 62/255], 
    pickingModes=["click"],
    children=[
        dash_vtk.GeometryRepresentation(
            [
                dash_vtk.Algorithm(
                    id=VTK_ALG_ID,
                    vtkClass="vtkConeSource",
                    state={"capping": False, "resolution": 60},
                )
            ]
        )
    ],
    interactorSettings=interactorSettings,
)
vtk_controls = dbc.Card(
  [
    dbc.CardHeader("Controls"),
    dbc.CardBody(
        [
            html.P("Resolution:"),
            dcc.Slider(
                id=VTK_SLIDER_ID,
                min=10,
                max=100,
                step=1,
                value=60,
                marks={10: "10", 100: "100"},
            ),
            html.Br(),
            dbc.Checklist(
                options=[{"label": "Capping", "value": "capping"}],
                value=[],
                id=VTK_CHECKLIST_ID,
                switch=True,
            ),
        ]
    ),
  ]
)
