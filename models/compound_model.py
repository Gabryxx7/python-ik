import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from models.basic.joint import Joint
from models.basic.model import Model
import math
class CompoundModel(Model):
  def __init__(self, _name="Compound", offset_pos=None, origin=None, trace_params=None):
    super().__init__(_name, offset_pos, origin, trace_params)
    self.arms = []
    self.children = []
    self.pistons = []
    self.planes = []
    self.trace_params['color'] = "#ff6348"
    
  def add_arm(self, arm):
    self.arms.append(arm)
    
  def add_piston(self, piston):
    self.pistons.append(piston)
    
  def add_joint(self, joint):
    self.children.append(joint)
    
  def add_plane(self, plane):
    self.planes.append(plane)
    
  def forward_kinematics(self):
    print("\n\nStarting Forward Kinematics:")
    for arm in self.arms:
      arm.forward_kinematics()
    for piston in self.pistons:
      piston.forward_kinematics()
    for plane in self.planes:
      plane.forward_kinematics()
    self.origin.update()
        
  def set_visibility(self, vis):
    super().set_visibility(vis)
    for a in self.arms:
      a.set_visibility(vis)
    for p in self.pistons:
      p.set_visibility(vis)
    for p in self.planes:
      p.set_visibility(vis)
  
  def draw(self, fig_data):
    super().draw(fig_data)
    for p in self.pistons:
      fig_data = p.draw(fig_data)
    for a in self.arms:
      fig_data = a.draw(fig_data)
    for p in self.planes:
      fig_data = p.draw(fig_data)
    return fig_data