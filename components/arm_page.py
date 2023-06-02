import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
from components.joint_widget import JointWidget
from components.trigger import Trigger

class ArmPage:  
  def __init__(self, model, app):
    self.app = app
    self.model = model
    self.page = None
    self.joints_widgets = []
    self.trigger = None
    self.id = f"tab-plane-{self.model.uuid}"
    self.ik_button = {'id': f"ik-run{self.model.uuid}", 'n_clicks': -1}
  
  def get_page(self):
    if self.page is None:
      for joint in self.model.joints:
        self.joints_widgets.append(JointWidget(joint, self.app))
      self.trigger = Trigger(self.model.uuid)
      ik_button = html.Button('Run IK', id=self.ik_button['id'])
      self.page = html.Div([ik_button] + [jw.get_widget() for jw in self.joints_widgets]+[self.trigger.component], className="model-sidebar")
    return self.page
  
  def update_arm(self, **inputs):
    # print(inputs)
    # if(inputs['ik_button'] is None or inputs['ik_button'] > self.ik_button['n_clicks']):
    #   self.ik_button['n_clicks'] += 1
    #   print("IK button pressed")
    # else:
    self.model.forward_kinematics()
    
    return ""
  
  def add_callback(self):
    print("Adding arm callbacks")
    inputs = {'joints': [], 'ik_button': None}
    for jw in self.joints_widgets:
      jw.add_callback()
      inputs['joints'].append(jw.trigger.input)
    outputs = self.trigger.output
    inputs['ik_button'] = Input(self.ik_button['id'], 'n_clicks')
    self.app.callback(outputs, inputs)(self.update_arm)