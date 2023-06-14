import uuid
import numpy as np
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
from copy import deepcopy
from objects.Object3D import Object3D
from components.PlotlyRenderer import TraceType
DEFAULT_CONSTRAINTS = {'angles': {'max': [], 'min': [0]}, 
                      'position': {'max': [], 'min': []}}

class JointConstraints:
  def __init__(self, max_angles=None, min_angles=None, max_pos=None, min_pos=None):
    self.max_angles = max_angles
    self.min_angles = min_angles
    self.max_pos = max_pos
    self.min_pos = min_pos
    
  def check(self):
    return True
    
class Joint(Object3D):
  def __init__(self, _name="Joint", offset_pos=None, trace_params=None):
    super().__init__(_name, offset_pos, trace_params)
    # self.constraints = constraints
    self.trace_type = TraceType.JOINT
  
  def force_update(self, override_transform):
    self.transform.position = override_transform@self.local_transform.translation
      
  def get_joint_length(self):
    if self.parent is not None:
      return (np.linalg.norm(self.parent.transform.position - self.transform.position))
    return -1.0
  
