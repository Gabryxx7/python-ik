from machine.joint import Joint
from machine.arm import Arm
from machine.plane import Plane
import numpy as np


PISTON_HEIGHT = 200.0
PISTON_START_HEIGHT_RATIO = 1
PLANE_INITIAL_HEIGHT = PISTON_HEIGHT*1.5
PISTON_ARM_LENGTH = 50
VTest_1 = [0.0, 0.0, 100]
VTest_2 = [VTest_1[0], VTest_1[1]+50, VTest_1[2]+50]
VTest_3 = [VTest_2[0]+25, VTest_2[1]+25, VTest_2[2]+25]
VTest_4 = [VTest_3[0]+50, VTest_3[1]+25, VTest_3[2]+25]

origin = [0,0,0]
arm_test = Arm("Test Arm", origin)
arm_test.add_joint(Joint("TA_Joint0", origin, color="#90FF33"))
arm_test.add_joint(Joint("TA_Joint1", VTest_1, color="#33FF74"))
arm_test.add_joint(Joint("TA_Joint2", VTest_2, color="#33FFEC"))
arm_test.add_joint(Joint("TA_Joint3", VTest_3, color="#33C1FF"))
test_model = {'arm': arm_test}

# origin = [200,250,0]
# VTest_1 = np.add(origin, VTest_1)
# VTest_2 = np.add(VTest_2, VTest_1)
# VTest_3 = np.add(VTest_3, VTest_2)
# arm2 = Arm("Test Arm2", origin)
# piston2.add_joint(Joint("TA2_Joint0", origin))
# piston2.add_joint(Joint("TA2_Joint1", VTest_1))
# piston2.add_joint(Joint("TA2_Joint2", VTest_2))
# piston2.add_joint(Joint("TA2_Joint3", VTest_3))
# arm.add_joint(Joint("TA_Joint4", VTest_4))

model_arms = []
model_pistons = []

origin = [-200,-200,0]
color="#90FF33"
piston1 = Arm("Arm1_Piston", origin)
piston1.add_joint(Joint("Arm1_Joint0", origin))
piston1.add_joint(Joint("Arm1_Joint1", np.add(origin, [0,0,PISTON_HEIGHT])))
model_pistons.append(piston1)
arm1_2 = Arm("Arm1_Arm", origin)
# arm1_2.add_joint(Joint("Arm1_2_Joint0", origin, color=color))
arm1_2.add_joint(Joint("Arm1_2_Joint1", np.array([origin[0], origin[1], PISTON_HEIGHT*PISTON_START_HEIGHT_RATIO]), color=color))
# arm1_2.add_joint(Joint("Arm1_2_Joint2", np.array([origin[0]-origin[0]*1.25, origin[1]-origin[1]*1.25, PISTON_ARM_LENGTH]), color=color))
arm1_2.add_joint(Joint("Arm1_2_Joint2", np.array([origin[0]-origin[0]*1.25, origin[1]-origin[1]*1.25, PISTON_ARM_LENGTH]), color=color))
model_arms.append(arm1_2)

origin = [200,200,0]
color="#33FFEC"
piston2 = Arm("Arm2_Piston", origin)
piston2.add_joint(Joint("Arm2_Joint0", origin))
piston2.add_joint(Joint("Arm2_Joint1", np.add(origin, [0,0,PISTON_HEIGHT])))
model_pistons.append(piston2)

arm2_2 = Arm("Arm2_Arm", origin)
# arm2_2.add_joint(Joint("Arm2_2_Joint0", [0,0,0], color=color))
arm2_2.add_joint(Joint("Arm2_2_Joint1", np.array([origin[0], origin[1], PISTON_HEIGHT*PISTON_START_HEIGHT_RATIO]), color=color))
arm2_2.add_joint(Joint("Arm2_2_Joint2", np.array([origin[0]-origin[0]*1.25, origin[1]-origin[1]*1.25, PISTON_ARM_LENGTH]), color=color))
model_arms.append(arm2_2)


origin = [300,-300,0]
color="#33C1FF"
piston3 = Arm("Arm3_Piston", origin)
piston3.add_joint(Joint("Arm3_Joint0", origin))
piston3.add_joint(Joint("Arm3_Joint1", np.add(origin, [0,0,PISTON_HEIGHT])))
model_pistons.append(piston3)

arm3_2 = Arm("Arm3_Arm", origin)
# arm3_2.add_joint(Joint("Arm3_2_Joint0", origin, color=color))
arm3_2.add_joint(Joint("Arm3_2_Joint1", np.array([origin[0], origin[1], PISTON_HEIGHT*PISTON_START_HEIGHT_RATIO]), color=color))
arm3_2.add_joint(Joint("Arm3_2_Joint2", np.array([origin[0]-origin[0]*1.25, origin[1]-origin[1]*1.25, PISTON_ARM_LENGTH]), color=color))
model_arms.append(arm3_2)



# arm2_2.joints[1].link_to(arm1_2.joints[1])
# arm3_2.joints[1].link_to(arm2_2.joints[1])
# # arm3_2.joints[1].link_to(arm1_2.joints[1])

# arm2_2.joints[1].update_transform()
# arm1_2.joints[1].update_transform()
# arm3_2.joints[1].update_transform()


# triangle_v1 = Joint("Tri1_Joint0", arm1_2.joints[1]._origin)
# arm1_2.add_joint(triangle_v1)
# arm1_2.joints[1].link_to(triangle_v1)
# triangle_v1.link_to(arm1_2.joints[1])

# triangle_v2 = Joint("Tri2_Joint0", arm2_2.joints[1]._origin)
# arm2_2.add_joint(triangle_v2)
# arm2_2.joints[1].link_to(triangle_v2)
# triangle_v2.link_to(arm2_2.joints[1])

# triangle_v3 = Joint("Tri3_Joint0", arm3_2.joints[1]._origin)
# arm3_2.add_joint(triangle_v3)
# arm3_2.joints[1].link_to(triangle_v3)
# triangle_v3.link_to(arm3_2.joints[1])

# triangle_v1.link_to(triangle_v2)
# triangle_v2.link_to(triangle_v1)
# triangle_v3.link_to(triangle_v2)

plane = Plane("Arm1", origin)
plane.add_vertex(arm1_2.joints[1])
plane.add_vertex(arm2_2.joints[1])
plane.add_vertex(arm3_2.joints[1])

plane_model = {'pistons': model_pistons, 'arms': model_arms, 'plane': plane}