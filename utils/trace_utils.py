import config.traces as config
from copy import deepcopy

class TracesHelper:
  @staticmethod
  def add_model_traces(fig_data, trace_type, name, uuid=None, params=None):
    default_trace = None
    trace_type = trace_type.lower()
    for key in config.default_traces.keys():
      if trace_type in key.lower():
        default_trace = config.default_traces[key]
        break
    if default_trace is None:
      print(f"No default trace of type {trace_type}")
      # raise Exception(f"No default trace of type {trace_type}")
    trace_uuid = str(uuid.uuid4()) if uuid is None else uuid
    trace = deepcopy(default_trace)
    trace['name'] = name
    trace['uuid'] = f"model_{trace_uuid}"
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
    x_ax_trace = deepcopy(config.default_traces['x_axis'])
    x_ax_trace['uuid'] = f"x_axis_{trace_uuid}"
    y_ax_trace = deepcopy(config.default_traces['y_axis'])
    y_ax_trace['uuid'] = f"y_axis_{trace_uuid}"
    z_ax_trace = deepcopy(config.default_traces['z_axis'])
    z_ax_trace['uuid'] = f"z_axis_{trace_uuid}"
    
    trace["legendgroup"] = name
    x_ax_trace["legendgroup"] = name
    y_ax_trace["legendgroup"] = name
    z_ax_trace["legendgroup"] = name
    fig_data.append(trace)
    fig_data.append(x_ax_trace)
    fig_data.append(y_ax_trace)
    fig_data.append(z_ax_trace)
    traces = [trace, x_ax_trace, y_ax_trace, z_ax_trace]
    return fig_data, traces
  
  @staticmethod
  def find_model_traces(fig_data, uuid):
    to_find = [f"model_{uuid}", f"x_axis_{uuid}", f"y_axis_{uuid}", f"z_axis_{uuid}"]
    found = []
    for i in range(0,len(fig_data)):
      t = fig_data[i]
      if 'uuid' in t and t['uuid'] in to_find:
        found.append(t)
      if len(found) >= len(to_find):
        return found
    return found
  
  @staticmethod
  def points_to_trace(points):
    x = [float(p[config.AXIS_ORDER_CONVENTION[0]]) for p in points]
    y = [float(p[config.AXIS_ORDER_CONVENTION[1]]) for p in points]
    z = [float(p[config.AXIS_ORDER_CONVENTION[2]]) for p in points]
    return x, y, z