import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc

class ModelPage:
  @staticmethod
  def make_page(app, model):
    j_widgets = []
    for joint in model.joints:
      j_w = joint.get_widget(app)
      j_widgets.append(j_w)
    widget = html.Div(j_widgets)
    return widget
  
  def __init__(self, _id, _title, app, model, label="Model"):
    self.label = label
    self.id = _id
    self.title = _title
    self.app = app
    self.layout = None
    self.model = model
  
  def get_page(self):
    if self.layout is None:
      self.layout = ModelPage.make_page(app, model)
    return self.layout
