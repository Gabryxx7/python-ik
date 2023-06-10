import warnings
import uuid
import numpy as np
from copy import deepcopy
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from utils.trace_utils import TracesHelper
from utils.transforms import Transform
from utils.quaternion import Quaternion

IMPL_MISSING_MSG = "implementatiom missing (did you override it in your new model class?)"

v_dist = lambda p, orig=[0,0,0]: (np.linalg.norm(np.array(orig) - np.array(p)))
def hex_to_rgb(h):
  h = h.lstrip('#')
  return list(float(int(h[i:i+2], 16)/255) for i in (0, 2, 4))

class Model:
  def __init__(self, _name="Model", offset_pos=None, trace_params=None):
    self.name = _name
    self.uuid = f"{self.name.replace(' ', '_')}_{str(uuid.uuid4())}"
    if offset_pos is None:
      offset_pos = np.array([0,0,0,1.0])
    self.origin_pos = np.array(deepcopy(offset_pos))
    if len(self.origin_pos) < 4:
      self.origin_pos = np.append(self.origin_pos, [1.0])
    self.relative_pos = deepcopy(self.origin_pos)
    self.absolute_pos = deepcopy(self.origin_pos)
    self.absolute_pos_new = deepcopy(self.origin_pos)
    self.parent = None
    self.children = []
    self.trace_type = "joint"
    self.trace_params = trace_params if trace_params is not None else {}
    self.visible = False
    self.transform = Transform.make_transform(translation=self.origin_pos[:3])
    self.quaternion = Quaternion()
  
  def get_trace(self, fig_data):
    trace = TracesHelper.find_trace(fig_data, self.uuid)
    if trace is None:
      fig_data, trace = TracesHelper.add_trace(fig_data, self.trace_type, self.name, uuid=self.uuid, params=self.trace_params)
    # print(f"Updating trace {trace['uuid']}")
    return fig_data, trace
    
  def forward_kinematics(self):
    warnings.warn(f"forward_kinematics() {IMPL_MISSING_MSG}")
  
  def inverse_kinematics(self):
    warnings.warn(f"inverse_kinematics() {IMPL_MISSING_MSG}")
    
  def update(self, dbg_prefix=""):
    try:
      dbg = f"{dbg_prefix}- Updating {self.name} Transform "
      self.transform = Transform.make_transform(translation=self.origin_pos[:3], quaternion=self.quaternion)
      if self.parent is not None:
        dbg += f"Using parent ({self.parent.name}) transform"
        self.transform = Transform.combine(self.parent.transform, self.transform)
      # Remember that the accumulated transform should always be applied to a hypothetical starting point 0 expressed in world coordinates,
      # and the last component should always be 1 (the 4th dimension used to apply transforms)
      self.absolute_pos = np.array(self.transform.mat@np.array([0,0,0,1])).flatten()
      for child in self.children:
        child.update(dbg_prefix=dbg_prefix)
    except Exception as e:
      print(f"Exception updating {self.name} transform {e}")
      # print(f"Exception combining parent and child transform {e}")
      
  def rotate(self, euler_rot=None, quaternion=None):
    # print(f"Rotating {self.name} ({self.uuid}) with: {quaternion}")
    if quaternion is not None:
      self.quaternion = Quaternion(quaternion)
      return
    if euler_rot is None:
      self.quaternion = Quaternion.quaternion_from_angles(euler_rot)
      return
    self.quaternion = Quaternion(axis=[0, 0, 0], angle=0)
    for axis_idx in AXIS_ORDER_CONVENTION:
      axis = [0,0,0]
      axis[axis_idx] = 1
      self.quaternion = self.quaternion * Quaternion(axis=axis, angle=euler_rot[axis_idx])
    # print(self.quaternion)
    # print(self.transform)
    # print("\n")
    
  # I know this is conceputally not right here since this is about the 3D model and joints and not the actual front end
  # but look, it's much easier this way!
  def set_visibility(self, vis, propagate=True):
    self.visible = vis
    if propagate:
      for child in self.children:
        child.set_visibility(vis)
      
  def set_parent(self, parent):
    # print(f"Attaching object {self.name} to {parent.name}")
    self.parent = parent
    parent.children.append(self)
    
  def add_child(self, child):
    # print(f"Attaching object {child.name} to {self.name}")
    child.parent = self
    self.children.append(child)
    
  def get_trace_points(self):
    points = [self.absolute_pos]
    # if self.parent is not None:
    #   points = [self.parent.absolute_pos] + points
    if len(self.children) > 0 is not None:
      points = points + [self.children[0].absolute_pos] 
    return points
  
  def get_vtk_model_data(self, draw_children=True, dbg_prefix=""):
    thickness = 8
    radius = 10
    points = self.get_trace_points()
    color =  hex_to_rgb(self.trace_params.get('color', "#FFFFFF"))
    angles = Transform.rotation_angles(self.transform)
    # angles = self.quaternion.rpy
    model_data = []
    p1 = list(points[0][0:3])
    model_data.append({
      'id': self.uuid+"point",
      'vtkClass': 'vtkSphereSource',
      'property': {
        'color': color,
        'pointSize': 20,
        },
      'actor': {
        'origin': p1,
        'orientation': angles,
      },
      'state': {
        "lineWidth": 10,
        "center": p1,
        "radius": radius,
        'resolution': 600
      }
    })
    if len(points) > 1:
      p2 = list(points[1][0:3])
      length = v_dist(p1, p2)
      model_data.append({
        'id': self.uuid+"line",
        'vtkClass': 'vtkLineSource',
        'property': {
          'color': color,
          'pointSize': 10,
          },
        'actor': {
          # 'origin': [0,0,0],
          # 'orientation': self.quaternion.rpy,
        },
        'state': {
          "lineWidth": 10,
          'point1': p1,
          'point2': p2,
          'resolution': 600
        }
      })
      cube_center = [p1[0], p1[1], p1[2]+length*0.5]
      cube_origin = p1
      model_data.append({
        'id': self.uuid+"cube",
        'vtkClass': 'vtkCubeSource',
        'property': {
          'color': color,
          # 'pointSize': 10,
          },
        'actor': {
          'origin': cube_origin,
          'orientation': [angles[0], angles[1], angles[2]],
        },
        'state': {
          'center': cube_center,
          'zLength': length,
          'xLength': thickness,
          'yLength': thickness,
          'resolution': 600
        }
      })
      # model_data.append({
      #   'id': self.uuid+"point2",
      #   'vtkClass': 'vtkSphereSource',
      #   'property': {
      #     'color': color,
      #     'pointSize': 20,
      #     },
      #   'actor': {
      #     'origin': cube_origin,
      #     'orientation': angles,
      #   },
      #   'state': {
      #     "lineWidth": 10,
      #     "center": cube_origin,
      #     "radius": radius*2,
      #     'resolution': 600
      #   }
      # })
    
    if not draw_children:
      return model_data
    
    dbg_prefix += "  "
    for child in self.children:
      child_model = child.get_vtk_model_data(draw_children=False, dbg_prefix=dbg_prefix)
      if child_model is not None and len(child_model) > 0:
        model_data += child_model
    # print(f"Model data for {self.name}")
    # print(model_data)
    return model_data
  
  def draw_plotly(self, fig_data, draw_children=True, dbg_prefix=""):
    fig_data, trace = self.get_trace(fig_data)
    trace['visible'] = self.visible
    # print(f"{dbg_prefix}Drawing {self.name}")
    if self.visible:
      points = self.get_trace_points()
      x, y, z = TracesHelper().points_to_trace(points)
      trace['x'] = x
      trace['y'] = y
      trace['z'] = z
    dbg_prefix += "  "
    if draw_children:
      for child in self.children:
        fig_data = child.draw_plotly(fig_data, draw_children=False, dbg_prefix=dbg_prefix)
    return fig_data
  