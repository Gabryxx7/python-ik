
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

def update_models(delta_time, models, offset):
  speed = 100
  for model in models:
    model.rotate([offset*speed, offset*speed*0.5, offset*speed*0.2])
    model.update()
    model.vtk_update()
  offset += delta_time
  if offset >= 360:
    offset = 0
  
def add_models(models, renderer):
  for model in models:
    model.update()
    vtk_model_data = model.get_vtk_model_data()
    assigned = False
    for vtk_model in vtk_model_data:
      source, actor = make_joint(vtk_model)
      print(f"Adding {vtk_model['id']}")
      renderer.AddActor(actor)
      if not assigned:
        if 'cube' in vtk_model['id'].lower():
          model.vtk_source = source
          model.vtk_actor = actor
          assigned = True

def make_joint(obj):
  state = obj.get('state', {})
  actor_prop = obj.get('actor', {})
  properties = obj.get('property', {})
  
  if obj['vtkClass'] == 'vtkSphereSource':
      source = vtkSphereSource()
      source.SetCenter(state.get('center', [0,0,0]))
      source.SetRadius(state.get('radius', 50))
  elif obj['vtkClass'] == 'vtkCubeSource':
      source = vtkCubeSource()
      source.SetXLength(state['xLength'])
      source.SetZLength(state['zLength'])
      source.SetYLength(state['yLength'])
      source.SetCenter(state.get('center', [0,0,0]))
  elif obj['vtkClass'] == 'vtkLineSource':
      source = vtkLineSource()
      source.SetPoint1(state.get('p1', [0,0,0]))
      source.SetPoint2(state.get('p2', [50,50,50]))
      
  properties["edgeVisibility"] = True
  properties["lineWidth"] = 2
  
  # create an actor
  actor = vtkActor()
  actor.SetOrigin(actor_prop.get('origin', [0,0,0]))
  actor.SetPosition(actor_prop.get('position', [0,0,0]))
  actor.SetOrientation(actor_prop.get('orientation', [0,0,0]))
  if properties["edgeVisibility"]:
      actor.GetProperty().EdgeVisibilityOn()
  actor.GetProperty().SetLineWidth(properties["lineWidth"])
  
  # actor.GetProperty().SetColor(colors.GetColor("Gray", r,g,b, 1))
  # vtk_color = colors.GetColorRGB(f"{obj['id']}_Color", properties.get('color', [0.0,0.0,1.0]))
  r, g, b = properties.get('color', [1.0,0.0,0.0])
  actor.GetProperty().SetColor(r, g, b)
  # opacity = 1 if properties['opacity'] else 0
  actor.GetProperty().SetOpacity(1)
  # create a mapper
  mapper = vtkPolyDataMapper()
  mapper.SetInputConnection(source.GetOutputPort())

  actor.SetMapper(mapper)
  return source, actor
  # return {'actor':}

def add_scene_cube(renderer):
  bounds = 500
  sceneCube = vtkCubeSource()
  sceneCube.SetCenter(0.0, 0.0, bounds/2)
  sceneCube.SetXLength(bounds)
  sceneCube.SetYLength(bounds)
  sceneCube.SetZLength(bounds)

  # create a mapper
  sceneCubeMapper = vtkPolyDataMapper()
  sceneCubeMapper.SetInputConnection(sceneCube.GetOutputPort())

  # create an actor
  sceneCubeActor = vtkActor()
  sceneCubeActor.SetOrigin(0,0,0)
  sceneCubeActor.SetMapper(sceneCubeMapper)
  sceneCubeActor.SetVisibility(0)
  renderer.AddActor(sceneCubeActor)
  
  #  The axes are positioned with a user transform
  # axes.SetUserTransform(transform)
  # https://vtk.org/Wiki/VTK/Examples/Python/Visualization/CubeAxesActor
  cubeAxesActor = vtkCubeAxesActor()
  cubeAxesActor.SetMapper(sceneCubeMapper)
  cubeAxesActor.SetBounds(sceneCubeMapper.GetBounds())
  cubeAxesActor.SetCamera(renderer.GetActiveCamera())
  cubeAxesActor.SetXTitle("AP (um)")
  cubeAxesActor.SetYTitle("DV (um)")
  cubeAxesActor.SetZTitle("ML (um)")
  cubeAxesActor.GetTitleTextProperty(0).SetColor(1.0, 0.0, 0.0)
  cubeAxesActor.GetLabelTextProperty(0).SetColor(1.0, 0.0, 0.0)
  cubeAxesActor.GetTitleTextProperty(1).SetColor(0.0, 1.0, 0.0)
  cubeAxesActor.GetLabelTextProperty(1).SetColor(0.0, 1.0, 0.0)
  cubeAxesActor.GetTitleTextProperty(2).SetColor(0.0, 0.0, 1.0)
  cubeAxesActor.GetLabelTextProperty(2).SetColor(0.0, 0.0, 1.0)
  cubeAxesActor.DrawXGridlinesOn()
  cubeAxesActor.DrawYGridlinesOn()
  cubeAxesActor.DrawZGridlinesOn()
  cubeAxesActor.SetGridLineLocation(cubeAxesActor.VTK_GRID_LINES_FURTHEST)
  
  renderer.AddActor(cubeAxesActor)