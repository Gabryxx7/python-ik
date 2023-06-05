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

class CompoundModelPage:  
  def __init__(self, model, app):
    self.app = app
    self.model = model
    self.page = None
    self.joints_widgets = []
    self.pistons_widgets = []
    self.planes_widgets = []
    self.trigger = None
    self.id = f"tab-plane-{self.model.uuid}"
  
  def get_page(self):
    if self.page is None:
      for arm in self.model.arms:
        self.joints_widgets.append(JointWidget(arm.joints[0], self.app))
        
      self.joints_widgets.append(JointWidget(self.model.origin, self.app))
      for joint in self.model.joints:
        self.joints_widgets.append(JointWidget(joint, self.app))
        
      for piston in self.model.pistons:
        self.pistons_widgets.append(PistonWidget(piston, self.app))
        
      for plane in self.model.planes:
        self.planes_widgets.append(RollPitchYawWidget(plane, self.app))
      self.trigger = Trigger(self.model.uuid)
      self.page = html.Div([plw.get_widget() for plw in self.planes_widgets] + [pw.get_widget() for pw in self.pistons_widgets] + [jw.get_widget() for jw in self.joints_widgets] + [self.trigger.component], className="model-sidebar")
    return self.page
  
  def update_model(self, *joints_callbacks):
    self.model.forward_kinematics()
    # self.model.update_plane_vertices()
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
    
    for plw in self.planes_widgets:
      plw.add_callback()
      inputs.append(plw.trigger.input)
    outputs = self.trigger.output
    self.app.callback(outputs, inputs)(self.update_model)