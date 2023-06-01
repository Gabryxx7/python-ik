import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
import numpy as np
from components.transform_widget import TransformWidget
from components.quaternion_widget import QuaternionWidget
from components.widget_interface import Widget
from components.trigger import Trigger

JOINT_WIDGET_STYLE = {'display': 'flex', 'flex-direction': 'row'}

class JointWidget:
  def __init__(self, joint, app):
    self.joint = joint
    self.app = app
    self.tf_widget = None
    self.q_widget = None
    self.widget = None
    self.trigger = None
    
  def get_widget(self):
    if self.widget is None:
      self.q_widget = QuaternionWidget(self.joint, self.app)
      self.tf_widget = TransformWidget(self.joint, self.app)
      self.trigger = Trigger(self.joint.uuid)
      self.widget = html.Div([self.q_widget.get_widget(), self.tf_widget.get_widget(), self.trigger.component], className="joint-widget", style=JOINT_WIDGET_STYLE)
    return self.widget
  
  def update_joint(self, *q_input):
    print("JOINT UPDATE")
    self.joint.rotate(quaternion=q_input)
    return ""
  
  def add_callback(self):
    self.app.callback(self.trigger.output, self.q_widget.sliders_inputs)(self.update_joint)
    self.app.callback(self.tf_widget.output, self.trigger.input)(self.tf_widget.update_transform_data)