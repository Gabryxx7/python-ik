import uuid
import numpy as np
from copy import deepcopy
from objects.joint import *
from objects.Object3D import Object3D

class MathManager():
  def __init__(self):
    self.uuid = f"Math_{str(uuid.uuid4())}"
  