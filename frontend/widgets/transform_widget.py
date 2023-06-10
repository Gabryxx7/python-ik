import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
import numpy as np
from frontend.components.widget_interface import Widget
from utils.quaternion import Quaternion
from utils.transforms import Transform

class TransformWidget:  
  def __init__(self, joint, app):
    self.app = app
    self.joint = joint
    self.widget = None
    self.output = None
  
  def make_widget(self):
    color = self.joint.trace_params.get('color', "inherit")
    tf_title = html.Div(f"{self.joint.name} Transform", className="transform-title", style={"color": color})
    tf_info = self.get_transform_info()
    tf_info_id = f"{self.joint.uuid}-tf-info"
    tf_info_container = html.Div(tf_info, className="transform-infos", id=tf_info_id)
    self.widget = html.Div([tf_title, tf_info_container], className="transform-widget")
    self.output = Output(tf_info_id, "children")
    return self.widget
  
  def get_widget(self):
    if self.widget is None:
      self.widget = self.make_widget()
    return self.widget
  
  def update_transform_data(self, *joint_widget_out_in):
    info = ""
    try:
      info = self.get_transform_info()
    except Exception as e:
      print(f"Exception updating transform info for joint {self.joint.name}: {e}")
    return info
  
  def get_transform_info(self):
    matrix_data = []
    tf = np.array(self.joint.transform.mat)
    for row in tf:
      for col in row:
        matrix_data.append(html.Span(f"{col:.2f}"))
    tf_matrix_div = html.Div(matrix_data, className="transform-matrix-view")
    tf_extras = []
    tf_extras.append(html.Div(f"\n\nOrigin: {np.round(self.joint.origin_pos, 2)}"))
    tf_extras.append(html.Div(f"\nAbs. Pos.: {np.round(self.joint.absolute_pos, 2)}"))
    tf_extras.append(html.Div(f"\nRel. Pos.: {np.round(self.joint.relative_pos, 2)}"))
    try:
      tf_extras.append(html.Div(f"\nDistance from prev: {np.round(self.joint.get_joint_length(), 2)}"))
    except Exception as e:
      pass
    tf_extras.append(html.Div(f"\nQuaternion: {self.joint.quaternion}"))
    # rpy_str = [round(angle,2) for angle in self.joint.quaternion.rpy]
    angles = angles = Transform.rotation_angles(self.joint.transform)
    rpy_str = [round(angle,2) for angle in angles]
    tf_extras.append(html.Div(f"\nRPY: {rpy_str}"))
    
    tf_extras_div = html.Div(tf_extras, className="transform-extras")
    tf_components = [tf_matrix_div, tf_extras_div]
    return tf_components