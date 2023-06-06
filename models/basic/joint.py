import uuid
import numpy as np
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from copy import deepcopy
from models.basic.model import Model
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
    
class Joint(Model):
  def __init__(self, _name="Joint", offset_pos=None, origin=None, trace_params=None):
    super().__init__(_name, offset_pos, origin, trace_params)
    # self.constraints = constraints
    self.trace_type = "joint"
    # self.rotate(euler_rot, quaternion)
  
  def force_update(self, override_transform):
    self.absolute_pos = override_transform@self.origin_pos
      
  def get_joint_length(self):
    if self.parent is not None:
      return (np.linalg.norm(self.parent.absolute_pos - self.absolute_pos))
    return -1.0
  
  def get_trace_points(self):
    points = [self.absolute_pos]
    if self.parent is not None:
      points = [self.parent.absolute_pos] + points
    return points
