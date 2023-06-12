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
    self.local_position = deepcopy(self.origin_pos)
    self.local_rotation = [0,0,0]
    self.local_quaternion = Quaternion(self.local_rotation[0], self.local_rotation[1], self.local_rotation[2])
    self.absolute_position = deepcopy(self.origin_pos)
    self.absolute_rotation = [0,0,0]
    self.absolute_quaternion = Quaternion(self.absolute_rotation[0], self.absolute_rotation[1], self.absolute_rotation[2])
    self.parent = None
    self.origin_transform = Transform.make_transform(translation=np.array([0,0,0]))
    self.children = []
    self.trace_type = "joint"
    self.trace_params = trace_params if trace_params is not None else {}
    self.visible = False
    self.transform = Transform.make_transform(translation=self.origin_pos[:3])
    self.local_transform = Transform.make_transform(translation=self.origin_pos[:3])
  
  def get_model_traces(self, fig_data):
    traces = TracesHelper.find_model_traces(fig_data, self.uuid)
    if len(traces) <= 0:
      fig_data, traces = TracesHelper.add_model_traces(fig_data, self.trace_type, self.name, uuid=self.uuid, params=self.trace_params)
    # print(f"Updating trace {trace['uuid']}")
    return fig_data, traces
    
  def forward_kinematics(self):
    warnings.warn(f"forward_kinematics() {IMPL_MISSING_MSG}")
  
  def inverse_kinematics(self):
    warnings.warn(f"inverse_kinematics() {IMPL_MISSING_MSG}")
    
  def update(self, dbg_prefix=""):
    try:
      dbg = f"{dbg_prefix}- Updating {self.name} Transform "
      self.local_transform = Transform.make_transform(translation=self.origin_pos[:3], rotation=self.local_rotation)
      # print(f"New transform for: {self.name}: {self.transform.mat}")
      if self.parent is not None:
        dbg += f"Using parent ({self.parent.name}) transform"
        # self.local_position = np.array(self.parent.transform.mat@np.array(self.origin_pos)).flatten()
        self.transform = Transform.combine(self.parent.transform, self.local_transform)
      else:
        self.transform = Transform.combine(self.origin_transform, self.local_transform)
        
      # Remember that the accumulated transform should always be applied to a hypothetical starting point 0 expressed in world coordinates,
      # and the last component should always be 1 (the 4th dimension used to apply transforms)
      self.absolute_position = np.array(self.transform.mat@np.array([0,0,0,1])).flatten()
      self.absolute_quaternion = Quaternion.quaternion_from_rotation_matrix(self.transform)
      # self.absolute_rotation = Quaternion.euler_from_quaternion(self.absolute_quaternion)
      self.absolute_rotation = Transform.rotation_to_angles(self.transform, order="zyx")
      for child in self.children:
        child.update(dbg_prefix=dbg_prefix)
    except Exception as e:
      print(f"Exception updating {self.name} transform {e}")
      # print(f"Exception combining parent and child transform {e}")
      
  def rotate(self, euler_angles):
    # print(f"Rotating {self.name} ({self.uuid}) with: {euler_angles}")
    euler_angles = Quaternion.convert_angles(euler_angles)
    self.local_rotation = [euler_angles[0], euler_angles[1], euler_angles[2]]
    self.local_quaternion = Quaternion(self.local_rotation[0], self.local_rotation[1], self.local_rotation[2])
    # self.local_quaternion = Quaternion(euler_angles[0], euler_angles[1], euler_angles[2])
    
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
    points = [self.absolute_position]
    # if self.parent is not None:
    #   points = [self.parent.absolute_position] + points
    if len(self.children) > 0 is not None:
      points = points + [self.children[0].absolute_position] 
    return points
  
  def get_vtk_model_data(self, draw_children=True, dbg_prefix=""):
    thickness = 8
    radius = 10
    points = self.get_trace_points()
    color =  hex_to_rgb(self.trace_params.get('color', "#FFFFFF"))
    angles = Transform.rotation_to_angles(self.transform, order="zxy")
    model_data = []
    p1 = list(points[0][0:3])
    orientation = [angles[0], angles[1], angles[2]]
    # I really don't get why the orientation does not work, everything seems ok except for the orientation of these stupid cubes
    joint_origin_point ={
      'id': self.uuid+"point",
      'vtkClass': 'vtkSphereSource',
      'property': {
        'color': color,
        'pointSize': 20,
        },
      'actor': {
        'origin': p1,
        'position': [0,0,0],
        'orientation': orientation,
      },
      'state': {
        "lineWidth": 10,
        "center": p1,
        "radius": radius,
        'resolution': 600
      }
    }
    model_data.append(joint_origin_point)
    
    if len(points) > 1:
      p2 = list(points[1][0:3])
      length = v_dist(p1, p2)
      joint_line = {
        'id': self.uuid+"line",
        'vtkClass': 'vtkLineSource',
        'property': {
          'color': color,
          'pointSize': 10,
          },
        'actor': {
        },
        'state': {
          "lineWidth": 10,
          'point1': p1,
          'point2': p2,
          'resolution': 600
        }
      }
      model_data.append(joint_line)
      joint_cube = {
        'id': self.uuid+"cube",
        'vtkClass': 'vtkCubeSource',
        'property': {
          'color': color,
          # 'pointSize': 10,
          },
        'actor': {
          'origin': p1,
          'position': [0,0,0],
          'orientation': orientation,
        },
        'state': {
          'center': [p1[0], p1[1], p1[2]+length*0.5],
          'zLength': length,
          'xLength': thickness,
          'yLength': thickness,
          'resolution': 600
        }
      }
      model_data.append(joint_cube)
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
    fig_data, traces = self.get_model_traces(fig_data)
    # print(f"Traces found for {self.name}: {[t['name'] for t in traces]}")
    for i in range(0, len(traces)):
      traces[i]['visible'] = self.visible
    # print(f"{dbg_prefix}Drawing {self.name}")
    if self.visible:
      points = self.get_trace_points()
      x, y, z = TracesHelper().points_to_trace(points)
      traces[0]['x'] = x
      traces[0]['y'] = y
      traces[0]['z'] = z
      if len(traces) > 1:
        # How to get axes lines
        # 1. You obviously need the updated transport of your joint that includes translation and rotation
        # 2. Given that transform, apply it to the origin (absolute pos) and then to an offset origin depending on which axes you're plotting
        # For instance, if you want the UP vector (x axis) you'll need to apply the transform to [0,0,0] and then [0,1,0]
        # Get the normalized difference between the new point and the origin. That will give you the direction from the origin to the new point
        # Since it's normalized you can just multiply it by whatever distance you want to get a greater length
        # Add this vector to the calculated position of the point (absolute pos) et voila you got a line that matches the axis direction no matter what the rotation is
        for i in range(0, 3):
          direction = [0,0,0]
          direction[i] = 1
          offset_point =  self.transform.get_direction_vector(direction) * 25
          traces[i+1]['x'] = [x[0], x[0]+offset_point[0]]
          traces[i+1]['y'] = [y[0], y[0]+offset_point[1]]
          traces[i+1]['z'] = [z[0], z[0]+offset_point[2]]
    dbg_prefix += "  "
    if draw_children:
      for child in self.children:
        fig_data = child.draw_plotly(fig_data, draw_children=False, dbg_prefix=dbg_prefix)
    return fig_data
  