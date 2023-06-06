import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
import numpy as np
from frontend.widgets.transform_widget import TransformWidget
from frontend.widgets.quaternion_widget import QuaternionWidget
from frontend.components.widget_interface import Widget
from frontend.components.trigger import Trigger

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
      color = self.joint.trace_params.get('color', "inherit")
      title = dcc.Markdown(f"** JOINT {self.joint.name.upper()} **", style={'color': color})
      self.trigger = Trigger(self.joint.uuid)
      widget_container = html.Div([self.q_widget.get_widget(), self.tf_widget.get_widget(), self.trigger.component], className="joint-widget-container")
      self.widget = html.Div([title, widget_container])
    return self.widget
  
  def update_joint(self, *q_input):
    # print("JOINT UPDATE")
    self.joint.rotate(quaternion=q_input)
    return ""
  
  def add_callback(self):
    self.app.callback(self.trigger.output, self.q_widget.sliders_inputs)(self.update_joint)
    self.app.callback(self.tf_widget.output, self.trigger.input)(self.tf_widget.update_transform_data)