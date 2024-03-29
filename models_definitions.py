from objects.plane import Plane
from objects.circle import Circle
from objects.joint import Joint
from objects.arm import Arm
from objects.compound_model import CompoundModel
from objects.compound_model import PISTON_HEIGHT, PISTON_ARM_LENGTH, PISTON_START_HEIGHT_RATIO, PLANE_INITIAL_HEIGHT, PISTON_START_HEIGHT
import numpy as np
import math



v_dist = lambda p, orig=[0,0,0]: (np.linalg.norm(np.array(orig) - np.array(p)))

# ***************************************
# TEST ARM
# ***************************************

origin = [0,0,0]
VTest_1 = [0.0, 0.0, 100]
VTest_2 = [VTest_1[0], VTest_1[1]+50, VTest_1[2]+50]
VTest_3 = [VTest_2[0]+25, VTest_2[1]+25, VTest_2[2]+25]
VTest_4 = [VTest_3[0]+50, VTest_3[1]+25, VTest_3[2]+25]

arm_test = Arm("Test_Arm", [0,0,0], trace_params={'color':"#22DAE6"})
arm_test.add_joint(Joint("First", [0.0, 0.0, 80], trace_params={'color':"#33FF74"})) # Offset from origin
arm_test.add_joint(Joint("Second", [0.0, 0.0, 80], trace_params={'color':"#FF3F33"})) # Offset from First
arm_test.add_joint(Joint("EE", [0.0, 0.0, 80], trace_params={'color':"#33C1FF"})) # Offset from Second

# ***************************************
# TEST PLANE
# ***************************************
plane_test = Plane("Plane_Test", [0, 0, 200])
V1 = [-100, 100, 0]
# print(f"V1 length: {v_dist(V1)}")
plane_test.add_vertex(V1)
V2 = [100, 100, 0]
# print(f"V2 length: {v_dist(V2)}")
plane_test.add_vertex(V2)
V3 = [0, v_dist(V1), 0]
# print(f"V3 length: {v_dist(V3)}")
plane_test.add_vertex(V3)

circle_test = Circle("circle_test", offset_pos=[0, 0, 200], radius=100)

# ***************************************
# COMPOUND PLANE + PISTONS
# ***************************************

machine = CompoundModel("Machine", origin)

machine_plane = Plane("PTriangle", [0, 0, 200], trace_params={'markersize': 10, 'linewidth': 11, 'linecolor': "#ffffff", 'meshcolor': "#ff6666"})
V1 = [-100, 100, 0]
V2 = [100, 100, 0]
V3 = [0, -v_dist(V1), 0]
machine_plane.add_vertex(V1)
machine_plane.add_vertex(V2)
machine_plane.add_vertex(V3)


origin = np.add(V3,[0,-PISTON_ARM_LENGTH,0])
color="#90FF33"
arm1 = Arm("Arm1_Piston", origin)
arm1.add_joint(Joint("Arm1_Joint0", [0,0,PISTON_HEIGHT], trace_params={'color':"#ff6666"}))
arm1.add_joint(Joint("Arm1_EE", [0, PISTON_ARM_LENGTH, PISTON_ARM_LENGTH], trace_params={'color':color}))

origin = np.add(V2, [PISTON_ARM_LENGTH,PISTON_ARM_LENGTH,0])
color="#33FFEC"
arm2 = Arm("Arm2_Piston", origin)
arm2.add_joint(Joint("Arm2_Joint0", [0,0,PISTON_HEIGHT], trace_params={'color':"#ff6666"}))
arm2.add_joint(Joint("Arm2_EE", [-PISTON_ARM_LENGTH, -PISTON_ARM_LENGTH, PISTON_ARM_LENGTH], trace_params={'color':color}))

origin = np.add(V1, [-PISTON_ARM_LENGTH,+PISTON_ARM_LENGTH,0])
color="#33C1FF"
arm3 = Arm("Arm3_Piston", origin)
arm3.add_joint(Joint("Arm3_Joint0", [0,0,PISTON_HEIGHT], trace_params={'color':"#ff6666"}))
arm3.add_joint(Joint("Arm3_EE", [PISTON_ARM_LENGTH, -PISTON_ARM_LENGTH, PISTON_ARM_LENGTH], trace_params={'color':color}))

machine.add_plane(machine_plane)
machine.add_arm(arm1)
machine.add_arm(arm3)
machine.add_arm(arm2)
machine.forward_kinematics()