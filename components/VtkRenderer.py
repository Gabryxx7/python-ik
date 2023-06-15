""" Main VTK Renderer
  - Official tutorials: https://examples.vtk.org/site/Python/#tutorial
  - VTK QT Example: https://stackoverflow.com/questions/69200800/pyqt5-and-vtk-object-integration
"""
from copy import deepcopy
import time
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

class VtkModel:
  def __init__(self, obj, name="VtkModel", modelType=ModelType.SPHERE):
    self.obj = obj
    self.modelType = modelType
    self.uuid = f"VtkModel_{self.obj.uuid}"
    self.models = {
      "model":  {"type": self.modelType},
      "x_axis": {"type": ModelType.X_AXIS},
      "y_axis": {"type": ModelType.Y_AXIS},
      "z_axis": {"type": ModelType.Z_AXIS}
    }
  
  def get_vtk_model_data(self, draw_children=True, dbg_prefix=""):
    thickness = 8
    radius = 10
    points = self.obj.get_trace_points()
    color =  hex_to_rgb(self.obj.trace_params.get('color', "#FFFFFF"))
    orientation = self.obj.transform.get_euler_angles(order="zxy")
    model_data = []
    p1 = list(points[0][0:3])
    # I really don't get why the orientation does not work, everything seems ok except for the orientation of these stupid cubes
    opacity = 1 if self.obj.visible else 0
    joint_origin_point = {
      'id': self.obj.uuid+"point",
      'vtkClass': 'vtkSphereSource',
      'property': {
        'opacity': opacity,
        'color': color,
        'pointSize': 20,
      },
      'actor': {
        'origin': p1,
        'position': [0,0,0],
        'orientation': orientation,
      },
      'state': {
        "lineWidth": 10,
        "center": p1,
        "radius": radius,
        'resolution': 600
      }
    }
    model_data.append(joint_origin_point)
    
    if len(points) > 1:
      p2 = list(points[1][0:3])
      length = v_dist(p1, p2)
      joint_line = {
        'id': self.uuid+"line",
        'vtkClass': 'vtkLineSource',
        'property': {
          'opacity': opacity,
          'color': color,
          'pointSize': 10,
          },
        'actor': {
        },
        'state': {
          "lineWidth": 10,
          'point1': p1,
          'point2': p2,
          'resolution': 600
        }
      }
      model_data.append(joint_line)
      joint_cube = {
        'id': self.uuid+"cube",
        'vtkClass': 'vtkCubeSource',
        'property': {
          'opacity': opacity,
          'color': color,
          # 'pointSize': 10,
          },
        'actor': {
          'origin': p1,
          'position': [0,0,0],
          'orientation': orientation,
        },
        'state': {
          'center': [p1[0], p1[1], p1[2]+length*0.5],
          'zLength': length,
          'xLength': thickness,
          'yLength': thickness,
          'resolution': 600
        }
      }
      model_data.append(joint_cube)
    if not draw_children:
      return model_data
    
    dbg_prefix += "  "
    for child in self.children:
      child_model = child.get_vtk_model_data(draw_children=False, dbg_prefix=dbg_prefix)
      if child_model is not None and len(child_model) > 0:
        model_data += child_model
    # print(model_data)
    return model_data
  
  def update_vtk_model_data(self, draw_children=True, dbg_prefix=""):
    model_data = []
    points = self.get_trace_points()
    # print(f"{self.name} - Visible: {self.visible} - Prev Visible: {self.prev_visible}")
    if not self.visible:
      if self.visible == self.prev_visible:
        # print(f"No model update: {self.name}")
        joint_origin =  {'property': dash.no_update, 'actor': dash.no_update, 'state': dash.no_update}
        model_data.append(joint_origin)
        if len(points) > 1:
          joint_line =  {'property': dash.no_update, 'actor': dash.no_update, 'state': dash.no_update}
          joint_cube =  {'property': dash.no_update, 'actor': dash.no_update, 'state': dash.no_update}
          model_data.append(joint_line)
          model_data.append(joint_cube)
        if not draw_children:
          return model_data
        for child in self.children:
          child_model = child.update_vtk_model_data(draw_children=False, dbg_prefix=dbg_prefix)
          if child_model is not None and len(child_model) > 0:
            model_data += child_model
        return model_data
    opacity = 1 if self.visible else 0
    p1 = list(points[0][0:3])
    orientation = self.transform.get_euler_angles(order="zxy")
    joint_origin =  {
      'property': {
        'opacity': opacity
      },
      'actor': {
        'origin': p1,
        'orientation': orientation
        },
      'state': {
        "center": p1
      }
    }
    model_data.append(joint_origin)
    
    if len(points) > 1:
      p2 = list(points[1][0:3])
      length = v_dist(p1, p2)
      joint_line =  {
        'property': {
          'opacity': opacity
        },
        'actor': {},
        'state': {'point1': p1, 'point2': p2}}
      model_data.append(joint_line)
      
      joint_cube =  {
        'property': {
          'opacity': opacity
        },
        'actor': {
          'origin': p1,
          'orientation': orientation,
        },
        'state': {
          'center': [p1[0], p1[1], p1[2]+length*0.5],
        }
      }
      model_data.append(joint_cube)
    print(f"VTK Model model update: {self.name}")
    if not draw_children:
      return model_data
    
    dbg_prefix += "  "
    for child in self.children:
      child_model = child.update_vtk_model_data(draw_children=False, dbg_prefix=dbg_prefix)
      if child_model is not None and len(child_model) > 0:
        model_data += child_model
    # print(model_data)
    return model_data
  
  def make_vtk_model(self, obj):
    obj['model'] = deepcopy(DefaultVTKModels[obj['type']])
    state = obj['model'].get('state', {})
    actor_prop = obj['model'].get('actor', {})
    properties = obj['model'].get('property', {})
    
    if obj['model']['vtkClass'] == 'vtkSphereSource':
        source = vtkSphereSource()
        source.SetCenter(state.get('center', [0,0,0]))
        source.SetRadius(state.get('radius', 50))
    elif obj['model']['vtkClass'] == 'vtkCubeSource':
        source = vtkCubeSource()
        source.SetXLength(state['xLength'])
        source.SetZLength(state['zLength'])
        source.SetYLength(state['yLength'])
        source.SetCenter(state.get('center', [0,0,0]))
    elif obj['model']['vtkClass'] == 'vtkLineSource':
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
    return actor, source, mapper
  
  def get_vtk_models(self):
    for k in self.models.keys():
      actor = self.models[k].get('actor', None)
      source = self.models[k].get('source', None)
      mapper = self.models[k].get('mapper', None)
      if actor is None:
        actor, source, mapper = self.make_vtk_model(self.models[k])
        self.models[k]['actor'] = actor
        self.models[k]['source'] = source
        self.models[k]['mapper'] = mapper
      return actor
  
  @staticmethod
  def add_model_to_dash_vtk(model, renderer):
    model.update()
    vtk_model_data = model.get_vtk_model_data()
    assigned = False
    for vtk_model in vtk_model_data:
      source, actor = VtkModel.make_vtk_model(vtk_model)
      print(f"Adding {vtk_model['id']}")
      renderer.AddActor(actor)
      if not assigned:
        if 'cube' in vtk_model['id'].lower():
          model.vtk_source = source
          model.vtk_actor = actor
          assigned = True

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
    self.models = []
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
    # self.observers['Updater'] = ModelsUpdater(self)
    for k in self.observers.keys():
      # Here is where we setup the observer.
      self.renderer.AddObserver('StartEvent', self.observers[k])
      
    VtkModel.add_axis_to_scene(self.renderer)
    # for model in models:
    #   VtkModel.add_model_to_dash_vtk(model, renderer)
    
  def add_model(self, model):
    # VtkModel.add_model_to_dash_vtk(model, self.renderer)
    # self.models
    pass
  
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