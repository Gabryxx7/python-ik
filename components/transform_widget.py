import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc

def make_transform_widget(app, joint, color="inherit"):
  math_string = "$$\\begin{pmatrix}"
  for i in range(0, len(joint.transform)):
    for j in range(0, len(joint.transform[i])):
      math_string += f"{joint.transform[i][j]}"
      math_string += " & " if j <= len(joint.transform[i])-1 else ""
    math_string += "\\\\" if i <= len(joint.transform)-1 else ""
  math_string += "\\end{pmatrix}$$"
  widget = html.Div([dcc.Markdown(math_string, mathjax=True)],
    style={"color":color})
  inpt = Input(f"tf-view-{joint.uuid}", 'value')
  return widget

