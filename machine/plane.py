import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from copy import deepcopy
from machine.joint import *

DEFAULT_TRACE = {
  "name": "Axis Joint",
  "showlegend": True,
  "type": "mesh3d",
  "opacity": BODY_MESH_OPACITY,
  "color": BODY_MESH_COLOR,
  "x": [],
  "y": [],
  "z": [],
}

class Plane:
  def __init__(self, _name, _origin):
    self.name = _name
    self.prev = None
    self.next = None
    self.uuid = str(uuid.uuid4())
    self.pos = deepcopy(_origin)
    self.tm = TransformManager()
    self.joints = []
    self.trace = deepcopy(DEFAULT_TRACE)
  
  def add_vertex(self, joint):
    self.joints.append(joint)
    
  # def forward_kinematics(self):
  #   combined_transform = None
  #   for i in range(0,len(self.joints)):
  #     idx = i
  #     self.joints[idx].update_transform()
  #     self.joints[idx].apply_transform(combined_transform)
  
  def draw(self, figure_data):
    trace = None
    for t in figure_data:
      if 'uuid' in t and t['uuid'] == self.uuid:
        # print(f"Updating trace: {self.uuid}")
        trace = t
        break
    if trace is None:
      trace = self.trace
      trace['name'] = self.name
      trace['uuid'] = self.uuid
      print(f"Appending trace: {self.uuid}")
      figure_data.append(trace)
    
    points = [j.pos for j in self.joints]
    trace['x'] = [float(p[AXIS_ORDER_CONVENTION[0]]) for p in points]
    trace['y'] = [float(p[AXIS_ORDER_CONVENTION[1]]) for p in points]
    trace['z'] = [float(p[AXIS_ORDER_CONVENTION[2]]) for p in points]
    return figure_data
    