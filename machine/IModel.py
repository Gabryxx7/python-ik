import warnings
import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from copy import deepcopy
from machine.joint import *
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

IMPL_MISSING_MSG = "implementatiom missing (did you override it in your new model class?)"
left_side_width = "30vw"
LEFT_PANEL_STYLE = {'display': 'flex', 'width': left_side_width, 'max-width': left_side_width, 'flex-wrap': 'wrap', 'flex-direction': 'row'}
RIGHT_PANEL_STYLE = {'display': 'flex', 'flex-direction': 'row', 'gap': '1rem', 'padding': '1rem', 'width': 'right_side_width', 'flex-wrap': 'nowrap', 'align-items': 'start', 'justify-items': 'start'}
CONTAINER_STYLE = {'display': 'flex', 'flex-direction': 'row'}

class IModel:
    
  def __init__(self, _name, _origin):
    self.name = _name
    self.prev = None
    self.next = None
    self.uuid = str(uuid.uuid4())
    self.absolute_pos = deepcopy(_origin)
    self.tm = TransformManager()
    self.joints = []
    self.origin = Joint(f"{self.name}_Origin", self.absolute_pos)
    self.origin.transform = pt.transform_from_pq(np.hstack((np.array(self.absolute_pos), pr.q_id)))
    self.trace = None
    self.visible = True
    self.joints_widgets = []
    self.outputs = []
    self.cb_outputs = []
    self.inputs = []
    self.quat_widgets = []
    self.arms = []
    self.pistons = []
    
  def get_trace(self, fig_data):
    if self.trace is not None:
      return self.trace
    trace = None
    for t in fig_data:
      if 'uuid' in t and t['uuid'] == self.uuid:
        # print(f"Updating trace: {self.uuid}")
        trace = t
        break
    if trace is None:
      trace = self.trace
      trace['name'] = self.name
      trace['uuid'] = self.uuid
      print(f"Appending trace: {self.uuid}")
      fig_data.append(trace)
    return trace
    
  def add_joint(self, joint):
    warnings.warn(f"add_joint(joint) {IMPL_MISSING_MSG}")
  
  def forward_kinematics(self):
    warnings.warn(f"forward_kinematics() {IMPL_MISSING_MSG}")
  
  def inverse_kinematics(self):
    warnings.warn(f"forward_kinematics() {IMPL_MISSING_MSG}")
    
  # I know this is conceputally not right here since this is about the 3D model and joints and not the actual front end
  # but look, it's much easier this way!
  def set_visibility(self, vis, fig_data):
    warnings.warn(f"set_visibility(vis, fig_data) not implemented, using IModel default")
    for j in self.joints:
      fig_data = j.set_visibility(vis)
  
  def draw(self, fig_data):
    warnings.warn(f"draw(fig_data) not implemented, using IModel default")
    for j in self.joints:
      fig_data = j.draw(fig_data)
    return fig_data
  
  def get_top_right_side_widgets(self, app):
    tf_widgets = []
    for i in range(0, len(self.joints)):
      tf_widget = self.joints[i].get_transform_widget(app)
      tf_widgets.append(tf_widget)
    return tf_widgets
  
  def get_left_side_widgets(self, app):
    self.quat_widgets = []
    for i in range(0, len(self.joints)):
      quat_widget = self.joints[i].get_quaternion_widget(app)
      self.quat_widgets.append(quat_widget)
    return self.quat_widgets
  
  def update_transforms_widgets(self, *args):
      tf_texts = []
      for i in range(0, len(self.joints)):
          tf_texts.append(self.joints[i].get_transform_text())    
      return tf_texts
  
  def update_joints_quaternions(self, model_quaternions):
    print(model_quaternions)
    for i in range(0, len(self.joints)):
        self.joints[i].rotate(quaternion=model_quaternions[i])
    self.forward_kinematics()
    out = [['test'] for x in self.cb_outputs]
    return out
  
  def get_widget(self, app):
    l_widgets = self.get_left_side_widgets(app)
    r_widgets = self.get_top_right_side_widgets(app)
    widgets_panel = html.Div([x['widget'] for x in l_widgets], LEFT_PANEL_STYLE)
    info_panel = html.Div([x['widget'] for x in r_widgets], style=RIGHT_PANEL_STYLE)
    model_page = html.Div([widgets_panel, info_panel], style=CONTAINER_STYLE)
    all_widgets = r_widgets+l_widgets
    for x in all_widgets:
      if 'inputs' in x:
        self.inputs.append(x['inputs'])
      if 'outputs' in x:
        self.outputs.append(x['outputs'])
      if 'cb_outputs' in x:
        self.cb_outputs.append(x['cb_outputs'])
    return model_page, self.inputs, self.outputs
    # vis_checkbox = dcc.Checklist(robots_show_options.copy(), [robots_show_options[0]], style={'display': 'flex', 'padding': '0.5rem', 'place-content': 'space-evenly'}, id='show-robots-checklist')
    
  def register_model_callbacks(self, app):
    inpts = [self.inputs]
    app.callback(self.outputs, inpts, [])(self.update_transforms_widgets)
    app.callback(self.cb_outputs, [inpts])(self.update_joints_quaternions)
    