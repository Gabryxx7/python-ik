from enum import Enum
# https://stackoverflow.com/questions/24481852/serialising-an-enum-member-to-json

class StrEnum(str, Enum):
  pass

# this creates nice lowercase and JSON serializable names
# https://docs.python.org/3/library/enum.html#using-automatic-values
class AutoNameLower(StrEnum):
  def _generate_next_value_(name, start, count, last_values):
    return name.lower()

class AutoNameLowerStrEnum(AutoNameLower):
  pass

class ModelType(AutoNameLowerStrEnum):
  Y_AXIS = 0
  X_AXIS = 1
  Z_AXIS = 2
  CUBE = 3
  PLANE = 4
  JOINT = 5
  SPHERE = 6
  LINE = 7
