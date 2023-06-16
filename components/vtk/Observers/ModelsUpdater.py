from components.vtk.Observers.Observer import Observer
class ModelsUpdater(Observer):
  def update(self):
    models = self.rendererComponent.vtk_models
    for model in models:
      model.update()
      model.vtk_renderer.update_models()
    
  # def update_models(delta_time, models, offset):
  #   speed = 100
  #   for model in models:
  #     model.rotate([offset*speed, offset*speed*0.5, offset*speed*0.2])
  #     model.update()
  #     model.vtk_update()
  #   offset += delta_time
  #   if offset >= 360:
  #     offset = 0