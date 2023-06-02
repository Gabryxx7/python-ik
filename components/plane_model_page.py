import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
from components.joint_widget import JointWidget
from components.piston_widget import PistonWidget
from components.trigger import Trigger

CONTAINER_STYLE = {'display': 'flex', 'flex-direction': 'column'}

class PlaneModelPage:  
  def __init__(self, plane, app):
    self.app = app
    self.plane = plane
    self.page = None
    self.joints_widgets = []
    self.pistons_widgets = []
    self.trigger = None
  
  def get_page(self):
    if self.page is None:
      for arm in self.plane.arms:
        self.joints_widgets.append(JointWidget(arm.joints[0], self.app))
      for piston in self.plane.pistons:
        self.pistons_widgets.append(PistonWidget(piston, self.app))
      self.trigger = Trigger(self.plane.uuid)
      self.page = html.Div([pw.get_widget() for pw in self.pistons_widgets] + [jw.get_widget() for jw in self.joints_widgets] + [self.trigger.component], className="model-sidebar")
    return self.page
  
  def update_plane(self, *joints_callbacks):
    self.plane.forward_kinematics()
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
    outputs = self.trigger.output
    self.app.callback(outputs, inputs)(self.update_plane)