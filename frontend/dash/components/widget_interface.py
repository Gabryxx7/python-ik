from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import uuid

class Widget:
  def __init__(self, _widget=None):
    self.uuid = f"Widget_{str(uuid.uuid4())}"
    self.widget = _widget
    self.inputs = []
    self.outputs = []
    self.states = []
    self.children = []
    
  def inputs():
    inputs = [x for x in self.inputs]
    for child in self.children:
      for inpt in child.inputs:
        inputs.append(inpt)
    return inputs
    
  def states():
    states = [x for x in self.states]
    for child in self.children:
      for state in child.states:
        states.append(state)
    return states
    
  def add_output(type='value'):
    self.outputs.append(Output())
    
  def outputs():
    outputs = [x for x in self.outputs]
    for child in self.children:
      for output in child.outputs:
        outputs.append(output)
    return outputs
  
  def get_widget():
    return self.widget
    
