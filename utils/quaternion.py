import uuid
import numpy as np
import math
from mathutils import Matrix
from copy import deepcopy
from scipy.spatial.transform import Rotation as R

class Quaternion:
  @staticmethod
  def quaternion_from_angles(alpha, beta, gamma):
    return Quaternion.quaternion_from_rpt(math.radians(alpha), math.radians(beta), math.radians(gamma))
    
  @staticmethod
  def quaternion_from_radians(alpha, beta, gamma):
    return Quaternion.quaternion_from_rpt(alpha, beta, gamma)
  
  @staticmethod
  def quaternion_from_rpt(roll, pitch, yaw):
    cr = math.cos(roll * 0.5);
    sr = math.sin(roll * 0.5);
    cp = math.cos(pitch * 0.5);
    sp = math.sin(pitch * 0.5);
    cy = math.cos(yaw * 0.5);
    sy = math.sin(yaw * 0.5);
    w = cr * cp * cy + sr * sp * sy;
    x = sr * cp * cy - cr * sp * sy;
    y = cr * sp * cy + sr * cp * sy;
    z = cr * cp * sy - sr * sp * cy;
    return Quaternion([z, y, -x, w])
  
  
  @staticmethod
  def quaternion_to_rpt(q):
    # q = [w, x, y, z]
    w, x, y, z = 0, 1, 2, 3
    # roll (x-axis rotation)
    sinp = math.sqrt(1 + 2 * (q.w * q.y - q.x * q.z));
    cosp = math.sqrt(1 - 2 * (q.w * q.y - q.x * q.z));
    roll = 2 * math.atan2(sinp, cosp) - math.pi / 2;

    # pitch (y-axis rotation)
    sinr_cosp = 2 * (q.w * q.x + q.y * q.z);
    cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y);
    pitch = math.atan2(sinr_cosp, cosr_cosp);

    # yaw (z-axis rotation)
    siny_cosp = 2 * (q.w * q.z + q.x * q.y);
    cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z);
    yaw = math.atan2(siny_cosp, cosy_cosp);

    return [-math.degrees(roll), math.degrees(pitch), math.degrees(yaw)]

  def to_string(self):
    return f"[ x: {self.x}, y: {self.y}, z: {self.z}, w: {self.w} ]"
  def __str__(self):
      return self.to_string()
  def __repr__(self):
      return self.to_string()
  
  def copy(self):
    return Quaternion(self.x, self.y, self.z, self.w)
  
  def to_list(self):
    return [self.x, self.y, self.z, self.w]
  
  def __init__(self, *args):
    comp = [0.0, 0.0, 0.0, 1.0]
    l = args
    if len(args) == 1:
      l = args[0]
    for i in range(0, min(len(l), len(comp))):
      comp[i] = l[i]
    self.x = comp[0]
    self.y = comp[1]
    self.z = comp[2]
    self.w = comp[3]
    

if __name__ == '__main__':
  print(Quaternion(2,2))
  print(Quaternion([2,2]))
  print()
  print(Quaternion(3,3,3))
  print(Quaternion([3,3,3]))
  print()
  print(Quaternion(4,4,4,4))
  print(Quaternion([4,4,4,4]))
  print()
  print(Quaternion(5,5,5,5,5))
  print(Quaternion([5,5,5,5,5]))
  print()