from models.basic.plane import Plane
from models.circle import Circle
from models.basic.joint import Joint
from models.arm import Arm
from models.compound_model import CompoundModel
from models.compound_model import PISTON_HEIGHT, PISTON_ARM_LENGTH, PISTON_START_HEIGHT_RATIO, PLANE_INITIAL_HEIGHT, PISTON_START_HEIGHT
import numpy as np




# ***************************************
# TEST ARM
# ***************************************

origin = [0,0,0]
VTest_1 = [0.0, 0.0, 100]
VTest_2 = [VTest_1[0], VTest_1[1]+50, VTest_1[2]+50]
VTest_3 = [VTest_2[0]+25, VTest_2[1]+25, VTest_2[2]+25]
VTest_4 = [VTest_3[0]+50, VTest_3[1]+25, VTest_3[2]+25]

arm_test = Arm("Test_Arm", [0,0,0])
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

machine = CompoundModel("Machine", origin)

machine_plane = Plane("PTriangle", [0, 0, 200], trace_params={'markersize': 10, 'linewidth': 11, 'linecolor': "#ffffff", 'meshcolor': "#ff6666"})
machine_plane.add_vertex([-100, 100, 0])
machine_plane.add_vertex([100, 100, 0])
machine_plane.add_vertex([0, -100, 0])

  
origin = [0,-100-PISTON_ARM_LENGTH,0]
color="#90FF33"
arm1 = Arm("Arm1_Piston", origin)
arm1.add_joint(Joint("Arm1_Joint0", [0,0,PISTON_HEIGHT], trace_params={'color':"#ff6666"}))
arm1.add_joint(Joint("Arm1_EE", [0, PISTON_ARM_LENGTH, PISTON_ARM_LENGTH], trace_params={'color':color}))

origin = [100+PISTON_ARM_LENGTH,100+PISTON_ARM_LENGTH,0]
color="#33FFEC"
arm2 = Arm("Arm2_Piston", origin)
arm2.add_joint(Joint("Arm2_Joint0", [0,0,PISTON_HEIGHT], trace_params={'color':"#ff6666"}))
arm2.add_joint(Joint("Arm2_EE", [-PISTON_ARM_LENGTH, -PISTON_ARM_LENGTH, PISTON_ARM_LENGTH], trace_params={'color':color}))

origin = [-100-PISTON_ARM_LENGTH,100+PISTON_ARM_LENGTH,0]
color="#33C1FF"
arm3 = Arm("Arm3_Piston", origin)
arm3.add_joint(Joint("Arm3_Joint0", [0,0,PISTON_HEIGHT], trace_params={'color':"#ff6666"}))
arm3.add_joint(Joint("Arm3_EE", [PISTON_ARM_LENGTH, -PISTON_ARM_LENGTH, PISTON_ARM_LENGTH], trace_params={'color':color}))

machine.add_plane(machine_plane)
machine.add_arm(arm1)
machine.add_arm(arm3)
machine.add_arm(arm2)
machine.forward_kinematics()