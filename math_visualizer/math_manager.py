import uuid
import numpy as np
from copy import deepcopy
from models.basic.joint import *
from models.basic.model import Model

class MathManager():
  def __init__(self):
    self.uuid = f"Math_{str(uuid.uuid4())}"
  