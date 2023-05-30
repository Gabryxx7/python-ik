import uuid
import numpy as np
from pyquaternion import Quaternion
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager
from copy import deepcopy
from machine.joint import *
from machine.IModel import IModel

DEFAULT_PLANE_TRACE = {
  "name": "Axis Joint",
  "showlegend": True,
  "type": "mesh3d",
  "opacity": BODY_MESH_OPACITY,
  "color": BODY_MESH_COLOR,
  "x": [],
  "y": [],
  "z": [],
}

class Plane(IModel):
  def __init__(self, _name, _origin):
    self.name = _name
    self.prev = None
    self.next = None
    self.uuid = str(uuid.uuid4())
    self.absolute_pos = deepcopy(_origin)
    self.tm = TransformManager()
    self.joints = []
    self.origin = Joint("Origin", self.absolute_pos)
    self.origin.transform = pt.transform_from_pq(np.hstack((np.array(self.absolute_pos), pr.q_id)))
    self.trace = deepcopy(DEFAULT_PLANE_TRACE)
    self.visible = True
    self.arms = []
    self.pistons = []
  
  def get_top_right_side_widgets(self, app):
    r_widgets = []
    for i in range(0, len(plane_model['arms'])):
        tf_widget = make_transform_widget(app, plane_model['arms'][i].joints[0])
        # tf_widget_ee, tf_output_ee = make_transform_widget(app, plane_model['arms'][i].joints[1])
        r_widgets.append(tf_widget)
        # tf_widget, tf_output = make_transform_widget(app, plane_model['arms'][i].joints[0])
        # tf_widget_ee, tf_output_ee = make_transform_widget(app, plane_model['arms'][i].joints[1])
        # plane_model['arm_joint0_inputs'].append(arm_joint0_inpt)
        # plane_model['tf_widgets'].append(tf_widget)
        # plane_model['tf_outputs'].append(tf_output)
        # plane_model['tf_widgets_ee'].append(tf_widget_ee)
        # plane_model['tf_outputs_ee'].append(tf_output_ee)
    return l_widgets
  
  def get_left_side_widgets(self, app):
    l_widgets = []
    plane_model['piston_inputs'] = []
    for i in range(0, len(plane_model['pistons'])):
        piston_widget = make_piston_widget(plane_model['pistons'][i].uuid, f"Piston {i+1}", PISTON_START_HEIGHT_RATIO, _min=0, _max=1, _input_resolution=0.05)
        l_widgets.append(piston_widget)
    
    for i in range(0, len(plane_model['arms'])):
        arm_joint0_widget = make_quaternion_widget(app, plane_model['arms'][i].joints[0])
        l_widgets.append(arm_joint0_widget)
        # tf_widget, tf_output = make_transform_widget(app, plane_model['arms'][i].joints[0])
        # tf_widget_ee, tf_output_ee = make_transform_widget(app, plane_model['arms'][i].joints[1])
        # plane_model['arm_joint0_inputs'].append(arm_joint0_inpt)
        # plane_model['tf_widgets'].append(tf_widget)
        # plane_model['tf_outputs'].append(tf_output)
        # plane_model['tf_widgets_ee'].append(tf_widget_ee)
        # plane_model['tf_outputs_ee'].append(tf_output_ee)
    return l_widgets
  
  def add_joint(self, joint):
    self.joints.append(joint)
    # if len(self.joints) > 1:
    #   self.joints[-2].link_to(self.joints[-1])
    #   self.joints[-1].update_transform()
    #   self.tm.add_transform(f"joint_{len(self.joints)-2}", f"joint_{len(self.joints)-1}", self.joints[-2].transform)
    #   return
    # self.origin.link_to(self.joints[0])
    
  def forward_kinematics(self):
    combined_transform = None
    for i in range(0,len(self.joints)):
      idx = i
      self.joints[idx].update_transform()
      self.joints[idx].apply_transform(combined_transform)
  
  def set_visibility(self, vis):
    self.visible = vis
    for j in self.joints:
      figure_data = j.set_visibility(vis)
      
  def draw(self, figure_data):
    trace = self.get_trace(figure_data)
    
    points = [j.absolute_pos for j in self.joints]
    trace['x'] = [float(p[AXIS_ORDER_CONVENTION[0]]) for p in points]
    trace['y'] = [float(p[AXIS_ORDER_CONVENTION[1]]) for p in points]
    trace['z'] = [float(p[AXIS_ORDER_CONVENTION[2]]) for p in points]
    trace['visible'] = self.visible
    return figure_data
    