
MARKER_SIZE = 15
LEG_OUTLINE_WIDTH = 15
AXIS_LINE_LENGTH = 25

DefaultVTKModels= {
  ModelType.MODEL: {
    "vtkClass": "vtkLineSource",
    "uuid": "Model_<UUID>",
    "name": "<NAME>_Model",
    'property': {
      'opacity': opacity,
      'color': color,
      'pointSize': 10,
    },
    'state': {
      "lineWidth": 10,
      'point1': p1,
      'point2': p2,
      'resolution': 600
    }
  },
  ModelType.PLANE: {
    "vtkClass": "vtkLineSource",
    "uuid": "Model_<UUID>",
    "name": "<NAME>_Model",
    'property': {
      'opacity': opacity,
      'color': color,
      'pointSize': 10,
    },
    'actor': {},
    'state': {
      "lineWidth": 10,
      'point1': p1,
      'point2': p2,
      'resolution': 600
    }
  },
  ModelType.SPHERE: {
    "vtkClass": "vtkSphereSource",
    "uuid": "Model_<UUID>",
    "name": "<NAME>_Model",
    'property': {
      'opacity': 1.0,
      'color': [1,0,0]
    },
    'actor': {
      'origin': [0,0,0],
      'position': [0,0,0],
      'orientation': [0,0,0],
    },
    'state': {
      "lineWidth": 10,
      "center": [0,0,0],
      "radius": 10,
      'resolution': 600
    }
  },
  ModelType.JOINT: {
    "vtkClass": "vtkCubeSource",
    "uuid": "Model_<UUID>",
    "name": "<NAME>_Model",
    'property': {
      'opacity': 1.0,
      'color': [1,0,0]
    },
    'actor': {
      'origin': [0,0,0],
      'position': [0,0,0],
      'orientation': [0,0,0],
    },
    'state': {
      'center': [0,0,10],
      'zLength': 10,
      'xLength': 2,
      'yLength': 2,
      'resolution': 60
    }
  },
  ModelType.X_AXIS: {
    "vtkClass": "vtkLineSource",
    "uuid": "XAxis_<UUID>",
    "name": "<NAME>_XAxis",
    "direction": [1,0,0],
    "length": AXIS_LINE_LENGTH,
    'property': {
      'opacity': 1.0,
      'color': "#e64722",
      'pointSize': 10,
    },
    'actor': {},
    'state': {
      "lineWidth": 10,
      'point1': [0,0,0],
      'point2': [0,0,0],
      'resolution': 600
    }
  },
  ModelType.Y_AXIS: {
    "vtkClass": "vtkLineSource",
    "uuid": "YAxis_<UUID>",
    "name": "<NAME>_YAxis",
    "direction": [0,1,0],
    "length": AXIS_LINE_LENGTH,
    'property': {
      'opacity': 1.0,
      'color': "#4de622",
      'pointSize': 10,
    },
    'actor': {},
    'state': {
      "lineWidth": 10,
      'point1': [0,0,0],
      'point2': [0,0,0],
      'resolution': 600
    }
  },
  ModelType.Z_AXIS: {
    "vtkClass": "vtkLineSource",
    "uuid": "ZAxis_<UUID>",
    "name": "<NAME>_ZAxis",
    "direction": [0,0,1],
    "length": AXIS_LINE_LENGTH,
    'property': {
      'opacity': 1.0,
      'color': "#2284e6",
      'pointSize': 10,
    },
    'actor': {},
    'state': {
      "lineWidth": 10,
      'point1': [0,0,0],
      'point2': [0,0,0],
      'resolution': 600
    }
  }
}
