import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
from components.joint_widget import JointWidget
from components.trigger import Trigger

class ArmPage:  
  def __init__(self, model, app):
    self.app = app
    self.model = model
    self.page = None
    self.joints_widgets = []
    self.trigger = None
  
  def get_page(self):
    if self.page is None:
      for joint in self.model.joints:
        self.joints_widgets.append(JointWidget(joint, self.app))
      self.trigger = Trigger(self.model.uuid)
      self.page = html.Div([jw.get_widget() for jw in self.joints_widgets]+[self.trigger.component], className="model-sidebar")
    return self.page
  
  def update_arm(self, *joints_callbacks):
    self.model.forward_kinematics()
    return ""
  
  def add_callback(self):
    print("Adding arm callbacks")
    inputs = []
    for jw in self.joints_widgets:
      jw.add_callback()
      inputs.append(jw.trigger.input)
    outputs = self.trigger.output
    self.app.callback(outputs, inputs)(self.update_arm)