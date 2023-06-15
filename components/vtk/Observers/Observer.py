from timeit import default_timer as timer
import time

"""
Callback for the interaction.
"""
class Observer(object):
  def __init__(self, rendererComponent):
    self.rendererComponent = rendererComponent
    self.timer = self.rendererComponent.timer
    
  def update(self):
    pass
  
  def __call__(self, caller, ev):
    self.timer = self.rendererComponent.timer
    self.update()
