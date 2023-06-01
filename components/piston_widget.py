import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
from components.trigger import Trigger

DARKMODE = True

NUMBER_INPUT_STYLE = {
    "marginRight": "5%",
    "width": "95%",
    "marginBottom": "5%",
    "borderRadius": "10px",
    "border": "solid 1px",
    "fontFamily": "Courier New",
}

if DARKMODE:
    NUMBER_INPUT_STYLE["backgroundColor"] = "#2c3e50"
    NUMBER_INPUT_STYLE["color"] = "#2ecc71"
    NUMBER_INPUT_STYLE["borderColor"] = "#2980b9"

config = {'value': 0.5, 'min': 0, 'max': 1, 'res': 0.01}

class PistonWidget:
  def __init__(self, piston, app):
    self.app = app
    self.piston = piston
    self.widget = None
    self.slider_input = None
    self.trigger = None
    
  def get_widget(self):
    if self.widget is None:
      self.widget = self.make_widget()
    return self.widget
  
  def make_widget(self):
    name = self.piston.name
    slider_id = f"{self.piston.uuid}_slider"
    input_field = dcc.Slider(config['min'], config['max'], config['res'], value=config['value'], id=slider_id, marks=None, updatemode='drag',
                            persistence=True,
                            tooltip={"placement": "bottom", "always_visible": True})
    label_id = f"{self.piston.uuid}_label"
    label = html.Div(name, id=label_id, **{'data-name': name})
    self.trigger = Trigger(self.piston.uuid)
    self.widget = dbc.Row([dbc.Col([self.trigger.component, label], width=2), dbc.Col([input_field], width=10)], className="piston-widget", style={'width': '100%'})
    self.slider_input = Input(slider_id, "value")
    return self.widget
    
  def update_piston(self, *slider_input):
    print(f"{self.piston.origin.absolute_pos[2]}\t{float(slider_input[0])}")
    self.piston.joints[-2].absolute_pos[2] = float(self.piston.joints[-1].absolute_pos[2]) * float(slider_input[0])
    return ""
    
  def add_callback(self):
    self.app.callback(self.trigger.output, self.slider_input)(self.update_piston)