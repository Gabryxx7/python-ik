import uuid
import numpy as np
import math
from mathutils import Matrix
from copy import deepcopy
from scipy.spatial.transform import Rotation as R

"""_summary_
Conversions Notes: https://www.euclideanspace.com/maths/geometry/rotations/conversions/index.htm
"""

class Quaternion:
  
  @staticmethod
  def convert_angles(angles):
    return angles
    # return [360.0+angle if angle < 0 else angle for angle in angles]
  
  def quaternion_from_rotation_matrix(transform):
    quat = Quaternion()
    try:
      matrix = transform.mat[0:3, 0:3]
      matrix = np.array(matrix)
      m00, m01, m02 = matrix[0]
      m10, m11, m12 = matrix[1]
      m20, m21, m22 = matrix[2]
      tr = m00 + m11 + m22

      if tr > 0:
        S = math.sqrt(tr+1.0) * 2 # S=4*qw 
        qw = 0.25 * S
        qx = (m21 - m12) / S
        qy = (m02 - m20) / S 
        qz = (m10 - m01) / S 
      elif (m00 > m11) and (m00 > m22):
        S = math.sqrt(1.0 + m00 - m11 - m22) * 2 # S=4*qx 
        qw = (m21 - m12) / S
        qx = 0.25 * S
        qy = (m01 + m10) / S 
        qz = (m02 + m20) / S 
      elif m11 > m22:
        S = math.sqrt(1.0 + m11 - m00 - m22) * 2 # S=4*qy
        qw = (m02 - m20) / S
        qx = (m01 + m10) / S 
        qy = 0.25 * S
        qz = (m12 + m21) / S 
      else:
        S = math.sqrt(1.0 + m22 - m00 - m11) * 2 # S=4*qz
        qw = (m10 - m01) / S
        qx = (m02 + m20) / S
        qy = (m12 + m21) / S
        qz = 0.25 * S
      quat.x = qx
      quat.y = qy
      quat.z = qz
      quat.w = qw
    except Exception as e:
      print(f"EXCEPTION getting Quaternion from rotation matrix: {e}")
    return quat
      
  @staticmethod
  def quaternion_from_angles(alpha, beta, gamma):
    return Quaternion.quaternion_from_rpt(math.radians(alpha), math.radians(beta), math.radians(gamma))
    
  @staticmethod
  def quaternion_from_radians(alpha, beta, gamma):
    return Quaternion.quaternion_from_rpt(alpha, beta, gamma)
  
  @staticmethod
  def quaternion_from_rpt(roll, pitch, yaw):
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy - sr * cp * sy
    z = cr * cp * sy - sr * sp * cy
    return [x, y, z, w]
    
  
  @staticmethod
  def euler_from_quaternion(q):
    w, x, y, z = q.w, q.x, q.y, q.z
    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = np.degrees(np.arctan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = np.where(t2>+1.0,+1.0,t2)
    #t2 = +1.0 if t2 > +1.0 else t2

    t2 = np.where(t2<-1.0, -1.0, t2)
    #t2 = -1.0 if t2 < -1.0 else t2
    Y = np.degrees(np.arcsin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = np.degrees(np.arctan2(t3, t4))

    return Quaternion.convert_angles([X, Y, Z ])
  
  @staticmethod
  def euler_from_quaternion_old(q):
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
    
    roll_x = math.degrees(roll_x)
    pitch_y = math.degrees(pitch_y)
    yaw_z = math.degrees(yaw_z)
    return Quaternion.convert_angles([roll_x, pitch_y, yaw_z]) # in radians
    # return [roll_x, pitch_y, yaw_z] # in radians
  

  def to_string(self):
    return f"[ x: {self.x:.2f}, y: {self.y:.2f}, z: {self.z:.2f}, w: {self.w:.2f} ]"
  def __str__(self):
      return self.to_string()
  def __repr__(self):
      return self.to_string()
  
  def copy(self):
    return Quaternion(self.x, self.y, self.z, self.w)
  
  def to_list(self):
    return [self.x, self.y, self.z, self.w]
  
  def __init__(self, roll=0, pitch=0, yaw=0):
    self.rpy = [roll, pitch, yaw]
    self.roll = self.rpy[0]
    self.pitch = self.rpy[1]
    self.yaw = self.rpy[2]
    self.quat = Quaternion.quaternion_from_angles(roll, pitch, yaw)
    self.x = self.quat[0]
    self.y = self.quat[1]
    self.z = self.quat[2]
    self.w = self.quat[3]
    # comp = [0.0, 0.0, 0.0, 0.0]
    # l = args
    # if len(args) == 1:
    #   l = args[0]
    # for i in range(0, min(len(l), len(comp))):
    #   comp[i] = l[i]
    # self.x = comp[0]
    # self.y = comp[1]
    # self.z = comp[2]
    # self.w = comp[3]
    # self.rpy = Quaternion.quaternion_to_euler_angle_vectorized(self)
    

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