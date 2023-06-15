from models_definitions import arm_test, plane_test, circle_test, machine
from components.VtkRenderer import VtkRenderer


models = []
# models.append(machine)
# models.append(arm_test)
offset = 0

def main(ui_type="vtk"):
  renderer_app = VtkRenderer()
  renderer_app.start()

if __name__ == '__main__':
  # main("qt")
  main("vtk")