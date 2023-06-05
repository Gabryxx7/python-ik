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
  "name": "Circle",
  "showlegend": True,
  "type": "mesh3d",
  "mode": "lines+markers",
  "opacity": 0.5,
  "color": "#ff6348",
  "x": [],
  "y": [],
  "z": []
}

class Circle(IModel):
  def __init__(self, _name, _origin, radius=20):
    self.name = _name
    self.next = None
    self.radius = radius
    self.uuid = f"Plane_{str(uuid.uuid4())}"
    self.absolute_pos = deepcopy(_origin)
    self.trace = None
    self.visible = False
    self.color = "#ff6348"
        
  def get_boundary_circle(self, nt=100):
    """
    r - boundary circle radius
    h - height above xOy-plane where the circle is included
    returns the circle parameterization
    """
    r = self.radius
    h = self.absolute_pos[2]
    theta = np.linspace(0, 2*np.pi, nt)
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    z = h*np.ones(theta.shape)
    return x, y, z
      
  def make_trace(self):
    trace = deepcopy(DEFAULT_PLANE_TRACE)
    trace['name'] = self.name
    trace['uuid'] = self.uuid
    return trace
        
  def set_visibility(self, vis):
    self.visible = vis
  
  def draw(self, figure_data):
    trace = self.get_trace(figure_data)
    x, y, z = self.get_boundary_circle()
    trace['x'] = x
    trace['y'] = y
    trace['z'] = z
    trace['visible'] = self.visible
    trace['color'] = self.color
    return figure_data