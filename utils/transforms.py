import numpy as np
import math
from scipy.spatial.transform import Rotation as R
try:
  from utils.quaternion import Quaternion
except Exception as e:
  from quaternion import Quaternion
  

X, Y, Z = 0,1,2
AXIS_ORDER = [X, Y, Z]

class Transform:
  @staticmethod
  def rotation_from_quaternion(Q):
    """
    Covert a quaternion into a full three-dimensional rotation matrix.

    Input
    :param Q: A 4 element array representing the quaternion (q0,q1,q2,q3) 

    Output
    :return: A 3x3 element matrix representing the full 3D rotation matrix. 
            This rotation matrix converts a point in the local reference 
            frame to a point in the global reference frame.
    """
    # Extract the values from Q
    q0 = Q.w
    q1 = Q.x
    q2 = Q.y
    q3 = Q.z
    
    # First row of the rotation matrix
    r00 = 2 * (q0 * q0 + q1 * q1) - 1
    r01 = 2 * (q1 * q2 - q0 * q3)
    r02 = 2 * (q1 * q3 + q0 * q2)
    
    # Second row of the rotation matrix
    r10 = 2 * (q1 * q2 + q0 * q3)
    r11 = 2 * (q0 * q0 + q2 * q2) - 1
    r12 = 2 * (q2 * q3 - q0 * q1)
    
    # Third row of the rotation matrix
    r20 = 2 * (q1 * q3 - q0 * q2)
    r21 = 2 * (q2 * q3 + q0 * q1)
    r22 = 2 * (q0 * q0 + q3 * q3) - 1
    
    # 3x3 rotation matrix
    rot_matrix = np.matrix([[r00,   r01,    r02],
                            [r10,   r11,    r12],
                            [r20,   r21,    r22]])
    return Transform.process_rotation_matrix(rot_matrix)
  
  @staticmethod
  def process_rotation_matrix(R):
    """ 
    Before we can use the Rotation Matrix we need to normalize it and convert it to a 4x4 matrix.add()
    I'm using pytransform3d matrix normalization function
    Then I'm creating an identity 4x4 matrix (with 1s in the main diagonal) and replacing the inner 3x3 matrix with the rotation matrix
    Now it's ready to be combined with translation and rotation
    """
    R = Transform.norm_matrix(R)
    rot_mat = np.identity(4)
    rot_mat[:3, :3] = R
    return rot_mat
  
  @staticmethod
  def norm_vector(v):
    """ From: https://dfki-ric.github.io/pytransform3d/_modules/pytransform3d/rotations/_utils.html#norm_matrix
    Normalize vector.

    Parameters
    ----------
    v : array-like, shape (n,)
        nd vector

    Returns
    -------
    u : array, shape (n,)
        nd unit vector with norm 1 or the zero vector
    """
    norm = np.linalg.norm(v)
    if norm == 0.0:
        return v

    return np.asarray(v) / norm


  @staticmethod
  def norm_matrix(R):
    """ From: https://dfki-ric.github.io/pytransform3d/_modules/pytransform3d/rotations/_utils.html#norm_matrix
    Orthonormalize rotation matrix.

    Parameters
    ----------
    R : array-like, shape (3, 3)
        Rotation matrix with small numerical errors

    Returns
    -------
    R : array, shape (3, 3)
        Normalized rotation matrix
    """
    R = np.asarray(R)
    c2 = R[:, 1]
    c3 = Transform.norm_vector(R[:, 2])
    c1 = Transform.norm_vector(np.cross(c2, c3))
    c2 = Transform.norm_vector(np.cross(c3, c1))
    return np.column_stack((c1, c2, c3))
  
  @staticmethod
  def rotation_from_axis(x, y, z):
    return Transform.rotation_from_angles(x, y, z)
  
  @staticmethod
  def rotation_from_angles(phi, theta, psi):
    return Transform.rotation_from_radians(math.radians(phi), math.radians(theta), math.radians(psi))
  
  @staticmethod
  def rotation_from_rpt(roll, pitch, yaw):
    return Transform.rotation_from_angles(roll, pitch, yaw)
  
  @staticmethod
  def rotation_from_radians(phi, theta, psi):
    Rx = np.matrix([[       1.0,             0.0,            0.0,           ],
                    [       0.0,        math.cos(phi),   -math.sin(phi),    ],
                    [       0.0,        math.sin(phi),    math.cos(phi),    ]])
    
    Ry = np.matrix([[  math.cos(theta),      0.0,       math.sin(theta),    ],
                    [       0.0,             1.0,            0.0,           ],
                    [ -math.sin(theta),      0.0,       math.cos(theta),    ]])
    
    Rz = np.matrix([[  math.cos(psi),   -math.sin(psi),      0.0,           ],
                    [  math.sin(psi),    math.cos(psi),      0.0,           ],
                    [       0.0,             0.0,            1.0,           ]])
    rotations = [Rx, Ry, Rz]
    rotation_matrix = rotations[AXIS_ORDER[0]] @ rotations[AXIS_ORDER[1]] @ rotations[AXIS_ORDER[2]]
    return Transform.process_rotation_matrix(rotation_matrix)
  
  @staticmethod
  def scale_matrix(X, Y, Z):
    scale_mat = np.matrix([ [   X,   0.0,   0.0,  0.0  ],
                            [  0.0,   Y,    0.0,  0.0  ],
                            [  0.0,  0.0,    Z,   0.0  ],
                            [  0.0,  0.0,   0.0,  1.0  ]])
    return scale_mat
  
  @staticmethod
  def translation_matrix(X, Y, Z):
    translatin_mat = np.matrix([[  1.0,   0.0,   0.0,   X  ],
                                [  0.0,   1.0,   0.0,   Y  ],
                                [  0.0,   0.0,   1.0,   Z  ],
                                [  0.0,   0.0,   0.0,  1.0 ]])
    return translatin_mat
  
  @staticmethod
  def combine(t1, t2):
    combined =  t1.mat @ t2.mat
    return Transform.from_matrix(combined)
    
  
  @staticmethod
  def from_matrix(mat):
    t = Transform()
    t.mat = mat
    return t
  
    
  @staticmethod
  def make_transform(translation=None, scale=None, rotation=None, quaternion=None):
    t = None
    try:
      t = Transform()
      t.translation = [0,0,0] if translation is None else translation
      t.translation_matrix = Transform.translation_matrix(t.translation[0], t.translation[1], t.translation[2])
      t.scale = [1,1,1] if scale is None else scale
      t.scale_matrix = Transform.scale_matrix(t.scale[0], t.scale[1], t.scale[2])
      
      if quaternion is None:
        t.rotation = rotation if rotation is not None else [0,0,0]
        t.quaternion = Quaternion.quaternion_from_angles(t.rotation[0], t.rotation[1], t.rotation[2])
        t.rotation_matrix = Transform.rotation_from_angles(t.rotation[0], t.rotation[1], t.rotation[2])
      else:
        t.quaternion = quaternion.copy() if quaternion is not None else Quaternion()
        t.rotation_matrix = Transform.rotation_from_quaternion(t.quaternion)
      t.mat = t.translation_matrix @ t.rotation_matrix @ t.scale_matrix
    except Exception as e:
      print(f"Error making Transform rotation: {e}")
    return t
    
  def __init__(self):
    self.translation = [0,0,0]
    self.translation_matrix = Transform.translation_matrix(self.translation[0], self.translation[1], self.translation[2])
    self.scale = [1,1,1]
    self.scale_matrix = Transform.scale_matrix(self.scale[0], self.scale[1], self.scale[2])
    self.quaternion = Quaternion()
    self.rotation = [0,0,0]
    self.rotation_matrix = Transform.rotation_from_angles(self.rotation[0], self.rotation[1], self.rotation[2])
    self.mat = self.translation_matrix @ self.rotation_matrix @ self.scale_matrix
    

if __name__ == '__main__':
  t = Transform.make_transform(rotation=[37,78,121])
  print("\n Transformation Mat:")
  print(t.mat)
  print("\n Quaternion: ")
  print(t.quaternion)
  print("\n Rot Matrix: ")
  print(t.rotation_matrix)
  print("\n Rot Matrix from Quat: ")
  print(Transform.rotation_from_quaternion(t.quaternion))
  print("\n Rot Matrix from Quat Scipy: ")
  print(R.from_quat(t.quaternion.to_list()).as_matrix())
  print("\n Angles from Quat:")
  print(Quaternion.quaternion_to_rpt(t.quaternion))