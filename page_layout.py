from figure_template import HEXAPOD_FIGURE
from dash import dcc
from dash import html
from copy import deepcopy
from style_settings import NUMBER_INPUT_STYLE

UI_GRAPH_HEIGHT = "600px"
UI_GRAPH_WIDTH = "63%"
UI_SIDEBAR_WIDTH = "37%"
DIMENSIONS_WIDGETS_HEADER = "TESTING"

BASE_FIGURE = deepcopy(HEXAPOD_FIGURE)

def get_sidebar(test_section_id, sections=None):
  # params_hidden_section = html.Div(
  #     id=params_hidden_section_id, style={"display": "none"}
  # )
  message_section = html.Div(id=test_section_id)
  HEADER = html.Label(dcc.Markdown(f"**{DIMENSIONS_WIDGETS_HEADER}**"))
  test_section = html.Div([HEADER, html.Div([message_section], style={"display": "flex"}), html.Br()])
  sections = sections+[test_section] if sections is not None else [test_section]
  sidebar = html.Div(sections, style={"width": UI_SIDEBAR_WIDTH})
  return sidebar

def get_graph(graph_id):
  graph = dcc.Graph(
        id=graph_id,
        figure=BASE_FIGURE,
        style={"width": UI_GRAPH_WIDTH, "height": UI_GRAPH_HEIGHT})
  return graph
  
  
def get_page_layout(graph_id, sidebar_id):
  sidebar = get_sidebar(sidebar_id)
  graph = get_graph(graph_id)
  layout = html.Div([sidebar, graph], style={"display": "flex"})
  return layout


def make_number_widget(_name, _value, _min=0, _max=200, _input_resolution=1, _label=None, _type="slider"):
  _label = _name if _label is None else _label
  if _type == "slider":
    input_field = dcc.Slider(_min, _max, _input_resolution, value=_value, id=_name)
  else:
    input_field = dcc.Input(
      id=_name,
      type="number",
      value=_value,
      min=_min,
      max=_max,
      step=_input_resolution,
      style=NUMBER_INPUT_STYLE,
    )
  label = html.Label(dcc.Markdown(f"{_label}"))
  return  html.Div([label, input_field])
