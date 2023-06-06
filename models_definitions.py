from models.basic.plane import Plane
from models.circle import Circle
from models.basic.joint import Joint
from models.arm import Arm
from models.compound_model import CompoundModel
import numpy as np




# ***************************************
# TEST ARM
# ***************************************

origin = [0,0,0]
VTest_1 = [0.0, 0.0, 100]
VTest_2 = [VTest_1[0], VTest_1[1]+50, VTest_1[2]+50]
VTest_3 = [VTest_2[0]+25, VTest_2[1]+25, VTest_2[2]+25]
VTest_4 = [VTest_3[0]+50, VTest_3[1]+25, VTest_3[2]+25]

arm_test = Arm("Test_Arm", origin)
arm_test.add_joint(Joint("First", [0.0, 0.0, 80], trace_params={'color':"#33FF74"})) # Offset from origin
arm_test.add_joint(Joint("Second", [0.0, 0.0, 80], trace_params={'color':"#33FFEC"})) # Offset from First
arm_test.add_joint(Joint("EE", [0.0, 0.0, 80], trace_params={'color':"#33C1FF"})) # Offset from Second

# ***************************************
# TEST PLANE
# ***************************************

plane_test = Plane("Plane_Test", [0, 0, 200])
plane_test.add_vertex([-100, 100, 0])
plane_test.add_vertex([100, 100, 0])
plane_test.add_vertex([0, -100, 0])


circle_test = Circle("circle_test", offset_pos=[0, 0, 200], radius=100)

# ***************************************
# COMPOUND PLANE + PISTONS
# ***************************************

PISTON_HEIGHT = 200.0
PISTON_START_HEIGHT_RATIO = 1
PISTON_ARM_LENGTH = 50
PISTON_START_HEIGHT = PISTON_HEIGHT * PISTON_START_HEIGHT_RATIO
PLANE_INITIAL_HEIGHT = PISTON_HEIGHT*1.5

machine = CompoundModel("Machine", origin)

machine_plane = Plane("PTriangle", [0, 0, 200], trace_params={'markersize': 10, 'linewidth': 11, 'linecolor': "#ffffff", 'meshcolor': "#ff6666"})
machine_plane.add_vertex([-100, 100, 0])
machine_plane.add_vertex([100, 100, 0])
machine_plane.add_vertex([0, -100, 0])

machine.add_plane(machine_plane)
  
origin = [0,-100-PISTON_ARM_LENGTH,0]
color="#90FF33"
piston1 = Arm("Arm1_Piston", origin)
piston1.add_joint(Joint("Piston1_Joint0", [0,0,PISTON_HEIGHT], trace_params={'color':"#ff6666"}))

arm1 = Arm("Arm", offset_pos=origin, origin=piston1.children[-1])
arm1.add_joint(Joint("Arm1_EE", np.array([0, PISTON_ARM_LENGTH, PISTON_ARM_LENGTH]), trace_params={'color':color}))

origin = [100+PISTON_ARM_LENGTH,100+PISTON_ARM_LENGTH,0]
color="#33FFEC"
piston2 = Arm("Arm2_Piston", origin)
piston2.add_joint(Joint("Piston2_Joint0", [0,0,PISTON_HEIGHT], trace_params={'color':"#ff6666"}))

arm2 = Arm("Arm", offset_pos=origin, origin=piston2.children[-1])
arm2.add_joint(Joint("Arm2_EE", np.array([-PISTON_ARM_LENGTH, -PISTON_ARM_LENGTH, PISTON_ARM_LENGTH]), trace_params={'color':color}))


origin = [-100-PISTON_ARM_LENGTH,100+PISTON_ARM_LENGTH,0]
color="#33C1FF"
piston3 = Arm("Arm3_Piston", origin)
piston3.add_joint(Joint("Piston3_Joint0", [0,0,PISTON_HEIGHT], trace_params={'color':"#ff6666"}))

arm3 = Arm("Arm", offset_pos=origin, origin=piston3.children[-1])
arm3.add_joint(Joint("Arm3_EE", np.array([PISTON_ARM_LENGTH, -PISTON_ARM_LENGTH, PISTON_ARM_LENGTH]), trace_params={'color':color}))
machine.add_piston(piston1)
machine.add_arm(arm1)
machine.add_piston(piston3)
machine.add_arm(arm3)
machine.add_piston(piston2)
machine.add_arm(arm2)