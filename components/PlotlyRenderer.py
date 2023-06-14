
class PlotlyRenderer(Object3D):
  def __init__(self, name="PlotylRenderer"):
    self.obj = obj
  
  def force_update(self, override_transform):
    self.transform.position = override_transform@self.local_transform.translation
      
  def get_joint_length(self):
    if self.parent is not None:
      return (np.linalg.norm(self.parent.transform.position - self.transform.position))
    return -1.0
  
  def draw_axes(self, fig_data):
  
  
  def draw(self, fig_data, draw_children=True, dbg_prefix=""):
    fig_data, traces = self.get_model_traces(fig_data)
    # print(f"Traces found for {self.name}: {[t['name'] for t in traces]}")
    if not self.visible:
      if self.visible == self.prev_visible:
        return fig_data
    print(f"Plotly Trace update: {self.name}")
    for i in range(0, len(traces)):
      traces[i]['visible'] = self.visible
    # print(f"{dbg_prefix}Drawing {self.name}")
    if self.visible:
      points = self.get_trace_points()
      x, y, z = TracesHelper().points_to_trace(points)
      traces[0]['x'] = x
      traces[0]['y'] = y
      traces[0]['z'] = z
      if len(traces) > 1:
        # How to get axes lines
        # 1. You obviously need the updated transport of your joint that includes translation and rotation
        # 2. Given that transform, apply it to the origin (absolute pos) and then to an offset origin depending on which axes you're plotting
        # For instance, if you want the UP vector (x axis) you'll need to apply the transform to [0,0,0] and then [0,1,0]
        # Get the normalized difference between the new point and the origin. That will give you the direction from the origin to the new point
        # Since it's normalized you can just multiply it by whatever distance you want to get a greater length
        # Add this vector to the calculated position of the point (absolute pos) et voila you got a line that matches the axis direction no matter what the rotation is
        for i in range(0, 3):
          direction = [0,0,0]
          direction[i] = 1
          offset_point =  self.transform.get_direction_vector(direction) * 25
          traces[i+1]['x'] = [x[0], x[0]+offset_point[0]]
          traces[i+1]['y'] = [y[0], y[0]+offset_point[1]]
          traces[i+1]['z'] = [z[0], z[0]+offset_point[2]]
    dbg_prefix += "  "
    if draw_children:
      for child in self.children:
        fig_data = child.draw_plotly(fig_data, draw_children=False, dbg_prefix=dbg_prefix)
    return fig_data
  