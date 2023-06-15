
class FPSObserver(Observer):
  def update(self):
    print(f"FPS: {self.fps:.2f}\tElapsed: {self.delta_time}")