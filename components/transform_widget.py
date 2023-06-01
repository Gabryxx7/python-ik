import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
import numpy as np
from components.widget_interface import Widget

class TransformWidget:  
  def __init__(self, joint, app):
    self.app = app
    self.joint = joint
    self.widget = None
    self.output = None
  
  def make_widget(self):
    color = "inherit" if self.joint.color is None else self.joint.color
    mk_id = f"{self.joint.uuid}-md-transform-view"
    markdown_widget = dcc.Markdown(self.get_transform_text(), id=mk_id, style={"color": color})
    self.widget = html.Div([markdown_widget], style={"color":color, 'width': '50%'})
    self.output = Output(mk_id, "children")
    return self.widget
  
  def get_widget(self):
    if self.widget is None:
      self.widget = self.make_widget()
    return self.widget
  
  def update_transform_data(self, *joint_widget_out_in):
    return self.get_transform_text()
  
  def get_transform_text(self):
    tf_text = f"{self.joint.name}"
    tf_text += f"\n```{np.array2string(self.joint.transform, precision=2, floatmode='fixed')}"
    tf_text += f"\n\nOrigin: {np.round(self.joint._origin, 2)}"
    tf_text += f"\nPosition: {np.round(self.joint.absolute_pos, 2)}"
    tf_text += f"\nDistance from prev: {np.round(self.joint.get_joint_length(), 2)}"
    tf_text += f"\nQuaternion: {self.joint.quaternion}"
    return tf_text