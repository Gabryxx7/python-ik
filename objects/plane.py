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
    # vertex.set_visibility(False) # 
    # self.children.append(vertex)
  
  def forward_kinematics(self):
    self.update()
    
  def draw_plotly(self, fig_data, draw_children=False, dbg_prefix=""):
    self.plotly_renderer.draw(fig_data, draw_children=False, dbg_prefix=dbg_prefix)
    
    for child in self.children:
      if(child.trace_type == ModelType.PLANE):
        fig_data = child.draw_plotly(fig_data, draw_children=False, dbg_prefix=dbg_prefix)
    return fig_data
    
  # def set_visibility(self, vis, propagate=True):
  #   # This is just to avoid the plane's vertices (which are actually joints) tp show up in the  legend and the plot
  #   # We have already set the visibility to False when adding the vertex anyway
  #   super().set_visibility(vis, propagate=False)
  #   for child in self.children:
  #     child.set_visibility(vis)
  
  def get_trace_points(self):
    return [x.transform.position for x in self.children]
    