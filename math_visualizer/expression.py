import uuid
import numpy as np
from copy import deepcopy
from objects.joint import *
from objects.Object3D import Object3D

class MathExpression:
  def __init__(self):
    self.uuid = f"MathExpr_{str(uuid.uuid4())}"
    self.ops = []
    
  def mul_transform(self, t1, t2):
    pass
    
  