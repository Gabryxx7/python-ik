import uuid
import numpy as np
from models.basic.joint import *
from models.basic.model import Model
import math
from models.basic.plane import Plane

class Circle(Plane):
  def __init__(self, _name="Circle", offset_pos=None, trace_params=None, radius=20):
    super().__init__(_name, offset_pos, trace_params)
    self.radius = radius
    x,y,z = self.get_boundary_circle()
    for p in zip(x,y,z):
      self.add_vertex(list(p))
        
  def get_boundary_circle(self, nt=100):
    """
    r - boundary circle radius
    h - height above xOy-plane where the circle is included
    returns the circle parameterization
    """
    r = self.radius
    # h = self.absolute_position[2]
    h = 0
    theta = np.linspace(0, 2*np.pi, nt)
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    z = h*np.ones(theta.shape)
    return x, y, z
  
  def draw_plotly(self, fig_data, draw_children=False, dbg_prefix=""):
    fig_data = super().draw_plotly(fig_data, draw_children=False, dbg_prefix=dbg_prefix)
    return fig_data