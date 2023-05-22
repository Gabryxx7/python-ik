from figure_template import HEXAPOD_FIGURE
from dash import dcc
from dash import html
from copy import deepcopy

UI_GRAPH_HEIGHT = "600px"
UI_GRAPH_WIDTH = "63%"
UI_SIDEBAR_WIDTH = "37%"
DIMENSIONS_WIDGETS_HEADER = "TESTING"

BASE_FIGURE = deepcopy(HEXAPOD_FIGURE)

def get_sidebar(test_section_id):
  # params_hidden_section = html.Div(
  #     id=params_hidden_section_id, style={"display": "none"}
  # )
  message_section = html.Div(id=test_section_id)
  HEADER = html.Label(dcc.Markdown(f"**{DIMENSIONS_WIDGETS_HEADER}**"))
  test_section = html.Div([HEADER, html.Div([message_section], style={"display": "flex"}), html.Br()])
  sections = [test_section]
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