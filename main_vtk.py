from models_definitions import arm_test, plane_test, circle_test, machine
from vtk_view.components.Model import *
from vtk_view.components.KeyPressInteractor import *
from vtk_qt import start_qt

from components.VtkRenderer import VtkRenderer

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow

models = []
models.append(machine)
models.append(arm_test)
offset = 0

def main(ui_type="vtk"):
  renderer_app = VtkRenderer(None)

if __name__ == '__main__':
  # main("vtk")
  main("vtk")