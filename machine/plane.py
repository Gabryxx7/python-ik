import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from machine.joint import *
from machine.IModel import IModel

from copy import deepcopy
from style_settings import (
    BODY_MESH_COLOR,
    BODY_MESH_OPACITY,
    BODY_COLOR,
    BODY_OUTLINE_WIDTH,
    COG_COLOR,
    COG_SIZE,
    HEAD_SIZE,
    LEG_COLOR,
    LEG_OUTLINE_WIDTH,
    SUPPORT_POLYGON_MESH_COLOR,
    SUPPORT_POLYGON_MESH_OPACITY,
    LEGENDS_BG_COLOR,
    AXIS_ZERO_LINE_COLOR,
    PAPER_BG_COLOR,
    GROUND_COLOR,
    LEGEND_FONT_COLOR,
)
MARKER_SIZE = 15
X = 0
Y = 1
Z = 2 
AXIS_ORDER_CONVENTION = [X, Y, Z]
DEFAULT_PLANE_TRACE = {
  "name": "Plane Triangle",
  "showlegend": True,
  "type": "mesh3d",
  "mode": "lines+markers",
  "opacity": 0.5,
  "color": "#ff6348",
  "x": [],
  "y": [],
  "z": []
}

class Plane(IModel):
  def __init__(self, _name, _origin):
    self.name = _name
    self.prev = None
    self.next = None
    self.uuid = f"Plane_{str(uuid.uuid4())}"
    self.absolute_pos = deepcopy(_origin)
    self.tm = TransformManager()
    self.joints = []
    self.origin = Joint("Origin", self.absolute_pos)
    self.origin.transform = pt.transform_from_pq(np.hstack((np.array(self.absolute_pos), pr.q_id)))
    self.trace = None
    self.visible = True
    self.arms = []
    self.pistons = []
    
  def add_arm(self, arm):
    self.arms.append(arm)
    
  def add_piston(self, piston):
    self.pistons.append(piston)
    
  def make_trace(self):
    trace = deepcopy(DEFAULT_PLANE_TRACE)
    trace['name'] = self.name
    trace['uuid'] = self.uuid
    return trace
  
  def forward_kinematics(self):
    print("\n\nStarting Forward Kinematics:")
    for arm in self.arms:
      arm.forward_kinematics()
    # self.origin.update(dbg_prefix="\t")
    
    # for i in range(1, len(self.joints)):
    #   print(f"Calculated Transform {self.joints[i-1].name} -> {self.joints[i]}: ")
    #   print(self.joints[i].transform)
    #   # print(f"\nTM MANAGER Transform joint_{self.joints[i-1].name} to joint_{self.joints[i].name}")
    #   # t = self.tm.get_transform(f"joint_{self.joints[i-1].name}", f"joint_{self.joints[i].name}")
    #   # self.joints[i].update_from_transform(t)
    #   # print(t)
    #   print(f"Distance from Parent: {np.linalg.norm(self.joints[i-1].absolute_pos - self.joints[i].absolute_pos)}")
        
              
  def draw(self, figure_data):
    trace = self.get_trace(figure_data)
    points = [p.joints[-1].absolute_pos for p in self.arms]
    trace['x'] = [float(p[AXIS_ORDER_CONVENTION[0]]) for p in points]
    trace['y'] = [float(p[AXIS_ORDER_CONVENTION[1]]) for p in points]
    trace['z'] = [float(p[AXIS_ORDER_CONVENTION[2]]) for p in points]
    print(trace)
    # trace['visible'] = 'true'
    return figure_data
    