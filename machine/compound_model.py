import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from machine.joint import *
from machine.IModel import IModel
import math

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

class CompoundModel(IModel):
  def __init__(self, _name, _origin):
    self.name = _name
    self.next = None
    self.uuid = f"Plane_{str(uuid.uuid4())}"
    self.absolute_pos = deepcopy(_origin)
    self.tm = TransformManager()
    self.origin = Joint(f"{self.name}_Origin", self.absolute_pos)
    self.origin.transform = pt.transform_from_pq(np.hstack((np.array(self.absolute_pos), pr.q_id)))
    self.trace = None
    self.visible = False
    self.arms = []
    self.joints = []
    self.pistons = []
    self.planes = []
    self.color = "#ff6348"
    
  def add_arm(self, arm):
    self.arms.append(arm)
    
  def add_piston(self, piston):
    self.pistons.append(piston)
    
  def add_joint(self, joint):
    self.joints.append(joint)
    
  def add_plane(self, plane):
    self.planes.append(plane)
    
  def make_trace(self):
    trace = deepcopy(DEFAULT_PLANE_TRACE)
    trace['name'] = self.name
    trace['uuid'] = self.uuid
    return trace
  
  def forward_kinematics(self):
    print("\n\nStarting Forward Kinematics:")
    for arm in self.arms:
      arm.forward_kinematics()
    for piston in self.pistons:
      piston.forward_kinematics()
    for plane in self.planes:
      plane.forward_kinematics()
    self.origin.update()
    
        
  def set_visibility(self, vis):
    self.visible = vis
    for j in self.joints:
      j.set_visibility(vis)
    for a in self.arms:
      a.set_visibility(vis)
    for p in self.pistons:
      p.set_visibility(vis)
    for p in self.planes:
      p.set_visibility(vis)
    self.origin.set_visibility(vis)
  
  def draw(self, figure_data):
    trace = self.get_trace(figure_data)
    for j in self.joints:
      figure_data = j.draw(figure_data)
    for p in self.pistons:
      figure_data = p.draw(figure_data)
    for a in self.arms:
      figure_data = a.draw(figure_data)
    for p in self.planes:
      figure_data = p.draw(figure_data)
    return figure_data