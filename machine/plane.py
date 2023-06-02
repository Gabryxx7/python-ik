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
  "name": "Plane Triangle",
  "showlegend": True,
  "type": "mesh3d",
  "mode": "lines+markers",
  "opacity": 0.5,
  "color": "#ff6348",
  "x": [],
  "y": [],
  "z": []
}

class Plane(IModel):
  def __init__(self, _name, _origin):
    self.name = _name
    self.next = None
    self.uuid = f"Plane_{str(uuid.uuid4())}"
    self.absolute_pos = deepcopy(_origin)
    self.tm = TransformManager()
    self.joints = []
    self.origin = Joint("Origin", self.absolute_pos)
    self.origin.transform = pt.transform_from_pq(np.hstack((np.array(self.absolute_pos), pr.q_id)))
    self.trace = None
    self.visible = False
    self.arms = []
    self.pistons = []
    
  def add_arm(self, arm):
    self.arms.append(arm)
    
  def add_piston(self, piston):
    self.pistons.append(piston)
    
  def make_trace(self):
    trace = deepcopy(DEFAULT_PLANE_TRACE)
    trace['name'] = self.name
    trace['uuid'] = self.uuid
    return trace
  
  def forward_kinematics(self):
    print("\n\nStarting Forward Kinematics:")
    for arm in self.arms:
      arm.forward_kinematics()
        
  def set_visibility(self, vis):
    self.visible = vis
    for j in self.joints:
      j.set_visibility(vis)
    for a in self.arms:
      a.set_visibility(vis)
    for p in self.pistons:
      p.set_visibility(vis)
              
  def draw(self, figure_data):
    trace = self.get_trace(figure_data)
    points = [p.joints[-1].absolute_pos for p in self.arms]
    trace['x'] = [float(p[AXIS_ORDER_CONVENTION[0]]) for p in points]
    trace['y'] = [float(p[AXIS_ORDER_CONVENTION[1]]) for p in points]
    trace['z'] = [float(p[AXIS_ORDER_CONVENTION[2]]) for p in points]
    trace['visible'] = self.visible
    return figure_data
    
  """
  http://ww2.me.ntu.edu.tw/~measlab/download/2003/sensitivity%20of%203-PRS%202003.pdf
    Input:
      z_T - height of platform w.r.t. inertial frame at the bottom
      alpha - roll
      beta - pitch
      Intermittent output:
      gamma - yaw
      x_T - x position w.r.t. IF
      y_T - y pos w.r.t. IF
    Actual output:
      H1, H2, H3 - heights of the legs
  """  
  def Inverse_Kinematics(zT, alpha, beta):
    Rbig = 22.645  # outer radius
    Rsmall = 15  # inner radius
    gamma = -np.arctan(np.sin(alpha) * np.sin(beta) / (np.cos(alpha) + np.cos(beta)))
    xT = Rbig / 2 + Rsmall / 2 * (
                np.cos(beta) * np.cos(gamma) + np.sin(alpha) * np.sin(beta) * np.sin(gamma) - np.cos(alpha) * np.cos(
            gamma))
    yT = -Rsmall * (np.cos(alpha) * np.sin(gamma) + np.sin(alpha) * np.sin(beta) * np.cos(gamma))
    
    Rx = np.array([[1, 0, 0], [0, np.cos(alpha), -np.sin(alpha)], [0, np.sin(alpha), np.cos(alpha)]])
    Ry = np.array([[np.cos(beta), 0, np.sin(beta)], [0, 1, 0], [-np.sin(beta), 0, np.cos(beta)]])
    Rz = np.array([[np.cos(gamma), -np.sin(gamma), 0], [np.sin(gamma), np.cos(gamma), 0], [0, 0, 1]])
    
    Txyz = np.matmul(np.matmul(Rx, Ry), Rz)
    Txyz = np.matmul(np.eye(4, 3), Txyz)
    Txyz = np.matmul(Txyz, np.eye(3, 4))
    v = np.array([xT, yT, zT, 1])
    
    for i in range(4):
      Txyz[i][3] += v[i]
      
    R1 = np.array([3 / 2 * Rbig, 0, 1])
    R2 = np.array([0, math.sqrt(3) / 2 * Rbig, 1])
    R3 = np.array([0, -math.sqrt(3) / 2 * Rbig, 1])
    
    b1 = np.array([[Rsmall], [0], [0], [1]])
    b2 = np.array([[-Rsmall / 2], [math.sqrt(3) / 2 * Rsmall], [0], [1]])
    b3 = np.array([[-Rsmall / 2], [-math.sqrt(3) / 2 * Rsmall], [0], [1]])
    
    b10 = np.matmul(Txyz, b1)
    b20 = np.matmul(Txyz, b2)
    b30 = np.matmul(Txyz, b3)
    
    l = 25
    
    H1 = b10[2][0] - math.sqrt(l ** 2 - (R1[0] - b10[0][0]) ** 2 - (R1[1] - b10[1][0]) ** 2)
    H2 = b20[2][0] - math.sqrt(l ** 2 - (R2[0] - b20[0][0]) ** 2 - (R2[1] - b20[1][0]) ** 2)
    H3 = b30[2][0] - math.sqrt(l ** 2 - (R3[0] - b30[0][0]) ** 2 - (R3[1] - b30[1][0]) ** 2)
    
    return H1, H2, H3, xT, yT, gamma