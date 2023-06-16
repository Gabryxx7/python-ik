from models_definitions import arm_test, plane_test, circle_test, machine
from components.VtkRenderer import VtkRenderer


models = []
# models.append(machine)
models.append(arm_test)
offset = 0

def start_viewer(ui_type="vtk", p_models=None):
  global models
  models = models if p_models is None else p_models
  renderer_app = VtkRenderer()
  for model in models:
    renderer_app.add_model(model)
  renderer_app.start()

if __name__ == '__main__':
  # main("qt")
  start_viewer("vtk")