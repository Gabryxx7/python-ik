import vtk
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (vtkRenderWindowInteractor)


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
  
  