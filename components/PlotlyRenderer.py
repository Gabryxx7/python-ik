import config.traces as config
from copy import deepcopy
from enum import Enum

class TraceType(Enum):
  MODEL = 0
  PLANE = 1
  JOINT = 2
  AXIS = 3

MARKER_SIZE = 15
LEG_OUTLINE_WIDTH = 15
AXIS_LINE_LENGTH = 25

DefaultTraces = {
  TraceType.MODEL: {
    "name": "Model",
    "line": {"color": "#22DAE6", "width": LEG_OUTLINE_WIDTH},
    "marker": {"size": MARKER_SIZE},
    "mode": "lines+markers",
    "showlegend": True,
    "type": "scatter3d",
    "x": [0],
    "y": [0],
    "z": [0]
  },
  TraceType.PLANE: {
    "name": "Plane",
    "showlegend": True,
    "type": "mesh3d",
    "mode": "lines+markers",
    "opacity": 0.5,
    "color": "#ff6348",
    "x": [],
    "y": [],
    "z": []
  },
  TraceType.JOINT: {
    "name": "Joint",
    "line": {"color": "#22DAE6", "width": LEG_OUTLINE_WIDTH},
    "marker": {"size": MARKER_SIZE},
    "mode": "lines+markers",
    "showlegend": True,
    "type": "scatter3d",
    "x": [0],
    "y": [0],
    "z": [0]
  },
  TraceType.AXIS: {
    "name": "Axis",
    "line": {"color": "#FFFFFF", "width": 3},
    "showlegend": False,
    "mode": "lines",
    "opacity": 1.0,
    "type": "scatter3d",
    "x": [0, 1],
    "y": [0, 0],
    "z": [0, 0],
  }
}

class TracesHelper:
  # def __init__(self, obj, name="PlotlyRenderer"):
  #   self.obj = obj
  @staticmethod
  def update_trace_params(trace, params=None):
    if params is None:
      return
    if 'opacity' in params:
      trace['opacity'] = params['opacity']
    if 'color' in params:
      if 'scatter' in trace['type']:
        trace['line']['color'] = params['color'] 
      if 'mesh' in trace['type']:
          trace['color'] = params['color'] 
    if 'linewidth' in params and params['linewidth'] > 0:
      if 'line' in trace:
        trace['line']['width'] = params['linewidth']
    if 'markersize' in params and params['markersize'] > 0:
      if 'marker' in trace:
        trace['marker']['size'] = params['markersize']
    return trace
  
  def make_trace(trace_data, legendgroup=None):
    default_trace = DefaultTraces.get(trace_data['type'], None)
    if default_trace is None:
      print(f"ERROR CREATING TRACE No default trace of type {trace_data['type']}")
      return None
    trace = deepcopy(default_trace)
    trace['uuid'] = trace_data['uuid']
    if 'name' in trace_data:
      trace['name'] = trace_data['name']
    if legendgroup is not None:
      trace["legendgroup"] = name
    trace = TracesHelper.update_trace_params(trace, trace_data.get('params', None))
    return trace

  @staticmethod
  def points_to_coords(points):
    x = [float(p[config.AXIS_ORDER_CONVENTION[0]]) for p in points]
    y = [float(p[config.AXIS_ORDER_CONVENTION[1]]) for p in points]
    z = [float(p[config.AXIS_ORDER_CONVENTION[2]]) for p in points]
    return {'x':x, 'y':y, 'z':z}

    
class PlotlyRenderer:
  def __init__(self, obj, name="PlotlyRenderer", traceType=TraceType.MODEL):
    self.obj = obj
    self.traceType = traceType
    self.uuid = f"Trace_{self.obj.uuid}"
    self.traces = {
      "model":  {"uuid": f"Model_{self.uuid}", "name": "Model", "trace": None, "type": traceType, "params": self.obj.trace_params},
      "x_axis": {"uuid": f"Xax_{self.uuid}",  "name": "X Axis",  "trace": None, "type": TraceType.AXIS, "params": {"color": "#e64722"}, "direction": [1,0,0]},
      "y_axis": {"uuid": f"Yax_{self.uuid}",  "name": "Y Axis",  "trace": None, "type": TraceType.AXIS, "params": {"color": "#4de622"}, "direction": [0,1,0]},
      "z_axis": {"uuid": f"Zax_{self.uuid}",  "name": "Z Axis",  "trace": None, "type": TraceType.AXIS, "params": {"color": "#2284e6"}, "direction": [0,0,1]}
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
  def update_trace(self, trace_data, coords):
    trace = trace_data['trace']
    trace['visible'] = self.obj.visible
    if not self.obj.visible:
      return
    if trace_data['type'] == TraceType.AXIS:
      direction = trace_data['direction']
      offset_point =  self.obj.transform.get_direction_vector(direction) * AXIS_LINE_LENGTH
      trace['x'] = [coords['x'][0], coords['x'][0] + offset_point[0]]
      trace['y'] = [coords['y'][0], coords['y'][0] + offset_point[1]]
      trace['z'] = [coords['z'][0], coords['z'][0] + offset_point[2]]
    else:
      trace['x'] = coords['x']
      trace['y'] = coords['y']
      trace['z'] = coords['z']
    return trace
    
  def find_trace_in_figure(self, trace_data, fig_data):
    for i in range(0,len(fig_data)):
      if 'uuid' in fig_data[i]:
        if fig_data[i]['uuid'] == trace_data['uuid']:
          return fig_data[i]
    return None
      
  def get_traces(self, fig_data):
    remaining = len(self.traces)
    for k in self.traces.keys():
      trace = None
      if self.traces[k]['trace'] is None:
        trace = TracesHelper.make_trace(self.traces[k])
        # print(f"Making Trace: {self.traces[k]['uuid']}: {trace is None}")
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
    coords = TracesHelper.points_to_coords(points)
    # print(f"{dbg_prefix}Drawing {self.obj.name}")
    for k in self.traces.keys():
      self.update_trace(self.traces[k], coords)
    dbg_prefix += "  "
    if draw_children:
      for child in self.obj.children:
        fig_data = child.draw_plotly(fig_data, draw_children=False, dbg_prefix=dbg_prefix)
    return fig_data
  