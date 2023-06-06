import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
from frontend.widgets.joint_widget import JointWidget
from frontend.widgets.piston_widget import PistonWidget
from frontend.components.trigger import Trigger
from frontend.widgets.roll_pitch_yaw_widget import RollPitchYawWidget

CONTAINER_STYLE = {'display': 'flex', 'flex-direction': 'column'}

class CompoundModelPage:
  def __init__(self, model, app, label="Machine"):
    self.label = label
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
        if arm.children[0]:
          self.joints_widgets.append(JointWidget(arm.children[0], self.app))
      if self.model.origin:  
       self.joints_widgets.append(JointWidget(self.model.origin, self.app))
      for joint in self.model.children:
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
  
  
  def update_pistons_sliders(self, *joints_callbacks):
    # self.model.planes[0].ik_res
    # self.model.update_plane_vertices()
    return [0,0,0]
  
  def add_callback(self):
    print("Adding plane callbacks")
    inputs = []
    for jw in self.joints_widgets:
      jw.add_callback()
      inputs.append(jw.trigger.input)
    
    pistons_outputs = []
    for pw in self.pistons_widgets:
      pw.add_callback()
      inputs.append(pw.trigger.input)
      pistons_outputs.append(pw.slider_output)
    
    planes_inputs = []
    for plw in self.planes_widgets:
      plw.add_callback()
      inputs.append(plw.trigger.input)
      planes_inputs.append(plw.trigger.input)
    self.app.callback(pistons_outputs, planes_inputs)(self.update_model)
    outputs = self.trigger.output
    self.app.callback(outputs, inputs)(self.update_model)