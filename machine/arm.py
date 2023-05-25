import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from copy import deepcopy
from machine.joint import *

class Arm:
  def __init__(self, _name, _origin):
    self.name = _name
    self.prev = None
    self.next = None
    self.uuid = str(uuid.uuid4())
    self.pos = deepcopy(_origin)
    self.tm = TransformManager()
    self.joints = []
  
  def add_joint(self, joint):
    self.joints.append(joint)
    if len(self.joints) > 1:
      self.joints[-2].link_to(self.joints[-1])
      self.joints[-1].update_transform()
      self.tm.add_transform(f"joint_{len(self.joints)-2}", f"joint_{len(self.joints)-1}", self.joints[-2].transform)
    
  def forward_kinematics(self):
    combined_transform = None
    for i in range(0,len(self.joints)):
      idx = i
      self.joints[idx].update_transform()
      self.joints[idx].apply_transform(combined_transform)
  
  def draw(self, figure_data):
    for j in self.joints:
      figure_data = j.draw(figure_data)
    return  figure_data
    