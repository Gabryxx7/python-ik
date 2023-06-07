import uuid
import numpy as np
from copy import deepcopy
from models.basic.joint import Joint
from models.basic.model import Model

class Arm(Model):
  def __init__(self, _name="Arm", offset_pos=None, origin=None, trace_params=None):
    super().__init__(_name, offset_pos, origin, trace_params)
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
    