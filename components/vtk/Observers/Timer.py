from components.vtk.Observers.Observer import Observer
from vtkmodules.vtkRenderingCore import vtkTextActor, vtkTextProperty
import time

class Timer(object):
  def __init__(self, renderer, window):
    self.start_time = time.time_ns()/1000000000
    self.last_time = time.time_ns()/1000000000
    self.delta_time = 0
    self.time_elapsed = 0
    self.fps = 0
    
    self.avg_window_secs = 0.5
    self.avg_elapsed = 0
    self.acc_fps = 0
    self.avg_fps = 0
    
    self.fpsActor = vtkTextActor()
    self.fpsActor.SetInput("")
    w, h = window.GetActualSize()
    offset = 30
    self.fpsActor.SetPosition(offset, h-(offset*1.5))
    self.fpsActor.GetTextProperty().SetFontSize(24)
    self.fpsActor.GetTextProperty().SetColor(1.0, 1.0, 1.0)
    renderer.AddActor2D(self.fpsActor);
    
  def update_avg_fps(self):
    self.avg_elapsed += self.delta_time
    self.acc_fps += 1
    if self.avg_elapsed >= self.avg_window_secs:
      self.avg_fps = self.acc_fps / self.avg_elapsed
      self.acc_fps = 0
      self.avg_elapsed = 0
    
  def __call__(self, caller, ev):
    now = time.time_ns()/1000000000
    self.delta_time = now - self.last_time
    self.last_time = now
    self.time_elapsed = now - self.start_time
    self.fps = 1.0 / self.delta_time
    self.update_avg_fps()
    spacing = f"{' ':<10}"
    fps_str = f"FPS: {self.avg_fps:.2f}{spacing}DeltaTime: {self.delta_time:.3f}{spacing}Elapsed: {self.time_elapsed:.3f}"
    print(fps_str, end="\r")
    self.fpsActor.SetInput(fps_str)