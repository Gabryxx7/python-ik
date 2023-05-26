import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, dash_table, Input, State, Output, callback
import dash_bootstrap_components as dbc
import numpy as np

def get_transform_text(joint):
  tf_text = f"{joint.name}"
  tf_text += f"\n```{np.array2string(joint.transform, precision=3, floatmode='fixed')}"
  tf_text += f"\n\nOrigin: {joint._origin}"
  tf_text += f"\nPosition: {joint.pos}"
  tf_text += f"\nQuaternion: {joint.quaternion}"
  return tf_text

def make_transform_widget(app, joint, color="inherit"):
  # math_string = "$$\\begin{pmatrix}"
  # for i in range(0, len(joint.transform)):
  #   for j in range(0, len(joint.transform[i])):
  #     math_string += f"{joint.transform[i][j]}"
  #     math_string += " & " if j <= len(joint.transform[i])-1 else ""
  #   math_string += "\\\\" if i <= len(joint.transform)-1 else ""
  # math_string += "\\end{pmatrix}$$"
  
  # markdown_widget = dcc.Markdown(math_string, mathjax=True)
  color = "inherit" if joint.color is None else joint.color
  mk_id = f"{joint.uuid}-md-transform-view"
  markdown_widget = dcc.Markdown(get_transform_text(joint), id=mk_id, style={"color": color})
  widget = html.Div([markdown_widget],
    style={"color":color})
  output = Output(mk_id, 'children')
  return widget, output

