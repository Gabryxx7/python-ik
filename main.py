from multiprocessing import Process, Pool
import frontend.dash.dashboard as dash_viwer
import frontend.vtk_viewer.vtk_viewer as vtk_viwer

from models_definitions import arm_test, plane_test, circle_test, machine

models = []
models.append(arm_test)
# models.append(machine)
# models.append(circle_test)
# models.append(plane_test)
    
def start_dash():
  dash_viwer.setup_page(p_models=models)
  dash_viwer.start_server(debug=False)
  
def start_vtk():
  vtk_viwer.start_viewer(p_models=models)
  
def start_all():
  p_dash = Process(target=start_dash)
  p_vtk = Process(target=start_vtk)
  p_dash.start()
  p_vtk.start()
  p_dash.join()
  p_vtk.join()

if __name__ == '__main__':
  # start_vtk()
  # start_dash()
  start_all()