""" Main VTK Renderer
  - Official tutorials: https://examples.vtk.org/site/Python/#tutorial
  - VTK QT Example: https://stackoverflow.com/questions/69200800/pyqt5-and-vtk-object-integration
"""
from copy import deepcopy
import time
import numpy as np
import math
import vtk
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkSphereSource, vtkCubeSource, vtkLineSource
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor
from vtkmodules.vtkRenderingCore import ( vtkActor, vtkPolyDataMapper, vtkRenderWindow, vtkRenderWindowInteractor, vtkRenderer )

from components.Renderer import ModelType
from components.vtk.DefaultVTKModels import *
from components.vtk.Observers.Timer import Timer
from components.vtk.Observers.ModelsUpdater import ModelsUpdater

from components.vtk.Interactors.KeyPressInteractor import KeyPressInteractorStyle

from utils.utils import Utils

v_dist = lambda p, orig=[0,0,0]: (np.linalg.norm(np.array(orig) - np.array(p)))

def hex_to_rgb(h):
  h = h.lstrip('#')
  return list(float(int(h[i:i+2], 16)/255) for i in (0, 2, 4))

class VtkModel:
  def __init__(self, obj, name="VtkModel", modelType=ModelType.SPHERE):
    self.obj = obj
    self.modelType = modelType
    self.renderer = None
    self.uuid = f"VtkModel_{self.obj.uuid}"
    self.models = {
      "joint":  {"type": ModelType.SPHERE},
      "line":   {"type": ModelType.LINE},
      "cube":   {"type": ModelType.CUBE},
      "x_axis": {"type": ModelType.X_AXIS},
      "y_axis": {"type": ModelType.Y_AXIS},
      "z_axis": {"type": ModelType.Z_AXIS}
    }
    self.make_vtk_models()
    self.initialized = False
    self.source = None
    self.actor = None
    self.mapper = None
  
  def add_models_to_scene(self, renderer, draw_children=True):
    self.renderer = renderer
    for k in self.models.keys():
      name = self.models[k].get('name', f"NO NAME - {k} ({self.obj.name})")
      instance = self.models[k].get('instance', None)
      if instance is None:
        print(f"{name} has no Instance, creating one")
        self.models[k] = self.make_instance(self.models[k])
        instance = self.models[k].get('instance', None)
      actor = None
      if instance is not None:
        actor = instance.get('actor', None)
      if actor is None:
        print(f"ERROR: {name} has no Actor")
        continue
      print(f"Adding {name} Actor")
      self.renderer.AddActor(actor)
    if draw_children:
      for child in self.obj.children:
        child.vtk_renderer.add_models_to_scene(renderer, draw_children=False)
  
  def copy_default_model(self, model_data, color=None, opacity=None):
    model_type = model_data['type']
    model_data = deepcopy(DefaultVTKModels[model_type])
    model_data['type'] = model_type
    model_data['uuid'] = model_data['uuid'].replace("<UUID>", self.obj.uuid) 
    model_data['name'] = model_data['name'].replace("<NAME>", self.obj.name)
    if color is not None:
      model_data['property']['color'] = color
    if opacity is not None:
      model_data['property']['opacity'] = opacity
    return model_data
  
  def update_models(self, draw_children=True):
    thickness = 8
    radius = 10
    points = self.obj.get_trace_points()
    orientation = self.obj.transform.get_euler_angles(order="zxy")
    p1 = [0,0,0]
    p2 = [0,0,0]
    if points is not None and len(points) > 0:
      p1 = list(points[0][0:3])
    
    self.models['joint']['actor']['origin'] = p1
    self.models['joint']['actor']['orientation'] = orientation
    self.models['joint']['state']['center'] = p1
    self.models['joint']['state']['radius'] = radius
    # self.models['joint'] = self.make_instance(self.models['joint'])
    
    if len(points) > 1:
      p1 = list(points[0][0:3])
      p2 = list(points[1][0:3])
      length = v_dist(p1, p2)
      self.models['cube']['actor']['origin'] = p1
      self.models['cube']['actor']['orientation'] = orientation
      self.models['cube']['state']['center'] = [p1[0], p1[1], p1[2]+length*0.5]
      self.models['cube']['state']['zLength'] = length
      self.models['cube']['state']['xLength'] = thickness
      self.models['cube']['state']['yLength'] = thickness
      # self.models['cube'] = self.make_instance(self.models['cube'])
    
      self.models['line']['state']['point1'] = p1
      self.models['line']['state']['point2'] = p2
      # self.models['line'] = self.make_instance(self.models['line'])
    
    self.models['x_axis']['state']['point1'] = p1
    p2 = self.obj.transform.get_direction_vector(self.models['x_axis']['direction']) * self.models['x_axis']['length']
    p2 = list(p2[0:3])
    self.models['x_axis']['state']['point2'] = p2
    
    self.models['y_axis']['state']['point1'] = p1
    p2 = self.obj.transform.get_direction_vector(self.models['y_axis']['direction']) * self.models['y_axis']['length']
    p2 = list(p2[0:3])
    self.models['y_axis']['state']['point2'] = p2
    
    self.models['z_axis']['state']['point1'] = p1
    p2 = self.obj.transform.get_direction_vector(self.models['z_axis']['direction']) * self.models['z_axis']['length']
    p2 = list(p2[0:3])
    self.models['z_axis']['state']['point2'] = p2
    
    for k in self.models.keys():
      self.update_instance(self.models[k])
    
  def update_instance(self, obj):
    vtk_class = obj.get('vtkClass', None)
    instance = obj.get('instance', None)
    if instance is None:
      return
    source = instance.get('source', None)
    if source is not None:
      state = obj.get('state', {})
      center = state.get('center', [0,0,0])
      p1 = state.get('point1', [0,0,0])
      p2 = state.get('point2', [50,50,50])
      print(f"Updating instance {obj['name']}: P: {center}\tP1: {p1}\tP2{p2}")
      if vtk_class == 'vtkSphereSource':
          source.SetCenter(center)
          source.SetRadius(state.get('radius', 50))
      elif vtk_class == 'vtkCubeSource':
          source.SetXLength(state['xLength'])
          source.SetZLength(state['zLength'])
          source.SetYLength(state['yLength'])
          source.SetCenter(center)
      elif vtk_class == 'vtkLineSource':
          source.SetPoint1(p1)
          source.SetPoint2(p2)
    
    actor = instance.get('actor', None)
    if actor is not None:
      actor_prop = obj.get('actor', {})
      actor.SetOrigin(actor_prop.get('origin', [0,0,0]))
      actor.SetPosition(actor_prop.get('position', [0,0,0]))
      actor.SetOrientation(actor_prop.get('orientation', [0,0,0]))
    
    
  def make_vtk_models(self, draw_children=True, dbg_prefix=""):
    color = hex_to_rgb(self.obj.trace_params.get('color', "#FFFFFF"))
    opacity = 1 if self.obj.visible else 0
    self.models['joint'] = self.copy_default_model(self.models['joint'], color, opacity)
    self.models['x_axis'] = self.copy_default_model(self.models['x_axis'], color, opacity)
    self.models['y_axis'] = self.copy_default_model(self.models['y_axis'], color, opacity)
    self.models['z_axis'] = self.copy_default_model(self.models['z_axis'], color, opacity)
    self.models['cube'] = self.copy_default_model(self.models['cube'], color, opacity)
    self.models['line'] = self.copy_default_model(self.models['line'], color, opacity)
  
    for k in self.models.keys():
      self.models[k] = self.make_instance(self.models[k])
  
  def make_instance(self, obj):
    state = obj.get('state', {})
    actor_prop = obj.get('actor', {})
    properties = obj.get('property', {})
    vtk_class = obj.get('vtkClass', None)
    if vtk_class is None:
      print(f"Error: no class for {obj.get('type', 'NO TYPE')} of ({self.obj.name}). Keys: {obj.keys()}")
      return obj
    if vtk_class == 'vtkSphereSource':
        source = vtkSphereSource()
    elif vtk_class == 'vtkCubeSource':
        source = vtkCubeSource()
    elif vtk_class == 'vtkLineSource':
        source = vtkLineSource()
        
    properties["edgeVisibility"] = True
    properties["lineWidth"] = 2
    
    # create an actor
    actor = vtkActor()
    if properties["edgeVisibility"]:
        actor.GetProperty().EdgeVisibilityOn()
    actor.GetProperty().SetLineWidth(properties["lineWidth"])
    
    # actor.GetProperty().SetColor(colors.GetColor("Gray", r,g,b, 1))
    # vtk_color = colors.GetColorRGB(f"{obj['id']}_Color", properties.get('color', [0.0,0.0,1.0]))
    col = properties.get('color', [1.0,0.0,0.0])
    r, g, b = col
    actor.GetProperty().SetColor(r, g, b)
    # opacity = 1 if properties['opacity'] else 0
    actor.GetProperty().SetOpacity(1)
    # create a mapper
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())

    actor.SetMapper(mapper)
    obj['instance'] = {}
    obj['instance']['actor'] = actor
    obj['instance']['source'] = source
    obj['instance']['mapper'] = mapper
    return obj
  
  # def get_vtk_models(self):
  #   for k in self.models.keys():
  #     actor = self.models[k].get('actor', None)
  #     source = self.models[k].get('source', None)
  #     mapper = self.models[k].get('mapper', None)
  #     if actor is None:
  #       actor, source, mapper = self.make_vtk_model(self.models[k])
  #       self.models[k]['actor'] = actor
  #       self.models[k]['source'] = source
  #       self.models[k]['mapper'] = mapper
  #     return actor

  @staticmethod
  def add_axis_to_scene(renderer):
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

