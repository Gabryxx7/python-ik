from components.vtk.Observers.Observer import Observer
from vtkmodules.vtkRenderingCore import vtkTextActor, vtkTextProperty
import time

TIME_UNIT = 1000000000 #ns

class Timer(object):
  def __init__(self, renderer, window):
    self.start_time = time.time_ns()
    self.last_time = time.time_ns()
    self.delta_time = 0
    self.time_elapsed = 0
    self.fps = 0
    
    self.avg_window_secs = 0.5
    self.avg_window = self.avg_window_secs * TIME_UNIT
    self.avg_elapsed = 0
    self.acc_fps = 0
    self.avg_fps = 0
    self.max_fps = 60
    self.exp_delta_time = self.max_fps/TIME_UNIT
    
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
    self.acc_fps += TIME_UNIT
    if self.avg_elapsed >= self.avg_window:
      self.avg_fps = self.acc_fps / self.avg_elapsed
      self.acc_fps = 0
      self.avg_elapsed = 0
  
  def update_fps(self):
    now = time.time_ns()
    self.delta_time = now - self.last_time
    self.last_time = now
    self.time_elapsed = (now - self.start_time)/TIME_UNIT
    if self.delta_time > 0:
      self.fps = TIME_UNIT / self.delta_time
    
  def __call__(self, caller, ev):
    self.update_fps()
    self.update_avg_fps()
    # while self.avg_fps >= self.max_fps:
    #   # print(f"Avg FPS: {self.avg_fps:.2f}\tdelta_time: {self.delta_time:.2f}\texp_delta_time {self.exp_delta_time:.2f}")
    #   if self.delta_time > self.exp_delta_time:
    #     time.sleep((self.delta_time - self.exp_delta_time)/TIME_UNIT)
    #   self.update_fps()
    #   self.update_avg_fps()
    fps_str = ""
    spacing = f"{' ':<10}"
    # fps_str = f"FPS: {self.fps:.2f}{spacing}Avg FPS: {self.avg_fps:.2f}{spacing}DeltaTime: {self.delta_time/TIME_UNIT:.3f}{spacing}Elapsed: {self.time_elapsed:.3f}"
    fps_str = f"Avg FPS: {self.avg_fps:.2f}{spacing}DeltaTime: {self.delta_time/TIME_UNIT:.3f}{spacing}Elapsed: {self.time_elapsed:.3f}"
    print(fps_str, end="\r")
    self.fpsActor.SetInput(fps_str)