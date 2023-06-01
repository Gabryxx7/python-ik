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
RIGHT_PANEL_STYLE = {'display': 'flex', 'flex-direction': 'column', 'gap': '1rem', 'padding': '1rem', 'width': 'right_side_width', 'flex-wrap': 'nowrap', 'align-items': 'start', 'justify-items': 'start'}
CONTAINER_STYLE = {'display': 'flex', 'flex-direction': 'row'}
COLUMN_STYLE = {'display': 'flex', 'flex-direction': 'row'}

class IModel:
  def __init__(self, _name, _origin):
    self.name = _name
    self.prev = None
    self.next = None
    self.uuid = f"IModel_{str(uuid.uuid4())}"
    self.absolute_pos = deepcopy(_origin)
    self.tm = TransformManager()
    self.joints = []
    self.origin = Joint(f"{self.name}_Origin", self.absolute_pos)
    self.origin.transform = pt.transform_from_pq(np.hstack((np.array(self.absolute_pos), pr.q_id)))
    self.trace = None
    self.visible = True
    
  def make_trace(self):
    trace = {}
    trace['name'] = self.name
    trace['uuid'] = self.uuid
    return trace
  
  def get_trace(self, fig_data):
    if self.trace is not None:
      return self.trace
    trace = None
    for t in fig_data:
      if 'uuid' in t and t['uuid'] == self.uuid:
        print(f"Updating trace: {self.uuid}")
        trace = t
        break
    if trace is None:
      trace = self.make_trace()
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
  