import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from copy import deepcopy
from models.basic.joint import Joint
from models.basic.model import Model

class Arm(Model):
  def __init__(self, _name="Arm", offset_pos=None, origin=None, trace_params=None):
    super().__init__(_name, offset_pos, origin, trace_params)
    # self.origin = Joint(f"{self.name}_Origin", self.origin_pos, trace_params=trace_params)
    # if self.origin is not None:
    #   self.origin.transform = pt.transform_from_pq(np.hstack((np.array(self.origin_pos[:3]), pr.q_id)))
    # self.children.append(self.origin)
    self.page = None
  
  def add_joint(self, joint):
    if len(self.children) <= 0:
      joint.set_parent(self)
    else:
      self.children.append(joint)
      self.children[-1].set_parent(self.children[-2])
    
  def forward_kinematics(self):
    self.update(dbg_prefix="\t")
    