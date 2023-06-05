import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from machine.joint import *
from machine.IModel import IModel
from machine.circle import Circle
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
    self.origin_pos = deepcopy(_origin)
    self.absolute_pos = deepcopy(_origin)
    self.tm = TransformManager()
    self.trace = None
    self.visible = False
    self.joints = []
    self.color = "#ff6348"
    self.ik_res = None
    # self.Rbig = 22.645  # outer radius
    # self.Rsmall = 15  # inner radius
    # self.l = 25
    self.Rbig = 130  # outer radius
    self.Rsmall = 70  # inner radius
    self.l = 80
    self.origin = Joint(f"{self.name}_Origin", self.absolute_pos)
    self.origin.transform = pt.transform_from_pq(np.hstack((np.array(self.absolute_pos), pr.q_id)))
    self.circles = []
    self.circles.append(Circle(f"{self.name}_Radius1", self.absolute_pos, self.Rbig, "#CEFF33"))
    self.circles.append(Circle(f"{self.name}_Radius1", self.absolute_pos, self.Rsmall, "#33E6FF"))
    # self.circles.append(Circle(f"{self.name}_Radius2", self.absolute_pos, 30))
  
  def add_joint(self, joint):
    joint.link_to(self.origin)
    self.joints.append(joint)
    
  def make_trace(self):
    trace = deepcopy(DEFAULT_PLANE_TRACE)
    trace['name'] = self.name
    trace['uuid'] = self.uuid
    return trace
  
  def forward_kinematics(self):
    self.origin.update()
    self.ik_res = self.Inverse_Kinematics(self.origin_pos[2], self.origin.quaternion[2], self.origin.quaternion[1])
    print(self.ik_res)
        
  def set_visibility(self, vis):
    self.visible = vis
    for v in self.joints:
      v.set_visibility(vis)
      
    for c in self.circles:
      c.set_visibility(vis)
    self.origin.set_visibility(vis)
  
  def draw(self, figure_data):
    trace = self.get_trace(figure_data)
    points = [x.absolute_pos for x in self.joints]
    trace['x'] = [float(p[AXIS_ORDER_CONVENTION[0]]) for p in points]
    trace['y'] = [float(p[AXIS_ORDER_CONVENTION[1]]) for p in points]
    trace['z'] = [float(p[AXIS_ORDER_CONVENTION[2]]) for p in points]
    trace['visible'] = self.visible
    trace['color'] = self.color
    # for v in self.joints:
    # for c in self.circles:
    #   c.draw(figure_data)
    figure_data = self.origin.draw(figure_data)
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
  def Inverse_Kinematics(self, zT, alpha, beta):
    print(f"IK Plane. Roll: {alpha}\tPitch: {beta}")
    
    gamma = -np.arctan(np.sin(alpha) * np.sin(beta) / (np.cos(alpha) + np.cos(beta)))
    xT = self.Rbig / 2 + self.Rsmall / 2 * (
                np.cos(beta) * np.cos(gamma) + np.sin(alpha) * np.sin(beta) * np.sin(gamma) - np.cos(alpha) * np.cos(
            gamma))
    yT = -self.Rsmall * (np.cos(alpha) * np.sin(gamma) + np.sin(alpha) * np.sin(beta) * np.cos(gamma))
    
    Rx = np.array([[1, 0, 0], [0, np.cos(alpha), -np.sin(alpha)], [0, np.sin(alpha), np.cos(alpha)]])
    Ry = np.array([[np.cos(beta), 0, np.sin(beta)], [0, 1, 0], [-np.sin(beta), 0, np.cos(beta)]])
    Rz = np.array([[np.cos(gamma), -np.sin(gamma), 0], [np.sin(gamma), np.cos(gamma), 0], [0, 0, 1]])
    
    Txyz = np.matmul(np.matmul(Rx, Ry), Rz)
    Txyz = np.matmul(np.eye(4, 3), Txyz)
    Txyz = np.matmul(Txyz, np.eye(3, 4))
    v = np.array([xT, yT, zT, 1])
    
    for i in range(4):
      Txyz[i][3] += v[i]
      
    R1 = np.array([3 / 2 * self.Rbig, 0, 1])
    R2 = np.array([0, math.sqrt(3) / 2 * self.Rbig, 1])
    R3 = np.array([0, -math.sqrt(3) / 2 * self.Rbig, 1])
    
    b1 = np.array([[self.Rsmall], [0], [0], [1]])
    b2 = np.array([[-self.Rsmall / 2], [math.sqrt(3) / 2 * self.Rsmall], [0], [1]])
    b3 = np.array([[-self.Rsmall / 2], [-math.sqrt(3) / 2 * self.Rsmall], [0], [1]])
    
    b10 = np.matmul(Txyz, b1)
    b20 = np.matmul(Txyz, b2)
    b30 = np.matmul(Txyz, b3)
    
    
    h1_before = self.l ** 2 - (R1[0] - b10[0][0]) ** 2 - (R1[1] - b10[1][0]) ** 2
    h2_before = self.l ** 2 - (R2[0] - b20[0][0]) ** 2 - (R2[1] - b20[1][0]) ** 2
    h3_before = self.l ** 2 - (R3[0] - b30[0][0]) ** 2 - (R3[1] - b30[1][0]) ** 2
    print(h1_before)
    print(h2_before)
    print(h3_before)
    H1 = b10[2][0] - math.sqrt(h1_before)
    H2 = b20[2][0] - math.sqrt(h2_before)
    H3 = b30[2][0] - math.sqrt(h3_before)
    
    return H1, H2, H3, xT, yT, gamma