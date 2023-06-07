import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
from frontend.components.trigger import Trigger
from models.compound_model import PISTON_HEIGHT, PLANE_INITIAL_HEIGHT

config = {'value': 0.5, 'min': 0, 'max': 1, 'res': 0.01}

class PistonWidget:
  def __init__(self, piston, app):
    self.app = app
    self.piston = piston
    self.widget = None
    self.slider_input = None
    self.slider_output = None
    self.trigger = None
    
  def get_widget(self):
    if self.widget is None:
      self.widget = self.make_widget()
    return self.widget
  
  def make_widget(self):
    name = self.piston.name
    slider_id = f"{self.piston.uuid}_piston_slider"
    input_slider = dcc.Slider(config['min'], config['max'], config['res'], value=config['value'], id=slider_id, marks=None, updatemode='drag',
                            persistence=True,
                            tooltip={"placement": "bottom", "always_visible": True})
    label_id = f"{self.piston.uuid}_label"
    label = html.Div(name, id=label_id, **{'data-name': name})
    self.trigger = Trigger(self.piston.uuid)
    self.widget = dbc.Row([dbc.Col([self.trigger.component, label], width=2), dbc.Col([input_slider], width=10)], className="pistons-widget-container")
    self.slider_input = Input(slider_id, "value")
    self.slider_output = Output(slider_id, "value")
    return self.widget
    
  def update_piston(self, *slider_input):
    self.piston.origin_pos[2] = PISTON_HEIGHT * float(slider_input[0])
    return ""
    
  def add_callback(self):
    self.app.callback(self.trigger.output, self.slider_input)(self.update_piston)