import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
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
# Angles and positions constraints follow the same convention above from AXIS_ORDER_CONVENTION
DEFAULT_CONSTRAINTS = {'angles': {'max': [], 'min': [0]}, 
                      'position': {'max': [], 'min': []}}

DEFAULT_TRACE = {
    "name": "Joint",
    "line": {"color": "#2284e6", "width": LEG_OUTLINE_WIDTH*2},
    "marker": {"size": MARKER_SIZE},
    "mode": "lines+markers",
    "showlegend": False,
    "type": "scatter3d",
    "x": [0],
    "y": [0],
    "z": [0]
}
DEFAULT_ROTATION_TRACE = {
  "name": "Axis Joint",
  "showlegend": True,
  "type": "mesh3d",
  "opacity": BODY_MESH_OPACITY,
  "color": BODY_MESH_COLOR,
  "x": [],
  "y": [],
  "z": [],
}
DEFAULT_AXIS_TRACE = {
    "name": "Joint Axis",
    "line": {"color": "#2284e6", "width": LEG_OUTLINE_WIDTH*2},
    "marker": {"size": MARKER_SIZE},
    "mode": "lines+markers",
    "showlegend": False,
    "type": "scatter3d",
    "x": [0],
    "y": [0],
    "z": [0]
}

class JointConstraints:
  def __init__(self, max_angles=None, min_angles=None, max_pos=None, min_pos=None):
    self.max_angles = max_angles
    self.min_angles = min_angles
    self.max_pos = max_pos
    self.min_pos = min_pos
    
  def check(self):
    return True
    
class Joint:
  def __init__(self, _name, _origin, euler_rot=None, quaternion=None, constraints=None, color=None):
    self.name = _name
    self.prev = None
    self.next = None
    self.uuid = str(uuid.uuid4())
    self.color = color
    self._origin = np.array(deepcopy(_origin))
    if len(self._origin) < 4:
      self._origin = np.append(self._origin, [1.0])
    self.pos = deepcopy(self._origin)
    self.constraints = constraints
    self.quaternion = pr.q_id
    self.update_transform()
    self.rotate(euler_rot, quaternion)
    self.trace = deepcopy(DEFAULT_TRACE)
  
  def update_transform(self):
    if self.prev is not None:
      self.transform = pt.transform_from_pq(np.hstack(((self.prev.pos)[:3], self.prev.quaternion)))
    else:
      self.transform = pt.transform_from_pq(np.hstack((np.array([0,0,0]), self.quaternion)))
      
  def rotate(self, euler_rot=None, quaternion=None):
    # print(f"Rotating {self.name} ({self.uuid}) with: {quaternion}")
    if quaternion is not None:
      self.quaternion = deepcopy(quaternion)
    else:
      if euler_rot is None:
        self.quaternion = pr.q_id
      else:
        self.quaternion = Quaternion(axis=[0, 0, 0], angle=0)
        for axis_idx in AXIS_ORDER_CONVENTION:
          axis = [0,0,0]
          axis[axis_idx] = 1
          self.quaternion = self.quaternion * Quaternion(axis=axis, angle=euler_rot[axis_idx])
    # print(self.quaternion)
    # print(self.transform)
    # print("\n")
      
  def link_to(self, next_joint):
    print(f"Linking joints {self.name} to {next_joint.name}")
    self.next = next_joint
    next_joint.prev = self
  
  def apply_transform(self, transform=None):
    transform = self.transform if transform is None else transform
    self.pos = transform@self._origin
    
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
      # print(f"Appending trace: {self.uuid}")
      figure_data.append(trace)
    
    # print(f"{self.name} Origin: {self._origin}")
    points = [self.pos]
    if self.next is not None:
      points.append(self.next.pos)
    if self.color is not None:
      trace['line']['color'] = self.color
    trace['x'] = [float(p[AXIS_ORDER_CONVENTION[0]]) for p in points]
    trace['y'] = [float(p[AXIS_ORDER_CONVENTION[1]]) for p in points]
    trace['z'] = [float(p[AXIS_ORDER_CONVENTION[2]]) for p in points]
    return figure_data
        
