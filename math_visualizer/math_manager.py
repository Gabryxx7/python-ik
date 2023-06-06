import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from copy import deepcopy
from models.basic.joint import *
from models.basic.model import Model

class MathManager():
  def __init__(self):
    self.uuid = f"Math_{str(uuid.uuid4())}"
  