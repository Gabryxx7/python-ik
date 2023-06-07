import config.traces as config
from copy import deepcopy

class TracesHelper:
  @staticmethod
  def add_trace(fig_data, trace_type, name, uuid=None, params=None):
    default_trace = None
    trace_type = trace_type.lower()
    for key in config.default_traces.keys():
      if trace_type in key.lower():
        default_trace = config.default_traces[key]
        break
    if default_trace is None:
      print(f"No default trace of type {trace_type}")
      # raise Exception(f"No default trace of type {trace_type}")
    trace = deepcopy(default_trace)
    trace['name'] = name
    trace['uuid'] = str(uuid.uuid4()) if uuid is None else uuid
    if params is not None:
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
    # print(f"Appending trace: {trace['name']} ({trace['uuid']})")
    fig_data.append(trace)
    return fig_data, trace
  
  @staticmethod
  def find_trace(fig_data, uuid):
    for i in range(0,len(fig_data)):
      t = fig_data[i]
      if 'uuid' in t and t['uuid'] == uuid:
        return t
    return None
  
  @staticmethod
  def points_to_trace(points):
    x = [float(p[config.AXIS_ORDER_CONVENTION[0]]) for p in points]
    y = [float(p[config.AXIS_ORDER_CONVENTION[1]]) for p in points]
    z = [float(p[config.AXIS_ORDER_CONVENTION[2]]) for p in points]
    return x, y, z