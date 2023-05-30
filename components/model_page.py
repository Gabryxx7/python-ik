

class ModelPage:
  def __init__(self, _id, _title, model):
    self.id = _id
    self.title = _title
    self.model = _model
    
  def make_model_page(self, _id, model):
    plot3d = dcc.Graph(id=GRAPH_ID, figure=BASE_FIGURE,style={'width': '100%'})
    pass
    