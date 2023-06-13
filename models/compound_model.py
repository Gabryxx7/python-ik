import uuid
import numpy as np
from models.basic.joint import Joint
from models.basic.model import Model
from models.circle import Circle
import math

PISTON_HEIGHT = 200.0
PISTON_START_HEIGHT_RATIO = 1
PISTON_ARM_LENGTH = 50
PISTON_START_HEIGHT = PISTON_HEIGHT * PISTON_START_HEIGHT_RATIO
PLANE_INITIAL_HEIGHT = PISTON_HEIGHT*1.5

class CompoundModel(Model):
  def __init__(self, _name="Compound", offset_pos=None, trace_params=None):
    super().__init__(_name, offset_pos, trace_params)
    self.arms = []
    self.children = []
    self.planes = []
    self.trace_params['color'] = "#ff6348"
    self.ik_res = None
    # self.Rbig = 22.645  # outer radius
    # self.Rsmall = 15  # inner radius
    # self.l = 25
    self.Rbig = 130  # outer radius
    self.Rsmall = 70  # inner radius
    self.l = 80
    self.max_piston_height = PLANE_INITIAL_HEIGHT*2
    
  def add_arm(self, arm):
    self.arms.append(arm)
    
  def add_joint(self, joint):
    self.children.append(joint)
    
  def add_plane(self, plane):
    self.planes.append(plane)
    try:
      self.Rsmall = abs(np.linalg.norm(plane.origin_pos[:2] - plane.children[0].origin_pos[:2]))
      self.Rbig = self.Rsmall*1.5
      self.l = (self.Rsmall*1.2)
      # print(self.Rbig)
      # print(self.Rsmall)
      # print(self.l)
      circle_big = Circle("Circle_Big", radius=self.Rbig, trace_params={'color': '#9999ff', 'opacity': 0.3})
      circle_small = Circle("Circle_Small", radius=self.Rsmall, trace_params={'color': '#00ffcc', 'opacity': 0.3})
      circle_big.set_parent(plane)
      circle_small.set_parent(plane)
    except Exception as e:
      print(f"Exception adding circles as children {e}")
    
  def forward_kinematics(self):
    # print("\n\nStarting Forward Kinematics:")
    for plane in self.planes:
      plane.update()
      self.ik_res = self.Inverse_Kinematics(plane.origin_pos[2], plane.local_quaternion.y, plane.local_quaternion.x)
      if self.ik_res is not None:
        for i in range(0,3):
          self.arms[i].children[0].origin_pos[2] = self.ik_res[i]
        # plane.forward_kinematics()
        yaw = self.ik_res[5]
        q = plane.local_quaternion
        q.z = yaw
        # plane.rotate(q)
        print(f"Plane quat: {plane.local_quaternion}")
    for arm in self.arms:
      arm.forward_kinematics()
        
  def set_visibility(self, vis):
    super().set_visibility(vis)
    for a in self.arms:
      a.set_visibility(vis)
    for p in self.planes:
      p.set_visibility(vis)
  
  def draw_plotly(self, fig_data):
    super().draw_plotly(fig_data)
    for a in self.arms:
      fig_data = a.draw_plotly(fig_data)
    for p in self.planes:
      fig_data = p.draw_plotly(fig_data)
    return fig_data
  
  
  def get_vtk_model_data(self, draw_children=True, dbg_prefix=""):
    model_data = super().get_vtk_model_data()
    for a in self.arms:
      model_data += a.get_vtk_model_data()
    # for p in self.planes:
    #   model_data += p.get_vtk_model_data()
    return model_data
  
  
  def update_vtk_model_data(self, draw_children=True, dbg_prefix=""):
    model_data = super().update_vtk_model_data()
    for a in self.arms:
      model_data += a.update_vtk_model_data()
    # for p in self.planes:
    #   model_data += p.get_vtk_model_data()
    return model_data
  
  
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
    gamma = -np.arctan(np.sin(alpha) * np.sin(beta) / (np.cos(alpha) + np.cos(beta)))
    zT *= 1.5
    print(f"IK Plan:\n\tzT: {zT}\tRbig: {self.Rbig:.2f}\tRsmall: {self.Rsmall:.2f}\t l: {self.l:.2f}\n\tRoll: {alpha}\t\tPitch: {beta}\tYaw (calc): {gamma}")
    
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
    H1 = b10[2][0] - math.sqrt(h1_before)
    H2 = b20[2][0] - math.sqrt(h2_before)
    H3 = b30[2][0] - math.sqrt(h3_before)
    print(f"H1: {H1}\tH2: {H2}\tH3: {H3}")
    
    return H1, H2, H3, xT, yT, gamma