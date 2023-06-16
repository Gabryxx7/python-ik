import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc

# Because Dash does not allow multiple callbacks with the same output and I did not want a huge, messy callback function that receives ALL inputs to update just the figure
# I set this trigger that is just an empty html element that when updated triggers the callbacks
# You can assign the trigger input to whatever you want to happen AFTER something else.
# When a callback has the trigger output as its OUTPUT you just need to return anything, even an empty string works. That will trigger any callback associated with the trigger input
class Trigger:
  def __init__(self, _id):
    self._id = _id +"_cb_out"
    self.component = html.Div("", id=self._id, style={'display': 'none'})
    self.output = Output(self._id, 'children')
    self.input = Input(self._id, 'children')