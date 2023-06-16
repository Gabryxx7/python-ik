import dash
import warnings
import uuid
import numpy as np
from copy import deepcopy
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from components.Transform import Transform
from components.PlotlyRenderer import PlotlyRenderer, ModelType
from components.VtkRenderer import VtkModel
from utils.quaternion import Quaternion

IMPL_MISSING_MSG = "implementatiom missing (did you override it in your new model class?)"

v_dist = lambda p, orig=[0,0,0]: (np.linalg.norm(np.array(orig) - np.array(p)))

class Object3D:
  def __init__(self, _name="Object", offset_pos=None, trace_params=None):
    self.name = _name
    self.uuid = f"{self.name.replace(' ', '_')}_{str(uuid.uuid4())}"
    self.components = []
    self.renderers = []
    self.children = []
    self.parent = None
    self.local_transform = Transform(translation=offset_pos)
    self.transform = Transform()
    self.trace_type = ModelType.JOINT
    self.trace_params = trace_params if trace_params is not None else {}
    self.visible = False
    self.prev_visible = True
    self.vtk_source = None
    self.vtk_actor = None
    self.plotly_renderer = PlotlyRenderer(self)
    self.vtk_renderer = VtkModel(self)
  
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
  
  def draw_plotly(self, fig_data, draw_children=True, dbg_prefix=""):
    self.plotly_renderer.draw(fig_data, draw_children, dbg_prefix)
    return fig_data