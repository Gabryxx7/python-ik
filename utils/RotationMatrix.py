import numpy as np
import math
from copy import deepcopy

class RotationMatrix:    
  @staticmethod
  def from_axis(x, y, z):
    return RotationMatrix.from_angles(x, y, z)
  
  @staticmethod
  def from_angles(phi, theta, psi):
    return RotationMatrix.from_radians(math.radians(phi), math.radians(theta), math.radians(psi))
  
  @staticmethod
  def from_rpt(roll, pitch, yaw):
    return RotationMatrix.from_angles(roll, pitch, yaw)
  
  @staticmethod
  def from_radians(phi, theta, psi):
    Rx = np.matrix([[       1.0,             0.0,            0.0,           ],
                    [       0.0,        math.cos(phi),   -math.sin(phi),    ],
                    [       0.0,        math.sin(phi),    math.cos(phi),    ]])
    
    Ry = np.matrix([[  math.cos(theta),      0.0,       math.sin(theta),    ],
                    [       0.0,             1.0,            0.0,           ],
                    [ -math.sin(theta),      0.0,       math.cos(theta),    ]])
    
    Rz = np.matrix([[  math.cos(psi),   -math.sin(psi),      0.0,           ],
                    [  math.sin(psi),    math.cos(psi),      0.0,           ],
                    [       0.0,             0.0,            1.0,           ]])
    rotation_matrix = Rz @ Ry @ Rx
    return rotation_matrix
  
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
  
  @staticmethod
  def from_quaternion(Q):
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
    return rot_matrix
  
  def __init__(self, x=0, y=0, z=0):
    self.matrix3x3 = RotationMatrix.from_angles(x,y,z)
    self.matrix4x4 = None
    self.normalized = False
    
  def to_norm_4x4(self):
    """ 
    Before we can use the Rotation Matrix we need to normalize it and convert it to a 4x4 matrix.add()
    I'm using pytransform3d matrix normalization function
    Then I'm creating an identity 4x4 matrix (with 1s in the main diagonal) and replacing the inner 3x3 matrix with the rotation matrix
    Now it's ready to be combined with translation and rotation
    """
    self.normalize()
    self.matrix4x4 = np.identity(4)
    self.matrix4x4[:3, :3] = deepcopy(self.matrix3x3)
    return self.matrix4x4
  
  def normalize(self):
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
    if self.normalized:
      return
    R = np.asarray(self.matrix3x3)
    c2 = R[:, 1]
    c3 = RotationMatrix.normalize_vector(R[:, 2])
    c1 = RotationMatrix.normalize_vector(np.cross(c2, c3))
    c2 = RotationMatrix.normalize_vector(np.cross(c3, c1))
    self.normalized = True
    self.matrix3x3 = np.column_stack((c1, c2, c3))
  
  