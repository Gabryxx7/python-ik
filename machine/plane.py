import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from copy import deepcopy
from machine.joint import *
from machine.IModel import IModel

DEFAULT_PLANE_TRACE = {
  "name": "Axis Joint",
  "showlegend": True,
  "type": "mesh3d",
  "opacity": BODY_MESH_OPACITY,
  "color": BODY_MESH_COLOR,
  "x": [],
  "y": [],
  "z": [],
}

class Plane(IModel):
  def __init__(self, _name, _origin):
    self.name = _name
    self.prev = None
    self.next = None
    self.uuid = f"Plane_{str(uuid.uuid4())}"
    self.absolute_pos = deepcopy(_origin)
    self.tm = TransformManager()
    self.joints = []
    self.origin = Joint("Origin", self.absolute_pos)
    self.origin.transform = pt.transform_from_pq(np.hstack((np.array(self.absolute_pos), pr.q_id)))
    self.trace = deepcopy(DEFAULT_PLANE_TRACE)
    self.visible = True
    self.arms = []
    self.pistons = []
    
  def add_arm(self, arm):
    self.arms.append(arm)
  def add_piston(self, piston):
    self.pistons.append(piston)
  
  def add_joint(self, joint):
    self.joints.append(joint)
    if len(self.joints) > 1:
      self.joints[-1].link_to(self.joints[-2])
      self.tm.add_transform(f"joint_{self.joints[-2].name}", f"joint_{self.joints[-1].name}", self.joints[-2].transform)
      return
    print(f"Origin Linking: {self.origin.name} -> {self.joints[0].name}")
    self.joints[0].link_to(self.origin)
    
  def forward_kinematics(self):
    print("\n\nStarting Forward Kinematics:")
    for arm in self.arms:
      arm.forward_kinematics()
    # self.origin.update(dbg_prefix="\t")
    
    # for i in range(1, len(self.joints)):
    #   print(f"Calculated Transform {self.joints[i-1].name} -> {self.joints[i]}: ")
    #   print(self.joints[i].transform)
    #   # print(f"\nTM MANAGER Transform joint_{self.joints[i-1].name} to joint_{self.joints[i].name}")
    #   # t = self.tm.get_transform(f"joint_{self.joints[i-1].name}", f"joint_{self.joints[i].name}")
    #   # self.joints[i].update_from_transform(t)
    #   # print(t)
    #   print(f"Distance from Parent: {np.linalg.norm(self.joints[i-1].absolute_pos - self.joints[i].absolute_pos)}")
        
              
  def draw(self, figure_data):
    trace = self.get_trace(figure_data)
    
    points = [j.absolute_pos for j in self.joints]
    trace['x'] = [float(p[AXIS_ORDER_CONVENTION[0]]) for p in points]
    trace['y'] = [float(p[AXIS_ORDER_CONVENTION[1]]) for p in points]
    trace['z'] = [float(p[AXIS_ORDER_CONVENTION[2]]) for p in points]
    trace['visible'] = self.visible
    return figure_data
    