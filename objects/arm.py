import uuid
import numpy as np
from copy import deepcopy
from objects.joint import Joint
from objects.Object3D import Object3D

class Arm(Object3D):
  def __init__(self, _name="Arm", offset_pos=None, trace_params=None):
    super().__init__(_name, offset_pos, trace_params)
    self.page = None
  
  def add_joint(self, joint):
    if len(self.children) <= 0:
      joint.set_parent(self)
    else:
      self.children.append(joint)
      self.children[-1].set_parent(self.children[-2])
    
  def forward_kinematics(self):
    try:
      self.update(dbg_prefix="\t")
    except Exception as e:
      print(f"Error updating Arm {r}")
    