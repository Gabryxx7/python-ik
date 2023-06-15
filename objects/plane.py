import uuid
import numpy as np
from objects.joint import Joint
from objects.Object3D import Object3D
import math
from copy import deepcopy
from components.PlotlyRenderer import ModelType

class Plane(Object3D):
  def __init__(self, _name="Plane", offset_pos=None, trace_params=None):
    super().__init__(_name, offset_pos, trace_params)
    self.trace_type = ModelType.PLANE
    self.color = "#ff6348"
  
  def add_vertex(self, offset_pos):
    # print(f"Adding vertex to {self.name}: {offset_pos}")
    vertex = Joint(f"{self.name}_V_{len(self.children)+1}", offset_pos, trace_params={'color': "#888888", 'linewidth': 8, 'markersize': 8})
    vertex.set_parent(self)
    # self.children.append(vertex)
  
  def forward_kinematics(self):
    self.update()
  
  def get_trace_points(self):
    return [x.transform.position for x in self.children]
    