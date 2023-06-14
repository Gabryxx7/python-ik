# Good soiurce of tutorials
# https://examples.vtk.org/site/Python/#tutorial

# VTK QT Example: https://stackoverflow.com/questions/69200800/pyqt5-and-vtk-object-integration

# noinspection PyUnresolvedReferences
import vtk
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkFiltersSources import vtkSphereSource, vtkCubeSource, vtkLineSource
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow

import pandas as pd
import json
import random
from timeit import default_timer as timer
import time
# from .models.arm import Arm
# from .models.basic.joint import Joint
from models_definitions import arm_test, plane_test, circle_test, machine
from vtk_view.components.Model import *
from vtk_view.components.KeyPressInteractor import *
from vtk_qt import start_qt


# if vtk.qt.PyQtImpl == 'PySide6':
#     from PySide6.QtCore import Qt
#     from PySide6.QtWidgets import QApplication, QMainWindow
# elif vtk.qt.PyQtImpl == 'PySide2':
#     from PySide2.QtCore import Qt
#     from PySide2.QtWidgets import QApplication, QMainWindow
# else:
#     from PySide.QtCore import Qt
#     from PySide.QtGui import QApplication, QMainWindow


models = []
models.append(machine)
models.append(arm_test)
offset = 0

class vtkMyCallback(object):
  """
  Callback for the interaction.
  """

  def __init__(self, renderer):
    self.renderer = renderer
    self.last_time = time.time_ns()/1000000000
    self.delta_time = 0

  def __call__(self, caller, ev):
    global offset
    global models
    timeInSeconds = self.renderer.GetLastRenderTimeInSeconds()
    now = time.time_ns()/1000000000
    self.delta_time = now - self.last_time
    self.last_time = now
    fps = 1.0 / self.delta_time
    position = self.renderer.GetActiveCamera().GetPosition()
    print(f"FPS: {fps:.2f}\tElapsed: {self.delta_time}\tOffset: {offset}\t ({position[0]:5.2f}, {position[1]:5.2f}, {position[2]:5.2f})", end="\r")
    update_models(self.delta_time, models, offset)


def main(ui_type="vtk"):
  colors = vtkNamedColors()
  # app = QApplication(['QVTKRenderWindowInteractor'])
  # renderWindow = QMainWindow()
  
  renderWindow = vtkRenderWindow()
  renderWindow.SetWindowName('Axes')
  renderWindow.SetSize(1920,1080)
  
  # a renderer and render window
  renderer = vtkRenderer()
  renderWindow.AddRenderer(renderer)
  br, bg, bb = [34/255, 47/255, 62/255]
  renderer.SetBackground(br, bg, bb)
  
  camera= renderer.GetActiveCamera()
  camera.SetViewUp([0,0,1])
  camera.SetPosition([0.9,0.9,0.25])
  
  add_scene_cube(renderer)
  add_models(models, renderer)

  # renderWindowInteractor = QVTKRenderWindowInteractor(renderWindow)
  # renderWindow.setCentralWidget(renderWindowInteractor)
  
  renderWindowInteractor = vtkRenderWindowInteractor()
  renderWindowInteractor.SetRenderWindow(renderWindow)
  renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()
  kp_interactor = KeyPressInteractorStyle(parent=renderWindowInteractor)
  renderWindowInteractor.SetInteractorStyle(kp_interactor)

  # Here is where we setup the observer.
  mo1 = vtkMyCallback(renderer)
  renderer.AddObserver('StartEvent', mo1)
  
  if ui_type.lower() == "qt":
    start_qt(renderer, renderWindow, renderWindowInteractor)
  else:
    start_vtk(renderer, renderWindow, renderWindowInteractor, kp_interactor)
  
  
def start_vtk(renderer, renderWindow, renderWindowInteractor, kp_interactor=None):
  renderer.ResetCamera()
  renderWindow.Render()
  # show the widget
  # renderWindow.show()
  
  # begin mouse interaction
  renderWindowInteractor.Initialize()
  print("\n\n\n")
  running = True
  while running:
    if kp_interactor is not None:
      running = kp_interactor.status
    if running:
        renderWindowInteractor.ProcessEvents()
        renderWindowInteractor.Render()
    else:
        renderWindowInteractor.TerminateApp()
  # renderWindowInteractor.Start()


if __name__ == '__main__':
  # main("vtk")
  main("qt")