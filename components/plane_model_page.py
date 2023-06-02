import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
from components.joint_widget import JointWidget
from components.piston_widget import PistonWidget
from components.trigger import Trigger
from components.roll_pitch_yaw_widget import RollPitchYawWidget

CONTAINER_STYLE = {'display': 'flex', 'flex-direction': 'column'}

class PlaneModelPage:  
  def __init__(self, plane, app):
    self.app = app
    self.plane = plane
    self.page = None
    self.joints_widgets = []
    self.pistons_widgets = []
    self.orientation_widget = None
    self.trigger = None
    self.id = f"tab-plane-{self.plane.uuid}"
  
  def get_page(self):
    if self.page is None:
      for arm in self.plane.arms:
        self.joints_widgets.append(JointWidget(arm.joints[0], self.app))
      for piston in self.plane.pistons:
        self.pistons_widgets.append(PistonWidget(piston, self.app))
      self.orientation_widget = RollPitchYawWidget(self.plane, self.app)
      self.trigger = Trigger(self.plane.uuid)
      self.page = html.Div([self.orientation_widget.get_widget()] + [pw.get_widget() for pw in self.pistons_widgets] + [jw.get_widget() for jw in self.joints_widgets] + [self.trigger.component], className="model-sidebar")
    return self.page
  
  def update_plane(self, *joints_callbacks):
    # self.plane.forward_kinematics()
    # self.plane.update_plane_vertices()
    return ""
  
  def add_callback(self):
    print("Adding plane callbacks")
    inputs = []
    for jw in self.joints_widgets:
      jw.add_callback()
      inputs.append(jw.trigger.input)
    
    for pw in self.pistons_widgets:
      pw.add_callback()
      inputs.append(pw.trigger.input)
    
    self.orientation_widget.add_callback()
    inputs.append(self.orientation_widget.trigger.input)
    outputs = self.trigger.output
    self.app.callback(outputs, inputs)(self.update_plane)