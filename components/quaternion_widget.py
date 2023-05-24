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


quat_widgets = ["w", "x", "y", "z"]

def make_number_widget(_name, _value, _min=0, _max=200, _input_resolution=1, _label=None, _type="slider"):
  _label = _name if _label is None else _label
  if _type == "slider":
    input_field = dcc.Slider(_min, _max, _input_resolution, value=_value, id=_name, marks=None, updatemode='drag',
                             persistence=True,
                             tooltip={"placement": "bottom", "always_visible": True})
  else:
    input_field = dcc.Input(
      id=_name,
      type="number",
      value=_value,
      min=_min,
      max=_max,
      step=_input_resolution,
      marks=None
      # style=NUMBER_INPUT_STYLE,
    )
  label = html.Div(_label, id=f"{_name}_label", **{'data-name': _label})
  return dbc.Row([dbc.Col([label], width=2), dbc.Col([input_field], width=10)])

quat_comp_widgets = [make_number_widget(f"quat_{val}", 0 if val!="w" else 1, _min=-1, _max=1, _input_resolution=0.05, _label=val.upper()) for val in quat_widgets]
quaternion_widget = html.Div([
  html.Label(dcc.Markdown(f"** QUATERNIONS **")),
  html.Div(
      quat_comp_widgets+
      [html.Button('Reset', id='quat-reset'),
       html.Div(id='output-container-button',children="[]")],
    style={"display": "flex", "flex-direction": "column"}),
  html.Br()])

def update_slider_label(slider_value, slider_name):
  return f"{slider_name}: {slider_value}"

def update_quaternion_string(*quat_input):
  return f"{list(quat_input)}"

def reset_quat(n_clicks):
  return [1,0,0,0]

def add_quat_widget_callback(app):
  [app.callback(Output(f"quat_{val}_label", 'children'),
                Input(f"quat_{val}", 'value'),
                State(f"quat_{val}_label", 'data-name'))
                (update_slider_label) for val in quat_widgets]
  app.callback(Output('output-container-button', 'children'), [[Input(f"quat_{val}", 'value') for val in quat_widgets]])(update_quaternion_string)
  app.callback([Output(f"quat_{val}", 'value') for val in quat_widgets],
               [Input(f"quat-reset", 'n_clicks')])(reset_quat)
  
def add_quaternion_listener(app, callback=None, output=None, state=None):
  callback = update_quaternion_string if callback is None else callback
  output = Output('output-container-button', 'children') if output is None else output
  inpt = [[Input(f"quat_{val}", 'value') for val in quat_widgets]]
  if state is not None:
    app.callback(output, inpt, state)(callback)
  else:
    app.callback(output, inpt)(callback)
  