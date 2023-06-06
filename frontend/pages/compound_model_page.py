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
    self.id = f"tab-{self.model.uuid}"
  
  def get_page(self):
    if self.page is None:
      for arm in self.model.arms:
        if len(arm.children) > 0:
          self.joints_widgets.append(JointWidget(arm.children[0], self.app))
        if len(arm.children) > 1:
          self.pistons_widgets.append(PistonWidget(arm.children[1], self.app))
      for joint in self.model.children:
        self.joints_widgets.append(JointWidget(joint, self.app))
        
      for plane in self.model.planes:
        self.planes_widgets.append(RollPitchYawWidget(plane, self.app, yaw_enabled=False))
      self.trigger = Trigger(self.id)
      self.page = html.Div([plw.get_widget() for plw in self.planes_widgets] + [pw.get_widget() for pw in self.pistons_widgets] + [jw.get_widget() for jw in self.joints_widgets] + [self.trigger.component], className="model-sidebar")
    return self.page
  
  def update_model(self, **inputs):
    self.model.forward_kinematics()
    pistons_heights = [0,0,0]
    for i in range(0,3):
      pistons_heights[i] = self.model.arms[i].children[0].origin_pos[2]
      pistons_heights[i] = pistons_heights[i]/self.model.max_piston_height
    # self.model.update_plane_vertices()
    yaw_output = [self.model.ik_res[5]]
    # yaw_output = []
    return [[""], yaw_output, pistons_heights]
  
  def add_callback(self):
    inputs = {}
    inputs['joints'] = []
    for jw in self.joints_widgets:
      jw.add_callback()
      inputs['joints'].append(jw.trigger.input)
    
    inputs['pistons'] = []
    pistons_outputs = []
    for pw in self.pistons_widgets:
      pw.add_callback()
      # inputs['pistons'].append(pw.trigger.input)
      pistons_outputs.append(pw.slider_output)
    
    yaw_outputs = []
    inputs['planes'] = []
    for plw in self.planes_widgets:
      plw.add_callback()
      inputs['planes'].append(plw.trigger.input)
      yaw_outputs.append(plw.sliders_outputs[2])
      
    outputs = [self.trigger.output]
    outputs.append(yaw_outputs)
    outputs.append(pistons_outputs)
    self.app.callback(outputs, inputs)(self.update_model)