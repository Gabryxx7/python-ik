import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from copy import deepcopy
from machine.joint import *
from machine.IModel import IModel

class MathExpression:
  def __init__(self):
    self.uuid = f"MathExpr_{str(uuid.uuid4())}"
    self.ops = []
    
  def mul_transform(self, t1, t2):
    pass
    
  