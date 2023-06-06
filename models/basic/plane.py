import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from models.basic.joint import Joint
from models.basic.model import Model
import math
from copy import deepcopy
from utils.trace_utils import TracesHelper

class Plane(Model):
  def __init__(self, _name="Plane", offset_pos=None, origin=None, trace_params=None):
    super().__init__(_name, offset_pos, origin, trace_params)
    # self.constraints = constraints
    # self.rotate(euler_rot, quaternion)
    self.trace_type = "plane"
    self.color = "#ff6348"
    # self.Rbig = 22.645  # outer radius
    # self.Rsmall = 15  # inner radius
    # self.l = 25
    self.Rbig = 130  # outer radius
    self.Rsmall = 70  # inner radius
    self.l = 80
    
    # self.circles = []
    # self.circles.append(Circle(f"{self.name}_Radius1", self.absolute_pos, self.Rbig, "#CEFF33"))
    # self.circles.append(Circle(f"{self.name}_Radius1", self.absolute_pos, self.Rsmall, "#33E6FF"))
    # self.circles.append(Circle(f"{self.name}_Radius2", self.absolute_pos, 30))
  
  def add_vertex(self, offset_pos):
    # print(f"Adding vertex to {self.name}: {offset_pos}")
    vertex = Joint(f"V_{len(self.children)+1}", offset_pos, trace_params={'color': "#888888", 'linewidth': 8, 'markersize': 8})
    vertex.set_parent(self)
    self.children.append(vertex)
  
  def forward_kinematics(self):
    self.update()
  
  def get_trace_points(self):
    return [x.absolute_pos for x in self.children]
    