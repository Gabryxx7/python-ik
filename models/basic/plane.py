import uuid
import numpy as np
from models.basic.joint import Joint
from models.basic.model import Model
import math
from copy import deepcopy
from utils.trace_utils import TracesHelper

class Plane(Model):
  def __init__(self, _name="Plane", offset_pos=None, trace_params=None):
    super().__init__(_name, offset_pos, trace_params)
    self.trace_type = "plane"
    self.color = "#ff6348"
  
  def add_vertex(self, offset_pos):
    # print(f"Adding vertex to {self.name}: {offset_pos}")
    vertex = Joint(f"V_{len(self.children)+1}", offset_pos, trace_params={'color': "#888888", 'linewidth': 8, 'markersize': 8})
    vertex.set_parent(self)
    self.children.append(vertex)
  
  def forward_kinematics(self):
    self.update()
  
  def get_trace_points(self):
    return [x.absolute_position for x in self.children]
    