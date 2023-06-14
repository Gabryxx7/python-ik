import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
import numpy as np
from frontend.components.widget_interface import Widget
from utils.quaternion import Quaternion
from components.Transform import Transform

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
    # self.widget = html.Div([tf_title, tf_info_container], className="transform-widget")
    self.widget = html.Div([tf_info_container], className="transform-widget")
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
    tf_extras.append(html.Div([html.Div(f"Abs. Pos.: "), html.Div(f"{np.round(self.joint.transform.position, 2)}")], className='tf-widget-row'))
    tf_extras.append(html.Div([html.Div(f"Rel. Pos.: "), html.Div(f"{np.round(self.joint.local_transform.position, 2)}")], className='tf-widget-row'))
    
    tf_extras.append(html.Div([html.Div(f"Abs Quaternion: "), html.Div(f"{self.joint.transform.quaternion}")], className='tf-widget-row'))
    
    calc_abs_quat = Quaternion.from_rotation_matrix(self.joint.transform)
    tf_extras.append(html.Div([html.Div(f"Quat from Abs Transf: "), html.Div(f"{calc_abs_quat}")], className='tf-widget-row'))
    
    tf_extras.append(html.Div([html.Div(f"Rel Quaternion: "), html.Div(f"{self.joint.local_transform.quaternion}")], className='tf-widget-row'))
    
    calc_rel_quat = Quaternion.from_rotation_matrix(self.joint.local_transform)
    tf_extras.append(html.Div([html.Div(f"Quat from Local Transf: "), html.Div(f"{calc_rel_quat}")], className='tf-widget-row'))
    
    angles_str = [round(angle,2) for angle in self.joint.transform.rotation]
    tf_extras.append(html.Div([html.Div(f"Abs. Rotation: "), html.Div(f"{angles_str}")], className='tf-widget-row'))
    
    angles_str = [round(angle,2) for angle in self.joint.transform.get_euler_angles(order="zyx")]
    tf_extras.append(html.Div([html.Div(f"Rotation from Abs Transf: "), html.Div(f"{angles_str}")], className='tf-widget-row'))
    
    angles_str = [round(angle,2) for angle in self.joint.local_transform.rotation]
    tf_extras.append(html.Div([html.Div(f"Rel. Rotation: "), html.Div(f"{angles_str}")], className='tf-widget-row'))
    
    angles_str = [round(angle,2) for angle in self.joint.local_transform.get_euler_angles(order="zyx")]
    tf_extras.append(html.Div([html.Div(f"Rotation from Local Transf: "), html.Div(f"{angles_str}")], className='tf-widget-row'))
    
    try:
      tf_extras.append(html.Div([html.Div(f"Distance from prev: "), html.Div(f"{np.round(self.joint.get_joint_length(), 2)}")], className='tf-widget-row'))
    except Exception as e:
      pass
    
    tf_extras_div = html.Div(tf_extras, className="transform-extras")
    tf_components = [tf_matrix_div, tf_extras_div]
    return tf_components