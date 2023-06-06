import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from models.basic.joint import *
from models.basic.model import Model
import math
from models.basic.plane import Plane

class Circle(Plane):
  def __init__(self, _name="Circle", offset_pos=None, origin=None, trace_params=None, radius=20):
    super().__init__(_name, offset_pos, origin, trace_params)
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
    # h = self.absolute_pos[2]
    h = 0
    theta = np.linspace(0, 2*np.pi, nt)
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    z = h*np.ones(theta.shape)
    return x, y, z
  
  def draw(self, fig_data):
    fig_data = super().draw(fig_data, draw_children=False)
    return fig_data