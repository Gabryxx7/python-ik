import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc

DARKMODE = True

NUMBER_INPUT_STYLE = {
    "marginRight": "5%",
    "width": "95%",
    "marginBottom": "5%",
    "borderRadius": "10px",
    "border": "solid 1px",
    "fontFamily": "Courier New",
}

if DARKMODE:
    NUMBER_INPUT_STYLE["backgroundColor"] = "#2c3e50"
    NUMBER_INPUT_STYLE["color"] = "#2ecc71"
    NUMBER_INPUT_STYLE["borderColor"] = "#2980b9"

def make_piston_widget(piston_id, _name, _value, _min=0, _max=200, _input_resolution=1, _label=None, _type="slider"):
  _label = _name if _label is None else _label
  if _type == "slider":
    input_field = dcc.Slider(_min, _max, _input_resolution, value=_value, id=piston_id, marks=None, updatemode='drag',
                             persistence=True,
                             tooltip={"placement": "bottom", "always_visible": True})
  label = html.Div(_label, id=f"{piston_id}_label", **{'data-name': _label})
  widget = dbc.Row([dbc.Col([label], width=2), dbc.Col([input_field], width=10)], style={'width': '100%'})
  inpt = Input(piston_id, "value")
  return widget, inpt

# quat_comp_widgets = [make_number_widget(f"quat_{val}", 0 if val!="w" else 1, _min=-1, _max=1, _input_resolution=0.05, _label=val.upper()) for val in quat_widgets]
# quaternion_widget = html.Div([
#   html.Label(dcc.Markdown(f"** QUATERNIONS **")),
#   html.Div(
#       quat_comp_widgets+
#       [html.Button('Reset', id='quat-reset'),
#        html.Div(id='output-container-button',children="[]")],
#     style={"display": "flex", "flex-direction": "column"}),
#   html.Br()])

def add_piston_slider_listener(app, piston_id, callback, output, state):
  inpt = Input(piston_id, 'value')
  if state is not None:
    app.callback(output, inpt, state)(callback)
  else:
    app.callback(output, inpt)(callback)
  