import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc

quat_components = {
  'w': {'value': 1, 'min': -1, 'max': 1, 'res': 0.01},
  'x': {'value': 0, 'min': -1, 'max': 1, 'res': 0.01},
  'y': {'value': 0, 'min': -1, 'max': 1, 'res': 0.01},
  'z': {'value': 0, 'min': -1, 'max': 1, 'res': 0.01}
}

def make_slider(_slider_id, _name, _value, _min=0, _max=200, _input_resolution=1, _label=None):
  _label = _name if _label is None else _label
  input_field = dcc.Slider(_min, _max, _input_resolution, value=_value, id=_slider_id, marks=None, updatemode='drag', persistence=True, tooltip={"placement": "bottom", "always_visible": True})
  label = html.Div(_label, id=f"{_slider_id}_label", **{'data-name': _label})
  widget = dbc.Row([dbc.Col([label], width=2), dbc.Col([input_field], width=10)])
  return widget

def update_slider_label(slider_value, slider_name):
  return f"{slider_name}: {slider_value}"

def update_quaternion_string(*quat_input):
  return f"{list(quat_input)}"

def reset_quat(n_clicks):
  return [1,0,0,0]

def make_quaternion_widget(app, joint):
  name = joint.name.upper()
  j_id = joint.uuid
  color = "inherit" if joint.color is None else joint.color
  comp_widgets = []
  value_inputs = []
  value_outputs = []
  comp_label_outputs = []
  comp_label_states = []
  for key, data in quat_components.items():
    slider_id = f"quat_{j_id}_{key}"
    input_field = dcc.Slider(data['min'], data['max'], data['res'], value=data['value'], id=slider_id, marks=None, updatemode='drag', persistence=True, tooltip={"placement": "bottom", "always_visible": True})
    label_id = slider_id +"_label"
    input_label = html.Div(key.upper(), id=label_id, **{'data-name': key.upper()})
    comp_widget = dbc.Row([dbc.Col([input_label], width=2), dbc.Col([input_field], width=10)])
    comp_widgets.append(comp_widget)
    value_inputs.append(Input(slider_id, 'value'))
    value_outputs.append(Output(slider_id, 'value'))
    comp_label_outputs.append(Output(label_id, 'children'))
    comp_label_states.append(State(label_id, 'data-name'))
    
  reset_button = html.Button('Reset', id=f"quat-reset-{j_id}")
  output_string = html.Div(id=f"output-label-{j_id}",children="[]")
  
  widget = html.Div([
    html.Div([dcc.Markdown(f"** QUATERNION {name} **"), output_string], className='d-flex', style={'gap': '1rem'}),
    html.Div(comp_widgets + [reset_button],
      style={"display": "flex", "flex-direction": "column"}),
    html.Br()],
    style={"color":color})

  [app.callback(data[0], [data[1]], [data[2]])(update_slider_label) for data in zip(comp_label_outputs, value_inputs, comp_label_states)]
  app.callback(Output(f"output-label-{j_id}", 'children'), [value_inputs])(update_quaternion_string)
  app.callback(value_outputs, Input(f"quat-reset-{j_id}", 'n_clicks'))(reset_quat)
  
  return widget, [value_inputs]


# def add_quat_widget_callback(app):
#   [app.callback(Output(f"quat_{val}_label", 'children'),
#                 Input(f"quat_{val}", 'value'),
#                 State(f"quat_{val}_label", 'data-name'))
#                 (update_slider_label) for val in quat_widgets]
#   app.callback(Output('output-container-button', 'children'), [[Input(f"quat_{val}", 'value') for val in quat_widgets]])(update_quaternion_string)
#   app.callback([Output(f"quat_{val}", 'value') for val in quat_widgets],
#                [Input(f"quat-reset", 'n_clicks')])(reset_quat)

# def get_quaternion_inputs():
#   inpt = [[Input(f"quat_{_joint_id}_{val}", 'value') for val in quat_widgets]]
#   return inpt

# def add_quaternion_listener(app, callback=None, output=None, state=None):
#   callback = update_quaternion_string if callback is None else callback
#   output = Output('output-container-button', 'children') if output is None else output
#   inpt = [[Input(f"quat_{_joint_id}_{val}", 'value') for val in quat_widgets]]
#   if state is not None:
#     app.callback(output, inpt, state)(callback)
#   else:
#     app.callback(output, inpt)(callback)
  