
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


class KeyPressInteractorStyle(vtkInteractorStyleTrackballCamera):
  def __init__(self, parent=None, status=True):
    self.parent = vtkRenderWindowInteractor()
    self.status = status
    if parent is not None:
      self.parent = parent
    self.AddObserver('KeyPressEvent', self.key_press_event)

  def key_press_event(self, obj, event):
    key = self.parent.GetKeySym().lower()
    update()
    if key == 'e' or key == 'q':
        self.status = False
    return
  
  