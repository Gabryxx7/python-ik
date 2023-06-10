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
  def euler_from_quaternion(q):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    """
    w, x, y, z = q.w, q.x, q.y, q.z
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    return [math.degrees(roll_x), math.degrees(pitch_y), math.degrees(yaw_z)] # in radians
    # return [roll_x, pitch_y, yaw_z] # in radians
  

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
    self.rpy = Quaternion.euler_from_quaternion(self)
    self.roll = self.rpy[0]
    self.pitch = self.rpy[1]
    self.yaw = self.rpy[2]
    

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