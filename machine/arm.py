import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from copy import deepcopy
from machine.joint import *
from machine.IModel import IModel

class Arm(IModel):
  def __init__(self, _name, _origin):
    super().__init__(_name, _origin)
  
  def add_joint(self, joint):
    self.joints.append(joint)
    if len(self.joints) > 1:
      self.joints[-1].link_to(self.joints[-2])
      self.tm.add_transform(f"joint_{self.joints[-2].name}", f"joint_{self.joints[-1].name}", self.joints[-2].transform)
      return
    print(f"Origin Linking: {self.origin.name} -> {self.joints[0].name}")
    self.joints[0].link_to(self.origin)
    
  def forward_kinematics(self):
    print("\n\nStarting Forward Kinematics:")
    self.origin.update(dbg_prefix="\t")
    
    # for i in range(1, len(self.joints)):
    #   print(f"Calculated Transform {self.joints[i-1].name} -> {self.joints[i]}: ")
    #   print(self.joints[i].transform)
    #   # print(f"\nTM MANAGER Transform joint_{self.joints[i-1].name} to joint_{self.joints[i].name}")
    #   # t = self.tm.get_transform(f"joint_{self.joints[i-1].name}", f"joint_{self.joints[i].name}")
    #   # self.joints[i].update_from_transform(t)
    #   # print(t)
    #   print(f"Distance from Parent: {np.linalg.norm(self.joints[i-1].absolute_pos - self.joints[i].absolute_pos)}")
        
  def set_visibility(self, vis):
    for j in self.joints:
      figure_data = j.set_visibility(vis)
  
  def draw(self, figure_data):
    for j in self.joints:
      figure_data = j.draw(figure_data)
    return figure_data
    