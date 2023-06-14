import sys
import vtk
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
from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFrame, QVBoxLayout


class MainWindow(QMainWindow):
  def __init__(self, renderer=None, renderWindow=None, renderWindowInteractor=None):
    super().__init__()
    self.frame = QFrame()
    self.vl = QVBoxLayout()
    self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
    self.vl.addWidget(self.vtkWidget)
    self.renderer = vtkRenderer() if renderer is None else renderer
    self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
    self.rendererInteractor = self.vtkWidget.GetRenderWindow().GetInteractor()
    
    self.add_objects()
    
    self.renderer.ResetCamera()

    self.frame.setLayout(self.vl)
    self.setCentralWidget(self.frame)

    self.show()
    self.rendererInteractor.Initialize()

  def add_objects(self):
    # Create source
    source = vtkSphereSource()
    source.SetCenter(0, 0, 0)
    source.SetRadius(5.0)

    # Create a mapper
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())

    # Create an actor
    actor = vtkActor()
    actor.SetMapper(mapper)

    self.renderer.AddActor(actor)
    
    
def start_qt(renderer=None, renderWindow=None, renderWindowInteractor=None):
  app = QApplication(sys.argv)
  ex = MainWindow(renderer, renderWindow, renderWindowInteractor)
  sys.exit(app.exec_())

if __name__ == "__main__":
  renderer = vtkRenderer()
  start_qt(renderer)