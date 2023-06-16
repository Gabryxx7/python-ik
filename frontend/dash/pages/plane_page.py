import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
from frontend.dash.widgets.joint_widget import JointWidget
from frontend.dash.widgets.piston_widget import PistonWidget
from frontend.dash.widgets.roll_pitch_yaw_widget import RollPitchYawWidget
from frontend.dash.components.trigger import Trigger

CONTAINER_STYLE = {'display': 'flex', 'flex-direction': 'column'}

class PlanePage:  
  def __init__(self, model, app, label="Plane"):
    self.label = label
    self.app = app
    self.model = model
    self.page = None
    self.joints_widgets = []
    self.plane_widget = None
    self.trigger = None
    self.id = f"tab-{self.model.uuid}"
  
  def get_page(self):
    if self.page is None:        
      self.plane_widget = RollPitchYawWidget(self.model, self.app)
      self.trigger = Trigger(self.id)
      self.page = html.Div([self.plane_widget.get_widget()] + [jw.get_widget() for jw in self.joints_widgets] + [self.trigger.component], className="model-sidebar")
    return self.page
  
  def update_plane(self, *joints_callbacks):
    self.model.forward_kinematics()
    return ""
  
  def add_callback(self):
    inputs = []
    for jw in self.joints_widgets:
      jw.add_callback()
      inputs.append(jw.trigger.input)
    self.plane_widget.add_callback()
    inputs.append(self.plane_widget.trigger.input)
    outputs = self.trigger.output
    self.app.callback(outputs, inputs)(self.update_plane)