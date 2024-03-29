import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
from frontend.dash.components.trigger import Trigger

quat_components_deg = {
  'Roll': {'value': 0, 'min': -90, 'max': 90, 'res': 0.01, 'enabled': True},
  'Pitch': {'value': 0, 'min': -90, 'max': 90, 'res': 0.01, 'enabled': True},
  'Yaw': {'value': 0, 'min': -90, 'max': 90, 'res': 0.01, 'enabled': True}
}

quat_components = {
  'Roll': {'value': 0, 'min': -1, 'max': 1, 'res': 0.01, 'enabled': True},
  'Pitch': {'value': 0, 'min': -1, 'max': 1, 'res': 0.01, 'enabled': True},
  'Yaw': {'value': 0, 'min': -1, 'max': 1, 'res': 0.01, 'enabled': True}
}

class RollPitchYawWidget:
  def __init__(self, plane, app, yaw_enabled=True):
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
    self.yaw_enabled = yaw_enabled
    
  def get_widget(self):
    if self.widget is None:
      self.widget = self.make_widget()
    return self.widget
  
  def make_widget(self):
    name = self.plane.name.upper()
    j_id = self.plane.uuid
    color = "inherit" if self.plane.color is None else self.plane.color
    for key, data in quat_components_deg.items():
      if key == 'Yaw':
        data['enabled'] = self.yaw_enabled
      slider_id = f"quat_{j_id}_{key}"
      input_slider = dcc.Slider(data['min'], data['max'], data['res'], value=data['value'], id=slider_id, className="quat-comp-slider", marks=None, updatemode='drag', persistence=True, tooltip={"placement": "bottom", "always_visible": True})
      label_id = slider_id +"_label"
      input_label = html.Div(key.upper(), id=label_id, **{'data-name': key.upper()})
      if data['enabled']:
        self.sliders_inputs.append(Input(slider_id, 'value'))
      self.sliders_outputs.append(Output(slider_id, 'value'))
      self.component_label_outputs.append(Output(label_id, 'children'))
      self.component_label_states.append(State(label_id, 'data-name'))
      disabled_class = "disabled" if not data['enabled'] else ""
      comp_widget = html.Div([input_label, input_slider], className=f"quat-comp-slider-container {disabled_class}")
      self.component_widgets.append(comp_widget)
      
    reset_button = html.Button('Reset', id=f"quat-reset-{j_id}")
    self.trigger = Trigger(slider_id)
    
    self.widget = html.Div([
      html.Div([self.trigger.component] + self.component_widgets + [reset_button], className="quaternion-sliders-container"),
      html.Br()],
      style={"color":color},
      className="pistons-widget-container")
    return self.widget
  
  def update_plane_orientation(self, *inputs):
    w = 0.0
    alpha = inputs[1]
    beta = inputs[0]
    gamma = inputs[2] if len(inputs) > 2 else 0
    quat = [alpha, beta, gamma]
    self.plane.rotate(quat)
    return ""
  
  def add_callback(self):
    self.app.callback(self.trigger.output, self.sliders_inputs)(self.update_plane_orientation)