import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
from frontend.components.trigger import Trigger

quat_components_deg = {
  'Roll': {'value': 90, 'min': 0, 'max': 180, 'res': 0.01},
  'Pitch': {'value': 90, 'min': 0, 'max': 180, 'res': 0.01},
  'Yaw': {'value': 90, 'min': 0, 'max': 180, 'res': 0.01}
}

quat_components = {
  'Roll': {'value': 0, 'min': -1, 'max': 1, 'res': 0.01},
  'Pitch': {'value': 0, 'min': -1, 'max': 1, 'res': 0.01},
  'Yaw': {'value': 0, 'min': -1, 'max': 1, 'res': 0.01}
}

class RollPitchYawWidget:
  def __init__(self, plane, app):
    self.app = app
    self.plane = plane
    self.widget = None
    self.label_outputs = []
    self.sliders_inputs = []
    self.sliders_outputs = []
    self.component_widgets = []
    self.component_label_states = []
    self.component_label_outputs = []
    self.trigger = None
    
  def get_widget(self):
    if self.widget is None:
      self.widget = self.make_widget()
    return self.widget
  
  def make_widget(self):
    name = self.plane.name.upper()
    j_id = self.plane.uuid
    color = "inherit" if self.plane.color is None else self.plane.color
    for key, data in quat_components.items():
      slider_id = f"quat_{j_id}_{key}"
      input_slider = dcc.Slider(data['min'], data['max'], data['res'], value=data['value'], id=slider_id, className="quat-comp-slider", marks=None, updatemode='drag', persistence=True, tooltip={"placement": "bottom", "always_visible": True})
      label_id = slider_id +"_label"
      input_label = html.Div(key.upper(), id=label_id, **{'data-name': key.upper()})
      self.sliders_inputs.append(Input(slider_id, 'value'))
      self.sliders_outputs.append(Output(slider_id, 'value'))
      self.component_label_outputs.append(Output(label_id, 'children'))
      self.component_label_states.append(State(label_id, 'data-name'))
      comp_widget = html.Div([input_label, input_slider], className="quat-comp-slider-container")
      self.component_widgets.append(comp_widget)
      
    reset_button = html.Button('Reset', id=f"quat-reset-{j_id}")
    self.trigger = Trigger(slider_id)
    
    self.widget = html.Div([
      html.Div([self.trigger.component] + self.component_widgets + [reset_button], className="quaternion-sliders-container"),
      html.Br()],
      style={"color":color},
      className="quaternion-widget-container")
    return self.widget
  
  def update_plane_orientation(self, *inputs):
    print("Plane RollPitchYaw UPDATE")
    # self.plane.update_plane_vertices(*inputs)
    inputs = [1.0, inputs[1], inputs[0], inputs[2] ]
    self.plane.origin.rotate(quaternion=inputs)
    return ""
  
  def add_callback(self):
    self.app.callback(self.trigger.output, self.sliders_inputs)(self.update_plane_orientation)