class VtkRenderer:
  def __init__(self):
    self.vtk_models = []
    self.colors = vtkNamedColors()
    self.renderWindow = vtkRenderWindow()
    self.renderWindow.SetWindowName('Axes')
    self.renderWindow.SetSize(1920,1080)
    
    self.renderer = vtkRenderer()
    br, bg, bb = [34/255, 47/255, 62/255]
    self.renderer.SetBackground(br, bg, bb)
    self.renderWindow.AddRenderer(self.renderer)
    
    self.camera = self.renderer.GetActiveCamera()
    self.camera.SetViewUp([0,0,1])
    self.camera.SetPosition([0.9,0.9,0.25])
    
    self.interactors = []
    self.renderWindowInteractor = vtkRenderWindowInteractor()
    self.renderWindowInteractor.SetRenderWindow(self.renderWindow)
    self.renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()
    
    self.kp_interactor = KeyPressInteractorStyle(parent=self.renderWindowInteractor)
    self.renderWindowInteractor.SetInteractorStyle(self.kp_interactor)
    self.interactors.append(self.kp_interactor)
    
    self.timer = Timer(self.renderer, self.renderWindow)
    self.renderer.AddObserver('StartEvent', self.timer)
    
    self.observers = {}
    self.observers['Updater'] = ModelsUpdater(self)
    for k in self.observers.keys():
      # Here is where we setup the observer.
      self.renderer.AddObserver('StartEvent', self.observers[k])
      
    VtkModel.add_axis_to_scene(self.renderer)
    
  def add_model(self, vtk_model):
    vtk_model.vtk_renderer.add_models_to_scene(self.renderer)
    self.vtk_models.append(vtk_model)
  
  def vtk_update(self):
    points = self.get_trace_points()
    orientation = self.transform.get_euler_angles(order="zxy")
    p1 = list(points[0][0:3])
    if len(points) > 1:
      p2 = list(points[1][0:3])
      length = v_dist(p1, p2)
      if self.vtk_source is not None:
        self.vtk_source.SetCenter([p1[0], p1[1], p1[2]+length*0.5])
      if self.vtk_actor is not None:
        self.vtk_actor.SetOrigin(p1)
        self.vtk_actor.SetOrientation(orientation)
    
  def draw(self):
    pass
  
  def start(self, ui_type="vtk"):
    if ui_type.lower() == "qt":
      self.start_qt_app(self.renderer, self.renderWindow, self.renderWindowInteractor)
    else:
      self.start_vtk_app(self.renderer, self.renderWindow, self.renderWindowInteractor)
    
  def start_qt_app(self, renderer=None, renderWindow=None, renderWindowInteractor=None):
    app = QApplication(sys.argv)
    ex = MainWindow(renderer, renderWindow, renderWindowInteractor)
    sys.exit(app.exec_())
  
  def start_vtk_app(self, renderer=None, renderWindow=None, renderWindowInteractor=None):
    self.renderer.ResetCamera()
    self.renderWindow.Render()
      
    # begin mouse interaction
    # for interactor in self.interactors:
    #   interactor.Initialize()
    
    self.renderWindowInteractor.Initialize()      
    print("\n\n\n")
    running = True
    while running:
      # if kp_interactor is not None:
      #   running = kp_interactor.status
      if running:
        self.renderWindowInteractor.ProcessEvents()
        self.renderWindowInteractor.Render()
      else:
        self.renderWindowInteractor.TerminateApp()
    # renderWindowInteractor.Start()