import dash
import warnings
import uuid
import numpy as np
from copy import deepcopy
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from components.Transform import Transform
from components.PlotlyRenderer import PlotlyRenderer, TraceType
from utils.quaternion import Quaternion

IMPL_MISSING_MSG = "implementatiom missing (did you override it in your new model class?)"

v_dist = lambda p, orig=[0,0,0]: (np.linalg.norm(np.array(orig) - np.array(p)))
def hex_to_rgb(h):
  h = h.lstrip('#')
  return list(float(int(h[i:i+2], 16)/255) for i in (0, 2, 4))

class Object3D:
  def __init__(self, _name="Object", offset_pos=None, trace_params=None):
    self.name = _name
    self.uuid = f"{self.name.replace(' ', '_')}_{str(uuid.uuid4())}"
    self.components = []
    self.children = []
    self.parent = None
    self.local_transform = Transform(translation=offset_pos)
    self.transform = Transform()
    self.trace_type = TraceType.JOINT
    self.trace_params = trace_params if trace_params is not None else {}
    self.visible = False
    self.prev_visible = True
    self.vtk_source = None
    self.vtk_actor = None
    self.plotly_renderer = PlotlyRenderer(self)
  
    
  def forward_kinematics(self):
    warnings.warn(f"forward_kinematics() {IMPL_MISSING_MSG}")
  
  def inverse_kinematics(self):
    warnings.warn(f"inverse_kinematics() {IMPL_MISSING_MSG}")
    
  def update(self, dbg_prefix=""):
    try:
      dbg = f"{dbg_prefix}- Updating {self.name} Transform "
      # print(f"New transform for: {self.name}: {self.transform.mat}")
      self.local_transform.update()
      if self.parent is not None:
        dbg += f"Using parent ({self.parent.name}) transform"
        self.transform = Transform.combine(self.parent.transform, self.local_transform)
      else:
        self.transform = self.local_transform
      
      for child in self.children:
        child.update(dbg_prefix=dbg_prefix)
    except Exception as e:
      print(f"Exception updating {self.name} transform {e}")
      # print(f"Exception combining parent and child transform {e}")
      
  def translate(self, translation):
    self.local_transform.set_translation(translation[0], translation[1], translation[2])
    
  def rotate(self, euler_angles):
    # print(f"Rotating {self.name} ({self.uuid}) with: {euler_angles}")
    self.local_transform.set_rotation(*euler_angles)
    
  # I know this is conceputally not right here since this is about the 3D model and joints and not the actual front end
  # but look, it's much easier this way!
  def set_visibility(self, vis, propagate=True):
    if self.visible != self.prev_visible:
      self.prev_visible = self.visible
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
    points = [self.transform.position]
    # if self.parent is not None:
    #   points = [self.parent.transform.position] + points
    if len(self.children) > 0 is not None:
      points = points + [self.children[0].transform.position] 
    return points
  
  def get_vtk_model_data(self, draw_children=True, dbg_prefix=""):
    thickness = 8
    radius = 10
    points = self.get_trace_points()
    color =  hex_to_rgb(self.trace_params.get('color', "#FFFFFF"))
    orientation = self.transform.get_euler_angles(order="zxy")
    model_data = []
    p1 = list(points[0][0:3])
    # I really don't get why the orientation does not work, everything seems ok except for the orientation of these stupid cubes
    opacity = 1 if self.visible else 0
    joint_origin_point ={
      'id': self.uuid+"point",
      'vtkClass': 'vtkSphereSource',
      'property': {
        'opacity': opacity,
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
          'opacity': opacity,
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
          'opacity': opacity,
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
    # print(model_data)
    return model_data
  
  
  def update_vtk_model_data(self, draw_children=True, dbg_prefix=""):
    model_data = []
    points = self.get_trace_points()
    # print(f"{self.name} - Visible: {self.visible} - Prev Visible: {self.prev_visible}")
    if not self.visible:
      if self.visible == self.prev_visible:
        # print(f"No model update: {self.name}")
        joint_origin =  {'property': dash.no_update, 'actor': dash.no_update, 'state': dash.no_update}
        model_data.append(joint_origin)
        if len(points) > 1:
          joint_line =  {'property': dash.no_update, 'actor': dash.no_update, 'state': dash.no_update}
          joint_cube =  {'property': dash.no_update, 'actor': dash.no_update, 'state': dash.no_update}
          model_data.append(joint_line)
          model_data.append(joint_cube)
        if not draw_children:
          return model_data
        for child in self.children:
          child_model = child.update_vtk_model_data(draw_children=False, dbg_prefix=dbg_prefix)
          if child_model is not None and len(child_model) > 0:
            model_data += child_model
        return model_data
    opacity = 1 if self.visible else 0
    p1 = list(points[0][0:3])
    orientation = self.transform.get_euler_angles(order="zxy")
    joint_origin =  {
      'property': {
        'opacity': opacity
      },
      'actor': {
        'origin': p1,
        'orientation': orientation
        },
      'state': {
        "center": p1
      }
    }
    model_data.append(joint_origin)
    
    if len(points) > 1:
      p2 = list(points[1][0:3])
      length = v_dist(p1, p2)
      joint_line =  {
        'property': {
          'opacity': opacity
        },
        'actor': {},
        'state': {'point1': p1, 'point2': p2}}
      model_data.append(joint_line)
      
      joint_cube =  {
        'property': {
          'opacity': opacity
        },
        'actor': {
          'origin': p1,
          'orientation': orientation,
        },
        'state': {
          'center': [p1[0], p1[1], p1[2]+length*0.5],
        }
      }
      model_data.append(joint_cube)
    print(f"VTK Model model update: {self.name}")
    if not draw_children:
      return model_data
    
    dbg_prefix += "  "
    for child in self.children:
      child_model = child.update_vtk_model_data(draw_children=False, dbg_prefix=dbg_prefix)
      if child_model is not None and len(child_model) > 0:
        model_data += child_model
    # print(model_data)
    return model_data
  
  def vtk_update(self):
    points = self.get_trace_points()
    orientation = self.transform.get_euler_angles(order="zxy")
    p1 = list(points[0][0:3])
    if len(points) > 1:
      p2 = list(points[1][0:3])
      length = v_dist(p1, p2)
      if self.vtk_source is not None:
        self.vtk_source.SetCenter([p1[0], p1[1], p1[2]+length*0.5])
      if self.vtk_actor is not None:
        self.vtk_actor.SetOrigin(p1)
        self.vtk_actor.SetOrientation(orientation)
    
  def draw_plotly(self, fig_data, draw_children=True, dbg_prefix=""):
    self.plotly_renderer.draw(fig_data, draw_children, dbg_prefix)
    return fig_data