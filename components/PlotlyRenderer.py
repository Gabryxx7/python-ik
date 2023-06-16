import config.traces as config
from copy import deepcopy
from components.Renderer import ModelType
from utils.utils import Utils

MARKER_SIZE = 15
LEG_OUTLINE_WIDTH = 15
AXIS_LINE_LENGTH = 25
AXIS_LINE_WIDTH = 3

DefaultTraces = {
  ModelType.CUBE: {
    "trace": {
      "uuid": "Model_<UUID>",
      "name": "<NAME>_Model",
      "line": {"color": "#22DAE6", "width": LEG_OUTLINE_WIDTH},
      "marker": {"size": MARKER_SIZE},
      "mode": "lines+markers",
      "showlegend": True,
      "type": "scatter3d",
      "x": [0],
      "y": [0],
      "z": [0]
    }
  },
  ModelType.PLANE: {
    "trace": {
      "uuid": "Plane_<UUID>",
      "name": "<NAME>_Plane",
      "showlegend": True,
      "type": "mesh3d",
      "mode": "lines+markers",
      "opacity": 0.5,
      "color": "#ff6348",
      "x": [],
      "y": [],
      "z": []
    }
  },
  ModelType.JOINT: {
    "trace": {
      "uuid": "Joint_<UUID>",
      "name": "<NAME>_Joint",
      "line": {"color": "#22DAE6", "width": LEG_OUTLINE_WIDTH},
      "marker": {"size": MARKER_SIZE},
      "mode": "lines+markers",
      "showlegend": True,
      "type": "scatter3d",
      "x": [0],
      "y": [0],
      "z": [0]
    }
  },
  ModelType.X_AXIS: {
    "params": {
      "color": "#e64722",
      "direction": [1,0,0],
      "length": AXIS_LINE_LENGTH
    },
    "trace": {
      "uuid": "XAxis_<UUID>",
      "name": "<NAME>_XAxis",
      "line": {"color": "#e64722", "width": AXIS_LINE_WIDTH},
      "showlegend": False,
      "mode": "lines",
      "opacity": 1.0,
      "type": "scatter3d",
      "x": [0, 1],
      "y": [0, 0],
      "z": [0, 0],
    }
  },
  ModelType.Y_AXIS: {
    "params": {
      "color": "#4de622",
      "direction": [0,1,0],
      "length": AXIS_LINE_LENGTH
    },
    "trace": {
      "uuid": "YAxis_<UUID>",
      "name": "<NAME>_YAxis",
      "line": {"color": "#4de622", "width": AXIS_LINE_WIDTH},
      "showlegend": False,
      "mode": "lines",
      "opacity": 1.0,
      "type": "scatter3d",
      "x": [0, 0],
      "y": [0, 1],
      "z": [0, 0],
    }
  },
  ModelType.Z_AXIS: {
    "params": {
      "color": "#2284e6",
      "direction": [0,0,1],
      "length": AXIS_LINE_LENGTH
    },
    "trace": {
      "uuid": "ZAxis_<UUID>",
      "name": "<NAME>_ZAxis",
      "line": {"color": "#2284e6", "width": AXIS_LINE_WIDTH},
      "showlegend": False,
      "mode": "lines",
      "opacity": 1.0,
      "type": "scatter3d",
      "x": [0, 0],
      "y": [0, 0],
      "z": [0, 1],
    }
  }
}

    
class PlotlyRenderer:
  def __init__(self, obj, name="PlotlyRenderer", modelType=ModelType.CUBE):
    self.obj = obj
    self.modelType = ModelType
    self.uuid = f"Trace_{self.obj.uuid}"
    self.traces = {
      "model":  {"type": self.modelType, "params": self.obj.trace_params},
      "x_axis": {"type": ModelType.X_AXIS},
      "y_axis": {"type": ModelType.Y_AXIS},
      "z_axis": {"type": ModelType.Z_AXIS}
    }
  
  def get_joint_length(self):
    if self.obj.parent is not None:
      return (np.linalg.norm(self.obj.parent.transform.position - self.obj.transform.position))
    return -1.0 
  
    # How to get axes lines
    # 1. You obviously need the updated transport of your joint that includes translation and rotation
    # 2. Given that transform, apply it to the origin (absolute pos) and then to an offset origin depending on which axes you're plotting
    # For instance, if you want the UP vector (x axis) you'll need to apply the transform to [0,0,0] and then [0,1,0]
    # Get the normalized difference between the new point and the origin. That will give you the direction from the origin to the new point
    # Since it's normalized you can just multiply it by whatever distance you want to get a greater length
    # Add this vector to the calculated position of the point (absolute pos) et voila you got a line that matches the axis direction no matter what the rotation is
  def update_trace(self, obj_trace, coords):
    trace = obj_trace['trace']
    trace['visible'] = self.obj.visible
    if not self.obj.visible:
      return
    params = obj_trace['params']
    if obj_trace['type'] in (ModelType.X_AXIS, ModelType.Y_AXIS, ModelType.Z_AXIS):
      offset_point =  self.obj.transform.get_direction_vector(params['direction']) * params['length']
      trace['x'] = [coords['x'][0], coords['x'][0] + offset_point[0]]
      trace['y'] = [coords['y'][0], coords['y'][0] + offset_point[1]]
      trace['z'] = [coords['z'][0], coords['z'][0] + offset_point[2]]
      return
    trace['x'] = coords['x']
    trace['y'] = coords['y']
    trace['z'] = coords['z']
    
  def update_trace_params(self, obj_trace):
    params = obj_trace.get('params', None)
    if params is None or len(params) <= 0:
      return obj_trace
    if 'opacity' in params:
      obj_trace['trace']['opacity'] = params['opacity']
    if 'color' in params:
      if 'scatter' in obj_trace['trace']['type']:
        obj_trace['trace']['line']['color'] = params['color'] 
      if 'mesh' in obj_trace['trace']['type']:
          obj_trace['trace']['color'] = params['color'] 
    if 'linewidth' in params and params['linewidth'] > 0:
      if 'line' in obj_trace:
        obj_trace['trace']['line']['width'] = params['linewidth']
    if 'markersize' in params and params['markersize'] > 0:
      if 'marker' in obj_trace:
        obj_trace['trace']['marker']['size'] = params['markersize']
    return obj_trace
  
  def make_trace(self, obj_trace, legendgroup=None):
    default_trace = DefaultTraces.get(obj_trace['type'], None)
    if default_trace is None:
      print(f"ERROR CREATING TRACE No default trace of type {obj_trace['type']}")
      return None
    default_trace = deepcopy(default_trace)
    for key in default_trace.keys():
      if key not in obj_trace:
        obj_trace[key] = default_trace[key]
    obj_trace['trace']['uuid'] = obj_trace['trace']['uuid'].replace("<UUID>", self.obj.uuid)
    obj_trace['trace']['name'] = obj_trace['trace']['name'].replace("<NAME>", self.obj.name)
    if legendgroup is not None:
      obj_trace['trace']["legendgroup"] = self.obj.name
    obj_trace = self.update_trace_params(obj_trace)
    return obj_trace['trace']

  def points_to_coords(self, points):
    x = [float(p[config.AXIS_ORDER_CONVENTION[0]]) for p in points]
    y = [float(p[config.AXIS_ORDER_CONVENTION[1]]) for p in points]
    z = [float(p[config.AXIS_ORDER_CONVENTION[2]]) for p in points]
    return {'x':x, 'y':y, 'z':z}
  
  def find_trace_in_figure(self, obj_trace, fig_data):
    for i in range(0,len(fig_data)):
      if 'uuid' in fig_data[i]:
        if fig_data[i]['uuid'] == obj_trace['trace']['uuid']:
          return fig_data[i]
    return None
      
  def get_traces(self, fig_data):
    remaining = len(self.traces)
    for k in self.traces.keys():
      trace = self.traces[k].get('trace', None)
      if trace is None:
        trace = self.make_trace(self.traces[k])
        # print(f"Making Trace: {k} for {self.obj.name}: {trace is None}")
        if trace is not None:
          fig_data.append(trace)
      else:
        trace = self.find_trace_in_figure(self.traces[k], fig_data)
        # print(f"Finding Trace: {self.traces[k]['uuid']}: {trace is None}")
      if trace is not None:
        self.traces[k]['trace'] = trace
        remaining -= 1
      if remaining <= 0:
        return
  
  def draw(self, fig_data, draw_children=True, dbg_prefix=""):
    self.traces['model']['type'] = self.obj.trace_type
    self.get_traces(fig_data)
    # print(f"Traces found for {self.obj.name}: {[t['name'] for t in traces]}")
    # if not self.obj.visible:
    #   if self.obj.visible == self.obj.prev_visible:
    #     return fig_data
    # print(f"Plotly Trace update: {self.obj.name}")
    
    points = self.obj.get_trace_points()
    coords = self.points_to_coords(points)
    # print(f"{dbg_prefix}Drawing {self.obj.name}")
    for k in self.traces.keys():
      self.update_trace(self.traces[k], coords)
    dbg_prefix += "  "
    if draw_children:
      for child in self.obj.children:
        fig_data = child.draw_plotly(fig_data, draw_children=False, dbg_prefix=dbg_prefix)
    return fig_data
  