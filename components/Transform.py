import numpy as np
import math
from scipy.spatial.transform import Rotation as sciR
from utils.RotationMatrix import RotationMatrix
try:
  from utils.quaternion import Quaternion
except Exception as e:
  print(f"Exception importin Quaternion: {e}")
  from quaternion import Quaternion



X, Y, Z = 0,1,2
AXIS_ORDER = [X, Y, Z]

  
class Transform:
  def scale_matrix(X, Y, Z):
    scale_mat = np.matrix([ [   X,   0.0,   0.0,  0.0  ],
                            [  0.0,   Y,    0.0,  0.0  ],
                            [  0.0,  0.0,    Z,   0.0  ],
                            [  0.0,  0.0,   0.0,  1.0  ]])
    return scale_mat
  
  @staticmethod
  def translation_matrix(X, Y, Z):
    translation_mat = np.matrix([[  1.0,   0.0,   0.0,   X  ],
                                [  0.0,   1.0,   0.0,   Y  ],
                                [  0.0,   0.0,   1.0,   Z  ],
                                [  0.0,   0.0,   0.0,  1.0 ]])
    return translation_mat
  
  @staticmethod
  def combine(t1, t2):
    # combined =  t1.mat @ t2.mat
    combined_mat = np.dot(t1.mat, t2.mat)
    return Transform.from_matrix(combined_mat)
  
  @staticmethod
  def from_matrix(mat):
    t = Transform()
    t.mat = mat
    t.position = np.array(t.mat@np.array([0,0,0,1])).flatten()
    t.rotation = t.get_euler_angles(order="zyx")
    t.quaternion = Quaternion(t.rotation[0], t.rotation[1], t.rotation[2])
    t.translation = t.get_translation()
    return t
  
  def get_translation(self):
    t = self.mat[0:3, 3]
    return t.flatten().tolist()[0]
  
  # From: https://github.com/mrdoob/three.js/blob/dev/src/math/Euler.js#L105
  # http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToAngle/
  # If you're applying rotations in the order XYZ then you need to retrieve the angles using the inverse order ZYX
  def get_euler_angles(self, order="zyx"):
    matrix = self.mat[0:3, 0:3]
    matrix = np.array(matrix)
    m11, m12, m13 = matrix[0]
    m21, m22, m23 = matrix[1]
    m31, m32, m33 = matrix[2]
    
    if order == "xyz":
      y = math.asin(np.clip(m13, -1, 1))
      # Checks for gymbal lock
      if abs(m13) < 0.999:
        x = math.atan2(-m23, m33)
        z = math.atan2(-m12, m11)
      else:
        x = math.atans(m32, m22)
        z = 0
    elif order == "yxz":
      x = math.asin(-np.clip(m23, -1, 1))
      # Checks for gymbal lock
      if abs(m23) < 0.999:
        y = math.atan2(m13, m33)
        z = math.atan2(m21, m22)
      else:
        y = math.atan2(-m31, m11)
        z = 0
    elif order == "zxy":
      x = math.asin(np.clip(m32, -1, 1))
      # Checks for gymbal lock
      if abs(m32) < 0.999:
        y = math.atan2(-m31, m33)
        z = math.atan2(-m12, m22)
      else:
        y = 0
        z = math.atan2(m21, m11)
    elif order == "zyx":
      y = math.asin(-np.clip(m31, -1, 1))
      # Checks for gymbal lock
      if abs(m31) < 0.999:
        x = math.atan2(m32, m33)
        z = math.atan2(m21, m11)
      else:
        x = 0
        z = math.atan2(-m12, m22)
      
    x = math.degrees(x)
    y = math.degrees(y)
    z = math.degrees(z)
    return [x, y, z]
    # return [roll, pitch, yaw]
  
  @staticmethod
  def normalize_vector(v):
    """ From: https://dfki-ric.github.io/pytransform3d/_modules/pytransform3d/rotations/_utils.html#norm_matrix
    Normalize vector.
    - Parameters:
      v : array-like, shape (n,)nd vector
    - Returns:
      u : array, shape (n,) nd unit vector with norm 1 or the zero vector
    """
    norm = np.linalg.norm(v)
    if norm == 0.0:
        return v
    return np.asarray(v) / norm
  
  # How to get axes directions
  # 1. You obviously need the updated transform of your joint that includes translation and rotation
  # 2. Given that transform, apply it to the origin (absolute pos) and then to an offset origin depending on which axes you're plotting
  # For instance, if you want the UP vector (x axis) you'll need to apply the transform to [0,0,0] and then [0,1,0]
  # Get the normalized difference between the new point and the origin. That will give you the direction from the origin to the new point
  def get_direction_vector(self, d=[0,0,0]):
    origin = np.array(self.mat@np.array([0,0,0,1])).flatten()
    offset_point = np.array(self.mat@np.array([d[0],d[1],d[2],1])).flatten()
    dist_vec = offset_point - origin
    return Transform.normalize_vector(dist_vec)
  
  def up_vec(self):
    return self.get_direction_vector([0,1,0])
    
  def right_vec(self):
    return self.get_direction_vector([1,0,0])
    
  def forward_vec(self):
    return self.get_direction_vector([0,0,1])
  
  def set_rotation(self, x=None, y=None, z=None):
    self.rotation[0] = self.rotation[0] if x is None else x
    self.rotation[1] = self.rotation[1] if y is None else y
    self.rotation[2] = self.rotation[2] if z is None else z
    self.quaternion = Quaternion(self.rotation[0], self.rotation[1], self.rotation[2])
    self.rotation_matrix = RotationMatrix(self.rotation[0], self.rotation[1], self.rotation[2])
    
  def set_translation(self, x=None, y=None, z=None, pos=None):
    if pos is not None:
      x = pos[0]
      y = pos[1]
      z = pos[2]
    else:
      self.translation[0] = self.translation[0] if x is None else x
      self.translation[1] = self.translation[1] if y is None else y
      self.translation[2] = self.translation[2] if z is None else z
    self.translation_matrix = Transform.translation_matrix(self.translation[0], self.translation[1], self.translation[2])
    
  def update(self):
    self.mat = self.translation_matrix @ self.rotation_matrix.to_norm_4x4() @ self.scale_matrix
    
    # Remember that the accumulated transform should always be applied to a hypothetical starting point 0 expressed in world coordinates,
    # and the last component should always be 1 (the 4th dimension used to apply transforms)
    self.position = np.array(self.mat@np.array([0,0,0,1])).flatten()
    
  def __init__(self, translation=None, rotation=None, scale=None, origin=None):
    self.origin = np.array([0,0,0, 1.0]) if origin is None else np.array([origin[0], origin[1], origin[2], 1.0])
    self.parent = None
    
    self.translation = [0,0,0] if translation is None else translation
    self.scale = [1,1,1] if scale is None else scale
    self.rotation = [0,0,0] if rotation is None else rotation
    self.quaternion = Quaternion(0,0,0)
    
    self.translation_matrix = Transform.translation_matrix(self.translation[0], self.translation[1], self.translation[2])
    self.scale_matrix = Transform.scale_matrix(self.scale[0], self.scale[1], self.scale[2])
    self.rotation_matrix = RotationMatrix(self.rotation[0], self.rotation[1], self.rotation[2])
    
    self.mat = self.translation_matrix @ self.rotation_matrix.to_norm_4x4() @ self.scale_matrix
    self.position = np.array(self.mat@np.array([0,0,0,1])).flatten()
  

if __name__ == '__main__':
  t = Transform.make_transform(rotation=[37,78,121])
  print("\n Transformation Mat:")
  print(t.mat)
  print("\n Quaternion: ")
  print(t.quaternion)
  print("\n Rot Matrix: ")
  print(t.rotation_matrix)
  print("\n Rot Matrix from Quat: ")
  print(Transform.RotationMatrix.from_quaternion(t.quaternion))
  print("\n Rot Matrix from Quat Scipy: ")
  print(sciR.from_quat(t.quaternion.to_list()).as_matrix())
  print("\n Angles from Quat:")
  print(t.quaternion.rpy)