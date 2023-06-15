from timeit import default_timer as timer
import time

class Observer(object):
  """
  Callback for the interaction.
  """

  def __init__(self, rendererComponent):
    self.rendererComponent = rendererComponent
    self.delta_time = 0
    self.last_time = 0
    self.time_elapsed = 0
    self.fps = 0
    
  def update(self):
    pass
  
  def __call__(self, caller, ev):
    now = time.time_ns()/1000000000
    self.rendererComponent.delta_time = now - self.rendererComponent.last_time
    self.rendererComponent.last_time = now
    self.rendererComponent.time_elapsed = now - self.rendererComponent.start_time
    self.rendererComponent.fps = 1.0 / self.rendererComponent.delta_time
    self.delta_time = self.rendererComponent.delta_time
    self.last_time = self.rendererComponent.last_time
    self.time_elapsed = self.rendererComponent.time_elapsed
    self.fps = self.rendererComponent.fps
    self.update()
