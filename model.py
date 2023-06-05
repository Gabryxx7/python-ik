from machine.joint import Joint
from machine.arm import Arm
from machine.plane import Plane
from machine.compound_model import CompoundModel
import numpy as np


PISTON_HEIGHT = 200.0
PISTON_START_HEIGHT_RATIO = 1
PISTON_ARM_LENGTH = 50

PISTON_START_HEIGHT = PISTON_HEIGHT * PISTON_START_HEIGHT_RATIO

PLANE_INITIAL_HEIGHT = PISTON_HEIGHT*1.5


VTest_1 = [0.0, 0.0, 100]
VTest_2 = [VTest_1[0], VTest_1[1]+50, VTest_1[2]+50]
VTest_3 = [VTest_2[0]+25, VTest_2[1]+25, VTest_2[2]+25]
VTest_4 = [VTest_3[0]+50, VTest_3[1]+25, VTest_3[2]+25]

origin = [0,0,0]
arm_test = Arm("Test Arm", origin)
arm_test.add_joint(Joint("Base", origin, color="#90FF33"))
arm_test.add_joint(Joint("First", VTest_1, color="#33FF74"))
arm_test.add_joint(Joint("Second", VTest_2, color="#33FFEC"))
arm_test.add_joint(Joint("EE", VTest_3, color="#33C1FF"))

# origin = [200,250,0]
# VTest_1 = np.add(origin, VTest_1)
# VTest_2 = np.add(VTest_2, VTest_1)
# VTest_3 = np.add(VTest_3, VTest_2)
# arm2 = Arm("Test Arm2", origin)
# piston2.add_joint(Joint("TA2_Joint0", origin))
# piston2.add_joint(Joint("TA2_Joint", VTest_1))
# piston2.add_joint(Joint("TA2_EE", VTest_2))
# piston2.add_joint(Joint("TA2_Joint3", VTest_3))
# arm.add_joint(Joint("TA_Joint4", VTest_4))


plane = CompoundModel("Plane", origin)

plane_triangle = Plane("PTriangle", [0, 0, 200])
pt_joint1 = Joint("PTriangle_joint1", [-100, 100, 0])
pt_joint2 = Joint("PTriangle_joint2", [100, 100, 0])
pt_joint3 = Joint("PTriangle_joint3", [0, -100, 0])
plane_triangle.add_joint(pt_joint1)
plane_triangle.add_joint(pt_joint2)
plane_triangle.add_joint(pt_joint3)

plane.add_plane(plane_triangle)
  
origin = [0,-100-PISTON_ARM_LENGTH,0]
color="#90FF33"
piston1 = Arm("Arm1_Piston", origin)
piston1.add_joint(Joint("Piston1_Joint0", [0,0,PISTON_HEIGHT]))

arm1 = Arm("Arm", origin, origin_joint=piston1.joints[-1])
arm1.add_joint(Joint("Arm1_EE", np.array([0, PISTON_ARM_LENGTH, PISTON_ARM_LENGTH]), color=color))

origin = [100+PISTON_ARM_LENGTH,100+PISTON_ARM_LENGTH,0]
color="#33FFEC"
piston2 = Arm("Arm2_Piston", origin)
piston2.add_joint(Joint("Piston2_Joint0", [0,0,PISTON_HEIGHT]))

arm2 = Arm("Arm", origin, origin_joint=piston2.joints[-1])
arm2.add_joint(Joint("Arm2_EE", np.array([-PISTON_ARM_LENGTH, -PISTON_ARM_LENGTH, PISTON_ARM_LENGTH]), color=color))


origin = [-100-PISTON_ARM_LENGTH,100+PISTON_ARM_LENGTH,0]
color="#33C1FF"
piston3 = Arm("Arm3_Piston", origin)
piston3.add_joint(Joint("Piston3_Joint0", [0,0,PISTON_HEIGHT]))

arm3 = Arm("Arm", origin, origin_joint=piston3.joints[-1])
arm3.add_joint(Joint("Arm3_EE", np.array([PISTON_ARM_LENGTH, -PISTON_ARM_LENGTH, PISTON_ARM_LENGTH]), color=color))
plane.add_piston(piston1)
plane.add_arm(arm1)
plane.add_piston(piston3)
plane.add_arm(arm3)
plane.add_piston(piston2)
plane.add_arm(arm2)



triangle = Plane("Triangle", [0, 0, 200])
t_joint1 = Joint("Triangle_joint1", [-100, 100, 0])
t_joint2 = Joint("Triangle_joint2", [100, 100, 0])
t_joint3 = Joint("Triangle_joint3", [0, -100, 0])
triangle.add_joint(t_joint1)
triangle.add_joint(t_joint2)
triangle.add_joint(t_joint3)


# arm2.joints[1].link_to(arm1.joints[1])
# arm2.joints[-1].link_to(arm.joints[-1])
# # arm3.joints[1].link_to(arm1.joints[1])

# arm2.joints[1].update_transform()
# arm1.joints[1].update_transform()
# arm3.joints[1].update_transform()


# triangle_v1 = Joint("Tri1_Joint0", arm1.joints[1]._origin)
# arm1.add_joint(triangle_v1)
# arm1.joints[1].link_to(triangle_v1)
# triangle_v1.link_to(arm1.joints[1])

# triangle_v2 = Joint("Tri2_Joint0", arm2.joints[1]._origin)
# arm2.add_joint(triangle_v2)
# arm2.joints[1].link_to(triangle_v2)
# triangle_v2.link_to(arm2.joints[1])

# triangle_v3 = Joint("Tri3_Joint0", arm3.joints[1]._origin)
# arm3.add_joint(triangle_v3)
# arm3.joints[1].link_to(triangle_v3)
# triangle_v3.link_to(arm3.joints[1])

# triangle_v1.link_to(triangle_v2)
# triangle_v2.link_to(triangle_v1)
# triangle_v3.link_to(triangle_v2)

# plane.add_joint(arm1.joints[-1])
# plane.add_joint(arm2.joints[-1])
# plane.add_joint(arm3.joints[-1])
