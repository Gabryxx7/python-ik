import uuid
import numpy as np
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from components.quaternion_widget import  make_quaternion_widget
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
  def __init__(self, _name, _origin, euler_rot=None, quaternion=None, constraints=None, color=LEG_COLOR):
    self.name = _name
    self.prev = None
    self.next = None
    self.uuid = str(uuid.uuid4())
    self.color = color
    self._origin = np.array(deepcopy(_origin))
    if len(self._origin) < 4:
      self._origin = np.append(self._origin, [1.0])
    self.relative_pos = deepcopy(self._origin)
    self.absolute_pos = deepcopy(self._origin)
    self.constraints = constraints
    self.quaternion = pr.q_id
    self.parent = None
    self.children = []
    self.rotate(euler_rot, quaternion)
    self.visible = True
    self.trace = deepcopy(DEFAULT_TRACE)
    self.combined_transform = None 
    self.transform = pt.transform_from_pq(np.hstack((self._origin[:3], self.quaternion)))
    self.quat_widget = None
    self.tf_widget = None
  
  def update_from_transform(self, transform):
    self.absolute_pos = transform@self._origin
  
  def update(self, dbg_prefix=""):
    dbg = f"{dbg_prefix}- Updating {self.name} Transform "
    self.transform = pt.transform_from_pq(np.hstack((self._origin[:3], self.quaternion)))
    # self.transform = pt.transform_from_pq(np.hstack((np.array([0,0,0]), self.quaternion)))
    # self.transform = pt.transform_from_pq(np.hstack((self.absolute_pos[:3], self.quaternion)))
    if self.parent is not None:
      dbg += f"Using parent ({self.parent.name}) transform"
      # self.transform = self.parent.transform * self.transform
      self.transform = pt.concat(self.parent.transform, self.transform)
    # if self.parent is not None and self.parent.combined_transform is not None:
    #   dbg += f"Using parent ({self.parent.name}) transform"
    #   self.combined_transform = self.parent.combined_transform * self.transform
    # else:
    #   dbg += f"NO PARENT TRANSFORM"
    #   self.combined_transform = self.transform
    print(dbg)
    self.absolute_pos = pt.transform(self.transform, self._origin)
    # self.absolute_pos = self.transform@self._origin
    for child in self.children:
      child.update(dbg_prefix=dbg_prefix)
      
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
      
  def link_to(self, parent):
    print(f"Linking joints {parent.name} to {self.name}")
    self.parent = parent
    parent.children.append(self)
    
  def set_visibility(self, vis):
    self.visible = vis
  
  def get_trace(self, figure_data):
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
    return trace
      
  def get_joint_length(self):
    return (np.linalg.norm(self.parent.absolute_pos - self.absolute_pos))
  
  def draw(self, figure_data):
    trace = self.get_trace(figure_data)
    points = [self.absolute_pos]
    if self.parent is not None:
      points = [self.parent.absolute_pos] + points
    if self.color is not None:
      trace['line']['color'] = self.color
    trace['x'] = [float(p[AXIS_ORDER_CONVENTION[0]]) for p in points]
    trace['y'] = [float(p[AXIS_ORDER_CONVENTION[1]]) for p in points]
    trace['z'] = [float(p[AXIS_ORDER_CONVENTION[2]]) for p in points]
    trace['visible'] = self.visible
    return figure_data
  
  def get_quaternion_widget(self, app):
    if self.quat_widget is None:
      self.quat_widget = make_quaternion_widget(app, self)
    return self.quat_widget
  
  def get_transform_widget(self, app, color="inherit"):
    color = "inherit" if self.color is None else self.color
    mk_id = f"{self.uuid}-md-transform-view"
    markdown_widget = dcc.Markdown(self.get_transform_text(), id=mk_id, style={"color": color})
    self.tf_widget = html.Div([markdown_widget],
      style={"color":color})
    self.tf_output = Output(mk_id, 'children')
    return {'widget': self.tf_widget, 'outputs': self.tf_output}

  def get_transform_text(self):
    tf_text = f"{self.name}"
    tf_text += f"\n```{np.array2string(self.transform, precision=2, floatmode='fixed')}"
    tf_text += f"\n\nOrigin: {np.round(self._origin, 2)}"
    tf_text += f"\nPosition: {np.round(self.absolute_pos, 2)}"
    tf_text += f"\nDistance from prev: {np.round(self.get_joint_length(), 2)}"
    tf_text += f"\nQuaternion: {self.quaternion}"
    return tf_text
