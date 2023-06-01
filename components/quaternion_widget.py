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

class QuaternionWidget:
  def __init__(self, joint, app):
    self.app = app
    self.joint = joint
    self.widget = None
    self.label_outputs = []
    self.sliders_inputs = []
    self.sliders_outputs = []
    self.callback_output = None
    self.component_widgets = []
    self.component_label_states = []
    self.component_label_outputs = []
    
  def get_widget(self):
    if self.widget is None:
      self.widget = self.make_widget()
    return self.widget
  
  def make_widget(self):
    name = self.joint.name.upper()
    j_id = self.joint.uuid
    color = "inherit" if self.joint.color is None else self.joint.color
    for key, data in quat_components.items():
      slider_id = f"quat_{j_id}_{key}"
      input_field = dcc.Slider(data['min'], data['max'], data['res'], value=data['value'], id=slider_id, marks=None, updatemode='drag', persistence=True, tooltip={"placement": "bottom", "always_visible": True})
      label_id = slider_id +"_label"
      input_label = html.Div(key.upper(), id=label_id, **{'data-name': key.upper()})
      self.sliders_inputs.append(Input(slider_id, 'value'))
      self.sliders_outputs.append(Output(slider_id, 'value'))
      self.component_label_outputs.append(Output(label_id, 'children'))
      self.component_label_states.append(State(label_id, 'data-name'))
      comp_widget = dbc.Row([dbc.Col([input_label], width=2), dbc.Col([input_field], width=10)])
      self.component_widgets.append(comp_widget)
      
    reset_button = html.Button('Reset', id=f"quat-reset-{j_id}")
    callback_out_id = slider_id +"_cb_out"
    callback_out = html.Div("", id=callback_out_id, style={'display': 'none'})
    self.callback_output = Output(callback_out_id, 'children')
    
    self.widget = html.Div([
      html.Div([dcc.Markdown(f"** QUATERNION {name} **"), callback_out], className='d-flex', style={'gap': '1rem'}),
      html.Div(self.component_widgets + [reset_button],
        style={"display": "flex", "flex-direction": "column"}),
      html.Br()],
      style={"color":color, 'width': '50%'})
    return self.widget
  

  def update_slider_label(slider_value, slider_name):
    return f"{slider_name}: {slider_value}"

  def update_quaternion_string(*quat_input):
    return f"{list(quat_input)}"

  def reset_quat(n_clicks):
    return [1,0,0,0]
